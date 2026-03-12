from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: str = "viewer"


class UserCreate(UserBase):
    password: str
    gram_panchayat_id: Optional[int] = None


class UserResponse(UserBase):
    id: int
    gram_panchayat_id: Optional[int]
    status: str
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    username: str
    password: str
