from .services import create_user, login_user
from .schemas import UserCreate, UserLogin
from sqlalchemy.orm import Session
from dependencies import get_db
from fastapi import APIRouter
from fastapi import Depends

user_router = APIRouter()


@user_router.post('/signup')
def sing_up(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user(user_data, db)


@user_router.post('/login')
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    return login_user(user_data, db)
