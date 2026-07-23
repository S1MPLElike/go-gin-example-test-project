import allure
import pytest
import requests

@allure.feature("认证模块")
class TestAuth:

    @allure.story("用户登录")
    @allure.title("正确用户名和密码---登录成功")
    def test_login_success(self, base_url):
        resp = requests.post(f"{base_url}/auth",data={
            "username":"test",
            "password":"test123"
        })
        assert resp.status_code == 200
        assert resp.json()["code"] == 200
        assert resp.json()["data"]["token"] is not None

    @allure.story("用户登录")
    @allure.title("仅密码错误---登录失败")
    def test_login_worth_password(self, base_url):
        resp = requests.post(f"{base_url}/auth",data={
            "username":"test",
            "password":"worth_password"
        })
        assert resp.status_code == 401
        assert resp.json()["code"] == 20004
        assert resp.json()["data"] is None

    @allure.story("用户登录")
    @allure.title("用户名不存在")
    def test_login_nonexistent_user(self, base_url):
        resp = requests.post(f"{base_url}/auth",data={
            "username":"test111",
            "password":"123456"
        })
        assert resp.status_code == 401
        assert resp.json()["code"] == 20004
        assert resp.json()["data"] is None

    @allure.story("用户登录")
    @allure.title("用户名为空")
    def test_login_non_username(self, base_url):
        resp = requests.post(f"{base_url}/auth",data={
            "username":"",
            "password":"test123"
        })
        assert resp.status_code == 400
        assert resp.json()["code"] == 400
        assert resp.json()["msg"] == "请求参数错误"


    @allure.story("用户登录")
    @allure.title("密码为空")
    def test_login_non_password(self, base_url):
        resp = requests.post(f"{base_url}/auth",data={
            "username":"test",
            "password":""
        })
        assert resp.status_code == 400
        assert resp.json()["code"] == 400
        assert resp.json()["data"] is None