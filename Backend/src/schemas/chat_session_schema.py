from typing import Optional

from pydantic import BaseModel

class CreateSessionRequest(BaseModel):
    user_id : str
    agent_type: str
    title : Optional[str] = None
    
class UpdateSessionTitle(BaseModel):
    title: str
