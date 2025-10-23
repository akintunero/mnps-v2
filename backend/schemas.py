from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: str
    role: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Student result schemas
class StudentResultBase(BaseModel):
    student_id: str
    student_name: str
    class_name: str
    session: str
    term: str
    subjects: str  # JSON string
    total_score: float
    average_score: float
    grade: str
    position: Optional[str] = None
    remarks: Optional[str] = None

class StudentResultCreate(StudentResultBase):
    pass

class StudentResultResponse(StudentResultBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Broadcast schemas
class BroadcastBase(BaseModel):
    title: str
    message: str
    priority: str = "normal"
    target_audience: str = "all"

class BroadcastCreate(BroadcastBase):
    pass

class BroadcastResponse(BroadcastBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
