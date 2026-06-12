from fastapi import FastAPI, APIRouter #type: ignore
import src.models
from src.controllers import user_controller, role_controller, chat_controller, auth_controller

from src.utils.rate_limiting import limiter
from slowapi.errors import RateLimitExceeded #type: ignore  
from slowapi import _rate_limit_exceeded_handler #type: ignore
from slowapi.middleware import SlowAPIMiddleware #type: ignore

app = FastAPI()

# Register limiter
app.state.limiter = limiter

# Register exception handler
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

# Add middleware
app.add_middleware(SlowAPIMiddleware)

app.include_router(user_controller.router, prefix = "/users", tags=["Users"])
app.include_router(role_controller.router, prefix = "/roles", tags=["Roles"])
app.include_router(chat_controller.router, prefix="/chat", tags=["Chats"])
app.include_router(auth_controller.router, prefix="/auth", tags=["auth"])
