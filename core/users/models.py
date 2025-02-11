from email.policy import default

from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timedelta
from sqlalchemy import String, Enum
from config import get_settings
from asyncdatabase import Base
import bcrypt
import enum
import jwt


class Role(enum.Enum):
    admin = 'admin'
    author = 'author'
    user = 'user'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String)
    role: Mapped[Enum] = mapped_column(Enum(Role), default=Role.user, nullable=False)

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
