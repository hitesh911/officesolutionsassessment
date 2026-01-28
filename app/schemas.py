from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    user_id: int
    title: str
    content: str

class PostOut(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
