
# --- Merged from schemas/chat_session_schema.py ---
from typing import Optional

from pydantic import BaseModel

class CreateSessionRequest(BaseModel):
    user_id : str
    agent_type: str
    title : Optional[str] = None
    
class UpdateSessionTitle(BaseModel):
    title: str


# --- Merged from schemas/chat_message_schema.py ---
from pydantic import BaseModel

class SendMessageRequest(BaseModel):
    session_id: str
    message: str
    
