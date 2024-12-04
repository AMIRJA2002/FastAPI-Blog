from core.users.bearer import JWTBearer
from core.users.utils import settings
from core.users.models import User
from fastapi import HTTPException
from datebase import SessionLocal
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


def get_current_user(token: str = Depends(JWTBearer())) -> User:
    try:
        payload = jwt.decode(token, f'{settings.SECRET_KEY}', algorithms=['HS256'])
        user_id = payload.get('sub')
        db = SessionLocal()
        return db.query(User).filter(User.id == user_id).first()
    except(jwt.PyJWTError, AttributeError):
        raise HTTPException(status_code="Invalid Token")
