from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6)
    phone: str = Field(...)

class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

class UserResponse(BaseModel):
    user_id: int = Field(...)
    email: EmailStr = Field(...)

    class Config:
        orm_mode = True
