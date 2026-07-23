import pytest
import requests
import random

@pytest.fixture(scope="session")
def base_url():
    return "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def auth_token(base_url):
    """整个测试会话只登录一次，拿 Token"""
    # 登录拿 Token
    resp = requests.post(f"{base_url}/auth", data={
        "username": "test",
        "password": "test123"
    })
    return resp.json()["data"]["token"]

@pytest.fixture
def auth_url(auth_token):
    """所有需要鉴权的接口用这个拼 URL"""
    return f"?token={auth_token}"

@pytest.fixture
def created_tag(base_url, auth_url):
    """创建一个标签，用例执行后自动软删除"""
    suffix = random.randint(10000, 90000)
    name = f"fixture_tag_{suffix}"
    resp = requests.post(f"{base_url}/api/v1/tags{auth_url}", data={
        "name": name,
        "created_by": "fixture_admin",
        "state": 1
    })
    assert resp.status_code == 200
    assert resp.json()["code"] == 200

    # 通过列表接口查询刚创建的标签ID
    resp = requests.get(f"{base_url}/api/v1/tags{auth_url}&name={name}")
    assert resp.status_code == 200
    assert resp.json()["code"] == 200
    tag = resp.json()["data"]["lists"][0]

    yield tag

    # 用例结束后清理（软删除）
    requests.delete(f"{base_url}/api/v1/tags/{tag['id']}{auth_url}")