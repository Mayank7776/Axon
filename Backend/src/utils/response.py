from typing import Generic, TypeVar
from pydantic import BaseModel #type: ignore

T = TypeVar("T")

class Response(BaseModel, Generic[T]):
    success: bool
    message: str
    data: T | None = None