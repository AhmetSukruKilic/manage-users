from pydantic import BaseModel, EmailStr
from typing import Optional

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    
    class Config:
        from_attributes = True

class ErrorResponse(BaseModel):
    error: str

