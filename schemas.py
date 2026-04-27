from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# --- Auth schemas ---

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    token: str
    email: str


# --- File schemas ---

class FileOut(BaseModel):
    id: int
    name: str
    type: str
    size: int
    date: datetime

    class Config:
        from_attributes = True


class UnlockRequest(BaseModel):
    password: str


class UnlockResponse(BaseModel):
    success: bool


class MessageResponse(BaseModel):
    message: str
