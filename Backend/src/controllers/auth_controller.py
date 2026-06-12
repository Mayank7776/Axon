from fastapi import APIRouter, Depends, Query, Request  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from src.core.db import get_db
from src.controllers.dependency.auth_dependency import validateToken
from src.models.user_model import User
from src.utils.rate_limiting import limiter
from src.schemas.auth_schema import (
    RefreshTokenRequest,
    RegisterSchema,
    LoginSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
    LoginWithOtpRequest,
    VerifyOtpRequest,
)
import src.services.auth_service as auth_svc

router = APIRouter()


@router.post("/register")
@limiter.limit("5/minute")
async def register(request: Request, body: RegisterSchema, db: Session = Depends(get_db)):
    return await auth_svc.register(body, db)


@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, body: LoginSchema, db: Session = Depends(get_db)):
    return auth_svc.login(body, db)


@router.post("/forgot-password")
@limiter.limit("5/minute")
async def forgot_password(request: Request, body: ForgotPasswordSchema, db: Session = Depends(get_db)):
    return await auth_svc.forgot_password(body, db)


# token comes in as a query param from the email link: /reset-password?token=...
@router.post("/reset-password")
@limiter.limit("5/minute")
async def reset_password(
    request: Request,
    body: ResetPasswordSchema,
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    return auth_svc.reset_password(token, body, db)


@router.get("/is-authenticated")
async def is_authenticated(
    request: Request,
    current_user: User = Depends(validateToken),
):
    return auth_svc.is_authenticated(current_user)

# ── OTP flow ──────────────────────────────────────────────────────────────────

# Step 1 — request OTP (also used by /otp-resend)
@router.post("/otp-login")
@limiter.limit("5/minute")
async def otp_login(request: Request, body: LoginWithOtpRequest, db: Session = Depends(get_db)):
    return await auth_svc.send_otp(body, db)


# Step 2 — verify OTP and receive tokens
@router.post("/otp-verification")
@limiter.limit("5/minute")
async def verify_otp(request: Request, body: VerifyOtpRequest, db: Session = Depends(get_db)):
    return auth_svc.verify_otp(body, db)


# Resend — same logic as step 1, separate endpoint for rate-limit control
@router.post("/otp-resend")
@limiter.limit("3/minute")
async def resend_otp(request: Request, body: LoginWithOtpRequest, db: Session = Depends(get_db)):
    return await auth_svc.resend_otp(body, db)

@router.post("/refresh-token")
@limiter.limit("1/minute")
async def new_refresh_token(request: Request, body: RefreshTokenRequest, db: Session = Depends(get_db)):
    return await auth_svc.generate_refresh_access_token(body, db)
