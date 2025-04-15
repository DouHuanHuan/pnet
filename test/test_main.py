import pytest
from fastapi.testclient import TestClient

from main import app
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

    response = client.post(
        "/register/",
        params={"username": username, "password": password}
    )

    assert response.status_code == 201
    assert response.json()["username"] == username
    assert response.json()["id"] is not None
    assert "url" in response.json()


def test_login(client, test_db):
    username = "testuser"
    password = "testpassword"

    response = client.post(
        "/login/",
        params={"username": username, "password": password}
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    assert response.json()["expires_in"] == 3600
    assert response.json()["user"]["username"] == username
