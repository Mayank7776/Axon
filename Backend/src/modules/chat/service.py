from src.modules.users.models import User
from src.modules.chat.models import ChatSession
from src.modules.chat.models import ChatMessage
from src.modules.chat.schemas import CreateSessionRequest
from groq import Groq # type: ignore
from src.core.settings import settings
from src.utils.response import Response
from sqlalchemy.orm import Session #type: ignore

client = Groq(
    api_key=settings.GROQ_API_KEY
)

system_prompts = {
    "trainer": settings.TRAINER_SYSTEM_PROMPT,
    "nutrition": settings.NUTRITION_SYSTEM_PROMPT,
    "designer": settings.DESIGNER_SYSTEM_PROMPT
}

# Session CRUD --------------------------------------------------------------------
def create_session(db: Session, payload: CreateSessionRequest):
        user = db.query(User).filter(User.id == payload.user_id).first()
        if not user:
            return Response(
                success=False,
                message="User not found",
                data=None
            )

        session = ChatSession(
                    user_id=payload.user_id,
                    agent_type=payload.agent_type,
                    title=payload.title
                    )

        db.add(session)
        db.commit()
        db.refresh(session)

        return Response(
            success=True,
            message="Session created successfully",
            data={
                "id": session.id,
                "title": session.title,
                "agent_type": session.agent_type
            }
        )
        
def get_session_by_id(
    db: Session,
    session_id: str
):
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id)
        .first()
    )

    if not session:
        return Response(
            success=False,
            message="Session not found",
            data=None
        )

    return Response(
        success=True,
        message="Session retrieved successfully",
        data={
            "id": session.id,
            "title": session.title,
            "agent_type": session.agent_type
        }
    )
    
def update_session_title(
    db: Session,
    session_id: str,
    title: str
):
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id)
        .first()
    )

    if not session:
        return Response(
            success=False,
            message="Session not found",
            data=None
        )

    session.title = title

    db.commit()
    db.refresh(session)

    return Response(
        success=True,
        message="Session title updated successfully",
        data={
            "id": session.id,
            "title": session.title
        }
    )
    
def delete_session_by_id(
    db: Session,
    session_id: str
):
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id)
        .first()
    )

    if not session:
        return Response(
            success=False,
            message="Session not found",
            data=None
        )

    db.delete(session)
    db.commit()

    return Response(
        success=True,
        message="Session deleted successfully",
        data=None
    )
    
def get_all_sessions(
    db: Session,
    user_id: str
):
    sessions = (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user_id)
        .order_by(ChatSession.updated_at.desc())
        .all()
    )

    return Response(
        success=True,
        message="Sessions fetched successfully",
        data=[
            {
                "id": session.id,
                "title": session.title,
                "agent_type": session.agent_type
            }
            for session in sessions
        ]
    )
    
# Message CRUD -------------------------------------------------------------------------------

def get_messages_by_session_id(
    db: Session,
    session_id: str
):
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id)
        .first()
    )

    if not session:
        return Response(
            success=False,
            message="Session not found",
            data=None
        )

    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )

    return Response(
        success=True,
        message="Messages retrieved successfully",
        data=[
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at
            }
            for msg in messages
        ]
    )

def send_message(
    db: Session,
    payload
):

    # Check session exists
    session = (
        db.query(ChatSession)
        .filter(ChatSession.id == payload.session_id)
        .first()
    )

    if not session:
        return Response(
            success=False,
            message="Session not found",
            data=None
        )

    # Save user message
    user_message = ChatMessage(
        session_id=payload.session_id,
        role="user",
        content=payload.message
    )

    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    # Load conversation history
    history = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == payload.session_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )

    # Build prompt for Groq
    messages = [
        {
            "role": "system",
            "content": system_prompts.get(
                session.agent_type,
                "You are a helpful assistant."
            )
        }
    ]

    messages.extend(
        [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in history
        ]
    )

    try:

        completion = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=messages,
            temperature=0.7
        )

        assistant_response = (
            completion.choices[0]
            .message
            .content
        )

    except Exception as e:

        return Response(
            success=False,
            message=f"Groq error: {str(e)}",
            data=None
        )

    # Save assistant message
    assistant_message = ChatMessage(
        session_id=payload.session_id,
        role="assistant",
        content=assistant_response
    )

    db.add(assistant_message)

    # Touch session updated_at
    session.updated_at = session.updated_at

    db.commit()
    db.refresh(assistant_message)

    return Response(
        success=True,
        message="Message sent successfully",
        data={
            "message_id": assistant_message.id,
            "session_id": payload.session_id,
            "role": assistant_message.role,
            "content": assistant_message.content,
            "created_at": assistant_message.created_at
        }
    )