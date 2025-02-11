from .services import create_user, login_user
from .schemas import UserCreate, UserLogin
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db, aget_db
from fastapi import APIRouter
from fastapi import Depends

user_router = APIRouter()


@user_router.post('/signup')
async def sing_up(user_data: UserCreate, db: AsyncSession = Depends(aget_db)):
    return await create_user(user_data, db)


@user_router.post('/login')
async def login(user_data: UserLogin, db: AsyncSession = Depends(aget_db)):
    return await login_user(user_data, db)
