from fastapi import FastAPI, APIRouter #type: ignore
from src.modules.users.router import router as user_router
from src.modules.roles.router import router as role_router
from src.modules.chat.router import router as chat_router
from src.modules.auth.router import router as auth_router
from src.modules.workouts.routers.muscles_router import router as muscles_router
from src.modules.workouts.routers.myworkout_router import router as myworkout_router
from src.modules.blogs.router import router as blogs_router
from src.modules.notifications.router import router as notification_router

from src.utils.rate_limiting import limiter
from slowapi.errors import RateLimitExceeded #type: ignore  
from slowapi import _rate_limit_exceeded_handler #type: ignore
from slowapi.middleware import SlowAPIMiddleware #type: ignore
from src.core import cloudinary  # executes config

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

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(role_router, prefix="/roles", tags=["Roles"])
app.include_router(chat_router, prefix="/chat", tags=["Chats"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(muscles_router, prefix="/musclegroup", tags=["Musclesgroup"])
app.include_router(myworkout_router, prefix="/workout", tags=["My-Workouts"])
app.include_router(blogs_router, prefix="/blogs", tags=["Blogs"])
app.include_router(notification_router, prefix="/notifications", tags=["Notifications"])