from pydantic import BaseModel
from typing import Optional
from .models import Role


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: Optional[Role] = Role.user


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
