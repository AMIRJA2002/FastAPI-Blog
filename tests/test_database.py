from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datebase import Base
import pytest

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
