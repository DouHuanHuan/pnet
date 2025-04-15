import pytest
from fastapi.testclient import TestClient
from sqlmodel import select

from main import app
from models import User
from utils.auth import hash_password
from utils.database import init_db, get_session


@pytest.fixture(scope="module")
def test_db():
    # 初始化数据库
    init_db()
    yield get_session()


@pytest.fixture
def client():
    return TestClient(app)


def test_register(client, test_db):
    username = "testuser"
    password = "testpassword"

    # 请求注册接口
    response = client.post(
        "/register/",
        json={"username": username, "password": password}
    )

    assert response.status_code == 201
    assert response.json()["username"] == username
    assert response.json()["id"] is not None
    assert "url" in response.json()

    # 检查数据库中是否有该用户
    user_in_db = test_db.exec(select(User).where(User.username == username)).first()
    assert user_in_db is not None
    assert user_in_db.username == username


def test_register_existing_user(client, test_db):
    # 先创建一个用户
    username = "existinguser"
    password = "testpassword"
    hashed_password = hash_password(password)
    new_user = User(username=username, hashed_password=hashed_password)
    test_db.add(new_user)
    test_db.commit()

    # 尝试再次注册该用户
    response = client.post(
        "/register/",
        json={"username": username, "password": password}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"
