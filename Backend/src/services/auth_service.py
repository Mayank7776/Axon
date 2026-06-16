import random
import logging

from datetime import datetime, timedelta, timezone

import jwt  #type:ignore
from pwdlib import PasswordHash #type:ignore
from pwdlib.hashers.argon2 import Argon2Hasher #type:ignore
from fastapi import HTTPException, status #type:ignore
from sqlalchemy.orm import Session #type:ignore
from sqlalchemy import func, or_ #type:ignore

from src.core.settings import settings
from src.models.user_model import User
from src.models.role_model import Role
from src.models.refresh_token import RefreshToken
from src.models.otp_model import LoginOtp
from src.schemas.auth_schema import (
    RefreshTokenRequest,
    RegisterSchema,
    LoginSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
    LoginWithOtpRequest,
    VerifyOtpRequest,
)
from src.utils.email_templates.welcome_mail import send_welcome_email
from src.utils.email_templates.otp_mail import send_login_otp_email
from src.utils.email_templates.reset_password_mail import send_reset_password_email

logger = logging.getLogger(__name__)

# Shared hasher instance (reuse to avoid rebuilding params each call)
_password_hash = PasswordHash([Argon2Hasher()])


# ─────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────

def _hash_password(password: str) -> str:
    return _password_hash.hash(password)

def _verify_password(plain: str, hashed: str) -> bool:
    try:
        return _password_hash.verify(plain, hashed)
    except Exception:
        return False

def _generate_otp() -> str:
    return str(random.randint(100000, 999999))

def _utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)

def _make_access_token(user: User) -> str:
    exp = _utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {"_id": str(user.id), "username": user.username, "email": user.email, "exp": exp},
        settings.ACCESS_TOKEN_SECRET,
        algorithm=settings.ALGORITHM,
    )

def _make_refresh_token(user: User) -> dict:
    exp = _utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    token = jwt.encode(
        {"_id": str(user.id), "scope": "refresh_token", "exp": exp},
        settings.REFRESH_TOKEN_SECRET,
        algorithm=settings.ALGORITHM,
    )
    return {"token": token, "expires_at": exp}

def _decode_token(token: str, secret: str) -> dict:
    """Decode a JWT, raising mapped HTTPExceptions on failure."""
    try:
        return jwt.decode(token, secret, algorithms=[settings.ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Reset link has expired.")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid reset token.")

def _get_user_or_404(db: Session, email: str) -> User:
    user = db.query(User).filter(func.lower(User.email) == email.lower()).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account deactivated. Contact support.")
    return user

def _issue_tokens(user: User, db: Session) -> dict:
    """Create and persist a fresh token pair, returned as a dict."""
    access_token = _make_access_token(user)
    refresh_data = _make_refresh_token(user)
    db.add(RefreshToken(user_id=user.id, token=refresh_data["token"], expires_at=refresh_data["expires_at"]))
    db.commit()
    return {"accessToken": access_token, "refreshToken": refresh_data["token"]}

# ─────────────────────────────────────────────
# Register
# ─────────────────────────────────────────────
async def register(body: RegisterSchema, db: Session):
    if db.query(User).filter(func.lower(User.username) == body.username.lower()).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists.")

    if db.query(User).filter(func.lower(User.email) == body.email.lower()).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists.")

    role = db.query(Role).filter(Role.name == "User").first()
    if not role:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Default role not configured.")

    user = User(
        username=body.username,
        email=body.email.lower(),
        hashed_password=_hash_password(body.password),
        role_id=role.id,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    try:
        await send_welcome_email(email=user.email, username=user.username)
    except Exception:
        logger.exception("Welcome email failed for %s", user.email)

    return {"status": "success", "message": "Registration successful."}

# ─────────────────────────────────────────────
# Login  (username/email + password)
# ─────────────────────────────────────────────
def login(body: LoginSchema, db: Session):
    user = db.query(User).filter(
        or_(
            func.lower(User.email) == body.username_or_email.lower(),
            func.lower(User.username) == body.username_or_email.lower(),
        )
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account deactivated. Contact support."
        )

    if not _verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials."
        )

    # Single active session
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user.id
    ).delete(synchronize_session=False)

    db.commit()

    return _issue_tokens(user, db)

# ─────────────────────────────────────────────
# Forgot Password  — sends a reset link via email
# ─────────────────────────────────────────────
async def forgot_password(body: ForgotPasswordSchema, db: Session):
    user = db.query(User).filter(func.lower(User.email) == body.email.lower()).first()
    if not user or not user.is_active:
        return {"status": "success", "message": "If that email is registered you will receive a reset link shortly."}

    exp = _utcnow() + timedelta(minutes=15)
    reset_token = jwt.encode(
        {"_id": str(user.id), "scope": "reset_password", "exp": exp},
        settings.ACCESS_TOKEN_SECRET,
        algorithm=settings.ALGORITHM,
    )
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

    try:
        await send_reset_password_email(email=user.email, username=user.username, reset_link=reset_link)
    except Exception:
        logger.exception("Reset email failed for %s", user.email)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send email. Try again.")

    return {"status": "success", "message": "Password reset link sent. It expires in 15 minutes."}

# ─────────────────────────────────────────────
# Reset Password  (consumes the reset link token)
# ─────────────────────────────────────────────
def reset_password(token: str, body: ResetPasswordSchema, db: Session):
    payload = _decode_token(token, settings.ACCESS_TOKEN_SECRET)

    if payload.get("scope") != "reset_password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token scope."
        )

    user = db.query(User).filter(
        User.id == payload.get("_id")
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    user.hashed_password = _hash_password(body.new_password)

    # Revoke all sessions
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user.id
    ).delete(synchronize_session=False)

    db.commit()

    return {
        "status": "success",
        "message": "Password reset successfully."
    }

# ─────────────────────────────────────────────
# Login with OTP  — step 1: request OTP
# ─────────────────────────────────────────────
async def send_otp(body: LoginWithOtpRequest, db: Session):
    user = _get_user_or_404(db, body.email)

    otp = _generate_otp()
    expiry = _utcnow() + timedelta(minutes=10)

    db.query(LoginOtp).filter(LoginOtp.user_id == user.id).delete()
    db.add(LoginOtp(user_id=user.id, otp=otp, expires_at=expiry))
    db.commit()

    try:
        await send_login_otp_email(email=user.email, username=user.username, otp=otp)
    except Exception:
        logger.exception("OTP email failed for %s", user.email)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send OTP. Try again.")

    return {"status": "success", "message": "OTP sent. It expires in 10 minutes."}

# ─────────────────────────────────────────────
# Login with OTP  — step 2: verify OTP → issue tokens
# ─────────────────────────────────────────────
def verify_otp(body: VerifyOtpRequest, db: Session):
    user = _get_user_or_404(db, body.email)

    otp_record: LoginOtp | None = (
        db.query(LoginOtp)
        .filter(LoginOtp.user_id == user.id)
        .first()
    )

    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No OTP found. Please request a new one."
        )

    if _utcnow() > otp_record.expires_at:
        db.delete(otp_record)
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP expired. Please request a new one."
        )

    if otp_record.otp != body.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP."
        )

    # Delete OTP
    db.delete(otp_record)

    # Single active session
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user.id
    ).delete(synchronize_session=False)

    db.commit()

    return _issue_tokens(user, db)

# ─────────────────────────────────────────────
# Resend OTP
# ─────────────────────────────────────────────
async def resend_otp(body: LoginWithOtpRequest, db: Session):
    return await send_otp(body, db)

# ─────────────────────────────────────────────
# User Authenticated Or Not Check
# ─────────────────────────────────────────────
def is_authenticated(current_user: User) -> dict:
    return {
        "status": "authenticated",
        "user": {
            "id": str(current_user.id),
            "username": current_user.username,
            "email": current_user.email,
        }
    }
    
# ─────────────────────────────────────────────
# Generate New Refresh token and access token 
# ─────────────────────────────────────────────
async def generate_refresh_access_token(
    body: RefreshTokenRequest,
    db: Session
):
    try:
        payload = jwt.decode(
            body.refreshToken,
            settings.REFRESH_TOKEN_SECRET,
            algorithms=[settings.ALGORITHM],
        )

    except jwt.ExpiredSignatureError:

        db.query(RefreshToken).filter(
            RefreshToken.token == body.refreshToken
        ).delete(synchronize_session=False)

        db.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired."
        )

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token."
        )

    if payload.get("scope") != "refresh_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token scope."
        )

    stored_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == body.refreshToken
        )
        .first()
    )

    if not stored_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found."
        )

    user = (
        db.query(User)
        .filter(
            User.id == payload.get("_id")
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account deactivated."
        )

    if stored_token.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token."
        )

    # Revoke all old refresh tokens
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user.id
    ).delete(synchronize_session=False)

    db.commit()

    tokens = _issue_tokens(user, db)

    return {
        "status": "success",
        "message": "Token refreshed successfully.",
        "data": tokens
    }