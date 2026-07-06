import jwt #type:ignore
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError #type:ignore

from fastapi import Depends, HTTPException, status, Request #type:ignore
from sqlalchemy.orm import Session #type:ignore

from src.modules.users.models import User
from src.core.settings import settings 
from src.core.db import get_db


def validateToken(req: Request, db: Session = Depends(get_db)) -> User:
    token = req.headers.get("Authorization")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing.",
        )

    try:
        token = token.split(" ")[1]
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Expected: Bearer <token>",
        )

    try:
        data = jwt.decode(token, settings.ACCESS_TOKEN_SECRET, algorithms=[settings.ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token has expired.",
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )

    user_id = data.get("_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload.",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account deactivated. Contact support.",
        )

    return user