from mako.compat import win32
from sqlalchemy import select

from core.users.bearer import JWTBearer
# from core.users.utils import settings
from core.users.models import User
from fastapi import HTTPException
from datebase import SessionLocal
from asyncdatabase import Base, engine, SessionLocal as aSessionLocal
from config import get_settings
from fastapi import Depends
import jwt

settings = get_settings()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def aget_db():
    async with aSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_current_user(token: str = Depends(JWTBearer())) -> User:
    try:
        payload = jwt.decode(token, f'{settings.SECRET_KEY}', algorithms=['HS256'])
        user_id = payload.get('sub')
        async with aSessionLocal() as session:
            query = select(User).where(User.id == int(user_id))
            result = await session.execute(query)
            user = result.scalars().first()
            return user
    except(jwt.PyJWTError, AttributeError):
        raise HTTPException(status_code=403, detail='Invalid Token')
