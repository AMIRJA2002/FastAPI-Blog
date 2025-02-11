from .schemas import UserCreate, UserLogin, Token
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import exists
from fastapi import HTTPException
from sqlalchemy import or_
from .models import User


async def create_user(user_data: UserCreate, db: AsyncSession) -> dict:
    query = select(exists().where(
        or_(
            User.username == user_data.username,
            User.email == user_data.email
        )
    ))
    result = await db.execute(query)
    user_exists = result.scalar()

    if user_exists:
        raise HTTPException(status_code=400, detail="username of email already exists")

    user = User(username=user_data.username, email=user_data.email, role=user_data.role)
    user.hash_password(user_data.password)
    db.add(user)
    await db.commit()
    return {'data': 'user has been created'}


async def login_user(user_data: UserLogin, db: AsyncSession) -> Token:
    query = select(User).where(User.username == user_data.username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user is None or not user.verify_password(user_data.password):
        raise HTTPException(status_code=401, detail='invalid username or password')

    token = user.generate_token()
    return Token(access_token=token, token_type='bearer')
