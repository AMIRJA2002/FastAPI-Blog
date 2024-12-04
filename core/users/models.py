from sqlalchemy import Column, String, Integer, Enum
from datetime import datetime, timedelta
from config import get_settings
from datebase import Base
import bcrypt
import enum
import jwt


class Role(enum.Enum):
    admin = 'admin'
    author = 'author'
    user = 'user'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum(Role), default=Role.user, nullable=False)

    def hash_password(self, password: str):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password: str):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def generate_token(self):
        expiration = datetime.utcnow() + timedelta(hours=24)
        payload = {
            "sub": str(self.id),
            "exp": expiration,
        }
        return jwt.encode(payload, f'{get_settings().SECRET_KEY}', algorithm='HS256')
