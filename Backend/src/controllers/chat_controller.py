from src.schemas.chat_message_schema import SendMessageRequest
from src.schemas.chat_session_schema import *
from fastapi import APIRouter, Depends, Request, status #type: ignore
from src.core.db import get_db
from sqlalchemy.orm import Session #type: ignore
from src.utils.rate_limiting import limiter
from src.services.chat_service import (
    # session
    get_session_by_id,
    create_session,
    delete_session_by_id,
    update_session_title,
    get_all_sessions,
    # message
    send_message,
    get_messages_by_session_id
    )

router = APIRouter()

#  Session CRUD ----------------------------------------------------------------------------------------------------------------
@router.get("/sessions")
@limiter.limit("20/minute")
async def get_all_chat_sessions(
    request: Request,
    user_id: str,
    db: Session = Depends(get_db)
):
    return get_all_sessions(
        db=db,
        user_id=user_id
    )

@router.get("/sessions/{session_id}")
@limiter.limit("20/minute")
async def get_session(
    request: Request,
    session_id: str,
    db: Session = Depends(get_db)
):
    return get_session_by_id(
        db=db,
        session_id=session_id
    )
    

@router.post("/sessions")
@limiter.limit("10/minute")
async def add_session(
    request: Request,
    payload: CreateSessionRequest,
    db: Session = Depends(get_db),
):
    return create_session(
        db=db,
        payload=payload
    )
    
@router.patch("/sessions/{session_id}")
@limiter.limit("10/minute")
async def update_chat_session(
    request: Request,
    session_id: str,
    body: UpdateSessionTitle,
    db: Session = Depends(get_db)
):
    return update_session_title(
        db=db,
        session_id=session_id,
        title=body.title
    )
    
@router.delete("/sessions/{session_id}")
@limiter.limit("50/minute")
async def delete_chat_session(
    request: Request,
    session_id: str,
    db: Session = Depends(get_db)
):
    return delete_session_by_id(
        db=db,
        session_id=session_id
    )
    
# Message related to a Particular Session CRUD ------------------------------------------------------------------------------------------------

@router.get("/sessions/{session_id}/messages")
@limiter.limit("30/minute")
async def get_messages(
    request: Request,
    session_id: str,
    db: Session = Depends(get_db)
):
    return get_messages_by_session_id(
        db=db,
        session_id=session_id
    )


@router.post("/messages")
@limiter.limit("5/minute")
async def add_message(
    request: Request,
    payload: SendMessageRequest,
    db: Session = Depends(get_db)
):
    return send_message(
        db=db,
        payload=payload
    )