from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str