import random

import allure
import pytest
import requests

@allure.feature("标签模块")
class TestTags:

    @allure.story("创建标签")
    @allure.title("正常创建")
    def test_add_tag_success_and_cleanIt(self, base_url, auth_url):
        suffix = random.randint(10000, 90000)
        name = f"test_tag_{suffix}"
        resp = requests.post(f"{base_url}/api/v1/tags{auth_url}", data={
            "name": name,
            "created_by": "test_admin",
            "state": 1
        })
        assert resp.status_code == 200
        assert resp.json()["code"] == 200

    @allure.story("创建标签")
    @allure.title("正常创建-不传state使用默认值")
    def test_add_tag_without_state_success(self, base_url, auth_url):
        suffix = random.randint(10000, 90000)
        name = f"test_tag_no_state_{suffix}"
        resp = requests.post(f"{base_url}/api/v1/tags{auth_url}", data={
            "name": name,
            "created_by": "test_admin"
        })
        assert resp.status_code == 200
        assert resp.json()["code"] == 200

    @allure.story("创建标签")
    @allure.title("重复名称创建")
    def test_add_tag_duplicate_name(self, base_url, auth_url):
        suffix = random.randint(10000, 90000)
        name = f"test_tag_dup_{suffix}"
        # 第一次创建
        requests.post(f"{base_url}/api/v1/tags{auth_url}", data={
            "name": name,
            "created_by": "test_admin",
            "state": 1
        })
        # 再次创建同名标签
        resp = requests.post(f"{base_url}/api/v1/tags{auth_url}", data={
            "name": name,
            "created_by": "test_admin",
            "state": 1
        })
        assert resp.status_code == 200
        assert resp.json()["code"] == 10001

    @allure.story("创建标签")
    @allure.title("name为空")
    def test_add_tag_name_empty(self, base_url, auth_url):
        resp = requests.post(f"{base_url}/api/v1/tags{auth_url}", data={
            "name": "",
            "created_by": "test_admin",
            "state": 1
        })
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("创建标签")
    @allure.title("created_by为空")
    def test_add_tag_created_by_empty(self, base_url, auth_url):
        suffix = random.randint(10000, 90000)
        name = f"test_tag_{suffix}"
        resp = requests.post(f"{base_url}/api/v1/tags{auth_url}", data={
            "name": name,
            "created_by": "",
            "state": 1
        })
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("创建标签")
    @allure.title("不带Token")
    def test_add_tag_without_token(self, base_url):
        suffix = random.randint(10000, 90000)
        name = f"test_tag_{suffix}"
        resp = requests.post(f"{base_url}/api/v1/tags", data={
            "name": name,
            "created_by": "test_admin",
            "state": 1
        })
        assert resp.status_code == 401
        assert resp.json()["code"] == 400

    @allure.story("创建标签")
    @allure.title("Token伪造或过期")
    def test_add_tag_invalid_token(self, base_url):
        suffix = random.randint(10000, 90000)
        name = f"test_tag_{suffix}"
        resp = requests.post(f"{base_url}/api/v1/tags?token=invalid_token_string", data={
            "name": name,
            "created_by": "test_admin",
            "state": 1
        })
        assert resp.status_code == 401
        assert resp.json()["code"] == 20001

    @allure.story("创建标签")
    @allure.title("state传非法值")
    def test_add_tag_invalid_state(self, base_url, auth_url):
        suffix = random.randint(10000, 90000)
        name = f"test_tag_{suffix}"
        resp = requests.post(f"{base_url}/api/v1/tags{auth_url}", data={
            "name": name,
            "created_by": "test_admin",
            "state": 999
        })
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("创建标签")
    @allure.title("name刚好100字符")
    def test_add_tag_name_boundary_100(self, base_url, auth_url):
        suffix = random.randint(10000, 90000)
        name = f"{'a' * (99 - len(str(suffix)))}_{suffix}"
        assert len(name) == 100
        resp = requests.post(f"{base_url}/api/v1/tags{auth_url}", data={
            "name": name,
            "created_by": "test_admin",
            "state": 1
        })
        assert resp.status_code == 200
        assert resp.json()["code"] == 200

    @allure.story("创建标签")
    @allure.title("name超过100字符")
    def test_add_tag_name_over_100(self, base_url, auth_url):
        suffix = random.randint(10000, 90000)
        name = f"{'a' * (100 - len(str(suffix)))}_{suffix}"
        assert len(name) == 101
        resp = requests.post(f"{base_url}/api/v1/tags{auth_url}", data={
            "name": name,
            "created_by": "test_admin",
            "state": 1
        })
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("创建标签")
    @allure.title("created_by刚好100字符")
    def test_add_tag_created_by_boundary_100(self, base_url, auth_url):
        suffix = random.randint(10000, 90000)
        name = f"test_tag_{suffix}"
        created_by = "a" * 100
        resp = requests.post(f"{base_url}/api/v1/tags{auth_url}", data={
            "name": name,
            "created_by": created_by,
            "state": 1
        })
        assert resp.status_code == 200
        assert resp.json()["code"] == 200



    @allure.story("获取标签列表")
    @allure.title("正常获取-不带筛选")
    def test_get_tags_without_filter(self, base_url, auth_url):
        resp = requests.get(f"{base_url}/api/v1/tags{auth_url}")
        assert resp.status_code == 200
        assert resp.json()["code"] == 200
        data = resp.json()["data"]
        assert "lists" in data
        assert "total" in data
        assert isinstance(data["lists"], list)
        assert isinstance(data["total"], int)

    @allure.story("获取标签列表")
    @allure.title("不带Token")
    def test_get_tags_without_token(self, base_url):
        resp = requests.get(f"{base_url}/api/v1/tags")
        assert resp.status_code == 401
        assert resp.json()["code"] == 400

    @allure.story("获取标签列表")
    @allure.title("Token伪造")
    def test_get_tags_invalid_token(self, base_url):
        resp = requests.get(f"{base_url}/api/v1/tags?token=invalid")
        assert resp.status_code == 401
        assert resp.json()["code"] == 20001

    @allure.story("获取标签列表")
    @allure.title("按name筛选")
    def test_get_tags_by_name(self, base_url, auth_url):
        suffix = random.randint(10000, 90000)
        name = f"test_filter_tag_{suffix}"
        requests.post(f"{base_url}/api/v1/tags{auth_url}", data={
            "name": name,
            "created_by": "test_admin",
            "state": 1
        })
        resp = requests.get(f"{base_url}/api/v1/tags{auth_url}&name={name}")
        assert resp.status_code == 200
        assert resp.json()["code"] == 200
        data = resp.json()["data"]
        assert data["total"] >= 1
        for tag in data["lists"]:
            assert tag["name"] == name

    @allure.story("获取标签列表")
    @allure.title("按name筛选-不存在的标签")
    def test_get_tags_by_nonexistent_name(self, base_url, auth_url):
        resp = requests.get(f"{base_url}/api/v1/tags{auth_url}&name=NoSuchTag99999")
        assert resp.status_code == 200
        assert resp.json()["code"] == 200
        data = resp.json()["data"]
        assert data["total"] == 0
        assert len(data["lists"]) == 0

    @allure.story("获取标签列表")
    @allure.title("按state=1筛选")
    def test_get_tags_by_state_active(self, base_url, auth_url):
        suffix = random.randint(10000, 90000)
        name = f"test_state1_tag_{suffix}"
        requests.post(f"{base_url}/api/v1/tags{auth_url}", data={
            "name": name,
            "created_by": "test_admin",
            "state": 1
        })
        resp = requests.get(f"{base_url}/api/v1/tags{auth_url}&state=1")
        assert resp.status_code == 200
        assert resp.json()["code"] == 200
        data = resp.json()["data"]
        assert isinstance(data["lists"], list)
        for tag in data["lists"]:
            assert tag["state"] == 1

    @allure.story("获取标签列表")
    @allure.title("按state=0筛选")
    def test_get_tags_by_state_inactive(self, base_url, auth_url):
        suffix = random.randint(10000, 90000)
        name = f"test_state0_tag_{suffix}"
        requests.post(f"{base_url}/api/v1/tags{auth_url}", data={
            "name": name,
            "created_by": "test_admin",
            "state": 0
        })
        resp = requests.get(f"{base_url}/api/v1/tags{auth_url}&state=0")
        assert resp.status_code == 200
        assert resp.json()["code"] == 200
        data = resp.json()["data"]
        assert isinstance(data["lists"], list)
        for tag in data["lists"]:
            assert tag["state"] == 0

    @allure.story("获取标签列表")
    @allure.title("按name和state组合筛选")
    def test_get_tags_by_name_and_state(self, base_url, auth_url):
        suffix = random.randint(10000, 90000)
        name = f"test_combined_tag_{suffix}"
        requests.post(f"{base_url}/api/v1/tags{auth_url}", data={
            "name": name,
            "created_by": "test_admin",
            "state": 1
        })
        resp = requests.get(f"{base_url}/api/v1/tags{auth_url}&name={name}&state=1")
        assert resp.status_code == 200
        assert resp.json()["code"] == 200
        data = resp.json()["data"]
        assert data["total"] >= 1
        for tag in data["lists"]:
            assert tag["name"] == name
            assert tag["state"] == 1

    def _create_tag(self, base_url, auth_url):
        suffix = random.randint(10000, 90000)
        name = f"test_edit_tag_{suffix}"
        resp = requests.post(f"{base_url}/api/v1/tags{auth_url}", data={
            "name": name,
            "created_by": "test_admin",
            "state": 1
        })
        assert resp.status_code == 200
        assert resp.json()["code"] == 200

        # 从列表中查询获取刚创建标签的ID
        resp = requests.get(f"{base_url}/api/v1/tags{auth_url}&name={name}")
        assert resp.status_code == 200
        assert resp.json()["code"] == 200
        data = resp.json()["data"]
        assert data["total"] >= 1
        return data["lists"][0]["id"], name

    @allure.story("更新标签")
    @allure.title("正常更新")
    def test_edit_tag_success(self, base_url, auth_url):
        tag_id, _ = self._create_tag(base_url, auth_url)
        resp = requests.put(f"{base_url}/api/v1/tags/{tag_id}{auth_url}", data={
            "name": f"updated_name_{random.randint(10000,90000)}",
            "modified_by": "test_admin",
            "state": 1
        })
        assert resp.status_code == 200
        assert resp.json()["code"] == 200

    @allure.story("更新标签")
    @allure.title("更新不存在的ID")
    def test_edit_tag_not_exist(self, base_url, auth_url):
        resp = requests.put(f"{base_url}/api/v1/tags/99999{auth_url}", data={
            "name": f"updated_name_{random.randint(10000,90000)}",
            "modified_by": "test_admin",
            "state": 1
        })
        assert resp.status_code == 200
        assert resp.json()["code"] == 10003

    @allure.story("更新标签")
    @allure.title("ID为负数")
    def test_edit_tag_negative_id(self, base_url, auth_url):
        resp = requests.put(f"{base_url}/api/v1/tags/-1{auth_url}", data={
            "name": f"updated_name_{random.randint(10000,90000)}",
            "modified_by": "test_admin",
            "state": 1
        })
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("更新标签")
    @allure.title("ID为非数字")
    def test_edit_tag_non_numeric_id(self, base_url, auth_url):
        resp = requests.put(f"{base_url}/api/v1/tags/abc{auth_url}", data={
            "name": f"updated_name_{random.randint(10000,90000)}",
            "modified_by": "test_admin",
            "state": 1
        })
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("更新标签")
    @allure.title("name为空")
    def test_edit_tag_name_empty(self, base_url, auth_url):
        tag_id, _ = self._create_tag(base_url, auth_url)
        resp = requests.put(f"{base_url}/api/v1/tags/{tag_id}{auth_url}", data={
            "name": "",
            "modified_by": "test_admin",
            "state": 1
        })
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("更新标签")
    @allure.title("modified_by为空")
    def test_edit_tag_modified_by_empty(self, base_url, auth_url):
        tag_id, _ = self._create_tag(base_url, auth_url)
        resp = requests.put(f"{base_url}/api/v1/tags/{tag_id}{auth_url}", data={
            "name": f"updated_name_{random.randint(10000,90000)}",
            "modified_by": "",
            "state": 1
        })
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("更新标签")
    @allure.title("不带Token")
    def test_edit_tag_without_token(self, base_url):
        resp = requests.put(f"{base_url}/api/v1/tags/1", data={
            "name": f"updated_name_{random.randint(10000,90000)}",
            "modified_by": "test_admin",
            "state": 1
        })
        assert resp.status_code == 401
        assert resp.json()["code"] == 400

    @allure.story("更新标签")
    @allure.title("name刚好100字符")
    def test_edit_tag_name_boundary_100(self, base_url, auth_url):
        tag_id, _ = self._create_tag(base_url, auth_url)
        suffix = random.randint(10000, 90000)
        name = f"{'a' * (99 - len(str(suffix)))}_{suffix}"
        assert len(name) == 100
        resp = requests.put(f"{base_url}/api/v1/tags/{tag_id}{auth_url}", data={
            "name": name,
            "modified_by": "test_admin",
            "state": 1
        })
        assert resp.status_code == 200
        assert resp.json()["code"] == 200

    @allure.story("删除标签")
    @allure.title("正常删除")
    def test_delete_tag_success(self, base_url, auth_url):
        tag_id, _ = self._create_tag(base_url, auth_url)
        resp = requests.delete(f"{base_url}/api/v1/tags/{tag_id}{auth_url}")
        assert resp.status_code == 200
        assert resp.json()["code"] == 200

    @allure.story("删除标签")
    @allure.title("删除不存在的ID")
    def test_delete_tag_not_exist(self, base_url, auth_url):
        resp = requests.delete(f"{base_url}/api/v1/tags/99999{auth_url}")
        assert resp.status_code == 200
        assert resp.json()["code"] == 10003

    @allure.story("删除标签")
    @allure.title("ID为负数")
    def test_delete_tag_negative_id(self, base_url, auth_url):
        resp = requests.delete(f"{base_url}/api/v1/tags/-1{auth_url}")
        print(resp.text)
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("删除标签")
    @allure.title("重复删除同一个ID")
    def test_delete_tag_twice(self, base_url, auth_url):
        tag_id, _ = self._create_tag(base_url, auth_url)
        # 第一次删除
        resp = requests.delete(f"{base_url}/api/v1/tags/{tag_id}{auth_url}")
        assert resp.status_code == 200
        assert resp.json()["code"] == 200
        # 第二次删除同一个ID
        resp = requests.delete(f"{base_url}/api/v1/tags/{tag_id}{auth_url}")
        assert resp.status_code == 200
        assert resp.json()["code"] == 10003

    @allure.story("删除标签")
    @allure.title("不带Token")
    def test_delete_tag_without_token(self, base_url):
        resp = requests.delete(f"{base_url}/api/v1/tags/1")
        assert resp.status_code == 401
        assert resp.json()["code"] == 400

    @allure.story("删除标签")
    @allure.title("验证软删除")
    def test_delete_tag_soft_delete(self, base_url, auth_url):
        tag_id, name = self._create_tag(base_url, auth_url)
        # 删除前可查到
        resp = requests.get(f"{base_url}/api/v1/tags{auth_url}&name={name}")
        assert resp.status_code == 200
        assert resp.json()["data"]["total"] >= 1

        # 执行删除
        resp = requests.delete(f"{base_url}/api/v1/tags/{tag_id}{auth_url}")
        assert resp.status_code == 200
        assert resp.json()["code"] == 200

        # 删除后列表中查不到
        resp = requests.get(f"{base_url}/api/v1/tags{auth_url}&name={name}")
        assert resp.status_code == 200
        assert resp.json()["code"] == 200
        assert resp.json()["data"]["total"] == 0
        assert len(resp.json()["data"]["lists"]) == 0

    @allure.story("删除标签")
    @allure.title("ID为非数字")
    def test_delete_tag_non_numeric_id(self, base_url, auth_url):
        resp = requests.delete(f"{base_url}/api/v1/tags/abc{auth_url}")
        assert resp.status_code == 400
        assert resp.json()["code"] == 400



