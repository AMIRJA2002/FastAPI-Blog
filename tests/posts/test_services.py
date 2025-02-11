import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app import app

from asyncdatabase import engine, Base
from core.users.models import User
from core.post.services import PostService, create_tag_service
from dependencies import get_current_user, aget_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

app.dependency_overrides[aget_db] = override_get_db


@pytest.mark.asyncio
async def test_create_post(client: AsyncClient, db_session: AsyncSession):
    user = User(id=1, username="testuser", role="admin")

    async def mock_get_current_user():
        return user

    app.dependency_overrides[get_current_user] = mock_get_current_user
    post_data = {
        "title": "Test Post",
        "content": "This is a test post",
        "tags": ["test", "fastapi"]
    }

    async def mock_get_db():
        return db_session

    app.dependency_overrides[aget_db] = mock_get_db


    async def mock_create_tag_service(tags, db):
        pass

    app.dependency_overrides[create_tag_service] = mock_create_tag_service


    response = await client.post("/posts", json=post_data)


    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["title"] == post_data["title"]
    assert response_data["content"] == post_data["content"]
    assert set(tag["name"] for tag in response_data["tags"]) == set(post_data["tags"])


@pytest.mark.asyncio
async def test_create_post_forbidden(client: AsyncClient, db_session: AsyncSession):

    user = User(id=1, username="testuser", role="user")


    async def mock_get_current_user():
        return user

    app.dependency_overrides[get_current_user] = mock_get_current_user


    post_data = {
        "title": "Test Post",
        "content": "This is a test post",
        "tags": ["test", "fastapi"]
    }


    async def mock_get_db():
        return db_session

    app.dependency_overrides[aget_db] = mock_get_db


    response = await client.post("/posts", json=post_data)


    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "You do not have permission for this action"
