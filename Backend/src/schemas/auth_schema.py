from pydantic import BaseModel, EmailStr, Field


class RegisterSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginSchema(BaseModel):
    username_or_email: str
    password: str


class ForgotPasswordSchema(BaseModel):
    email: EmailStr


class ResetPasswordSchema(BaseModel):
    new_password: str = Field(
        min_length=8,
        max_length=128
    )


class OtpSchema(BaseModel):
    otp: str = Field(
        min_length=6,
        max_length=6
    )
    
class LoginWithOtpRequest(BaseModel):
    email: str
    
class VerifyOtpRequest(BaseModel):
    email: str
    otp: str
    
class RefreshTokenRequest(BaseModel):
    refreshToken: str