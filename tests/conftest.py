from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app.models import *
from alembic import command
import pytest


# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Earlfrosh@localhost:5432/fastapi_social_app_test'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    """command.downgrade("base")
    command.upgrade("head")"""
    db = TestingSessionLocal()
    try:
        yield db

    finally:
        db.close()


@pytest.fixture
def client(session):
    # run our code before our test
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
    # run our code after our test finishes


@pytest.fixture
def test_user(client):
    user_data = {
        "email": "ezsdev@gmail.com",
        "password": "password234",
        "phone_number": "4638373837",
    }
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {
        "email": "ezsdev0@gmail.com",
        "password": "password234",
        "phone_number": "4638373837",
    }
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"bearer {token}",
    }

    return client


@pytest.fixture
def test_posts(test_user, client, session, test_user2):
    posts_data = [
        {
            "title": "First test post",
            "content": "This is a first test content",
            "owner_id": test_user["id"],
        },
        {
            "title": "Second test post",
            "content": "This is a second test content",
            "owner_id": test_user["id"],
        },
        {
            "title": "Third test post",
            "content": "This is a third test content",
            "owner_id": test_user["id"],
        },
        {
            "title": "Fourth test post",
            "content": "This is a fourth test content",
            "owner_id": test_user2["id"],
        },
    ]

    def create_post_model(post):
        return Post(**post)

    post_map = map(create_post_model, posts_data)

    posts = list(post_map)
    print(posts)
    session.add_all(posts)
    session.commit()
    posts = session.query(Post).all()
    return posts


@pytest.fixture
def test_vote(session, authorized_client, test_posts, test_user):
    print(test_posts[0].id)
    new_vote = Vote(post_id=test_posts[0].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()
    return new_vote


@pytest.fixture
def test_comments(session, client, test_posts, test_user, test_user2):
    comments_data = [
        {
            "comment": "This is the first comment test",
            "user_id": test_user2["id"],
            "post_id": test_posts[0].id,
        },
        {
            "comment": "This is the second comment test",
            "user_id": test_user2["id"],
            "post_id": test_posts[1].id,
        },
        {
            "comment": "This is the third comment test",
            "user_id": test_user["id"],
            "post_id": test_posts[0].id,
        },
        {
            "comment": "This is the fourth comment test",
            "user_id": test_user["id"],
            "post_id": test_posts[1].id,
        },
    ]
    def create_comments_model(comment):
        return Comment(**comment)
    comment_map = map(create_comments_model, comments_data)
    comments = list(comment_map)
    session.add_all(comments)
    session.commit()
    comments = session.query(Comment).all()
    return comments
    