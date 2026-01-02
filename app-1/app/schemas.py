# app/schemas.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    class Config:
        # orm_mode = True
        from_attributes = True

from pydantic import BaseModel

class AIModel(BaseModel):
    name: str
    framework: str 
    accuracy: float