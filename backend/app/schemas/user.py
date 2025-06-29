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
    id: int
    name: str
    email: EmailStr
    phone: str
    role: str

    class Config:
        orm_mode = True
