from .schemas import UserCreate, UserLogin, Token
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from fastapi import HTTPException
from sqlalchemy import or_
from .models import User


def create_user(user_data: UserCreate, db: Session) -> dict:
    user = db.query(exists().where(
        or_(
            User.username == user_data.username,
            User.email == user_data.email
        )
    )).scalar()

    if user:
        raise HTTPException(status_code=400, detail="username of email already exists")

    user = User(username=user_data.username, email=user_data.email, role=user_data.role)
    user.hash_password(user_data.password)
    db.add(user)
    db.commit()
    return {'data': 'user has been created'}


def login_user(user_data: UserLogin, db: Session) -> Token:
    user = db.query(User).filter(User.username == user_data.username).first()
    if user is None or not user.verify_password(user_data.password):
        raise HTTPException(status_code=401, detail='invalid username or password')

    token = user.generate_token()
    return Token(access_token=token, token_type='bearer')
