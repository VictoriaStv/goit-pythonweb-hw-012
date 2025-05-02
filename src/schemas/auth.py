from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    confirmed: bool
    avatar: str | None = None
    role: str   

class Config:
    from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class RequestPasswordReset(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)

class RefreshTokenRequest(BaseModel):
    refresh_token: str
