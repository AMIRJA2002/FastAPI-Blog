from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import get_settings

settings = get_settings()
from sqlalchemy.engine.url import URL
from sqlalchemy.pool import NullPool

engine = create_async_engine(settings.DATABASE_URL,
                             echo=False,
                             poolclass=NullPool,
                             # pool_size=pool_size
                             )

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


SessionLocal = async_sessionmaker(engine,
                             autocommit=False,
                             future=True,
                             expire_on_commit=False,
                             class_=AsyncSession)

class Base(DeclarativeBase):
    pass
