import random

import allure
import pytest
import requests

@allure.feature("文章模块")
class TestArticles:

    def _create_tag(self, base_url, auth_url):
        suffix = random.randint(10000, 90000)
        name = f"test_article_tag_{suffix}"
        resp = requests.post(f"{base_url}/api/v1/tags{auth_url}", data={
            "name": name,
            "created_by": "test_admin",
            "state": 1
        })
        assert resp.status_code == 200
        assert resp.json()["code"] == 200

        resp = requests.get(f"{base_url}/api/v1/tags{auth_url}&name={name}")
        assert resp.status_code == 200
        assert resp.json()["code"] == 200
        data = resp.json()["data"]
        assert data["total"] >= 1
        return data["lists"][0]["id"]

    def _article_data(self, tag_id):
        suffix = random.randint(10000, 90000)
        return {
            "tag_id": tag_id,
            "title": f"test_article_title_{suffix}",
            "desc": f"test_article_desc_{suffix}",
            "content": f"test_article_content_{suffix}",
            "created_by": "test_admin",
            "cover_image_url": f"http://example.com/cover_{suffix}.jpg",
            "state": 1
        }

    @allure.story("创建文章")
    @allure.title("正常创建")
    def test_add_article_success(self, base_url, auth_url):
        tag_id = self._create_tag(base_url, auth_url)
        data = self._article_data(tag_id)
        resp = requests.post(f"{base_url}/api/v1/articles{auth_url}", data=data)
        assert resp.status_code == 200
        assert resp.json()["code"] == 200

    @allure.story("创建文章")
    @allure.title("tag_id指向不存在的标签")
    def test_add_article_tag_not_exist(self, base_url, auth_url):
        data = self._article_data(99999)
        resp = requests.post(f"{base_url}/api/v1/articles{auth_url}", data=data)
        assert resp.status_code == 200
        assert resp.json()["code"] == 10003

    @allure.story("创建文章")
    @allure.title("tag_id为0")
    def test_add_article_tag_id_zero(self, base_url, auth_url):
        data = self._article_data(0)
        resp = requests.post(f"{base_url}/api/v1/articles{auth_url}", data=data)
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("创建文章")
    @allure.title("tag_id为负数")
    def test_add_article_tag_id_negative(self, base_url, auth_url):
        data = self._article_data(-1)
        resp = requests.post(f"{base_url}/api/v1/articles{auth_url}", data=data)
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("创建文章")
    @allure.title("title为空")
    def test_add_article_title_empty(self, base_url, auth_url):
        tag_id = self._create_tag(base_url, auth_url)
        data = self._article_data(tag_id)
        data["title"] = ""
        resp = requests.post(f"{base_url}/api/v1/articles{auth_url}", data=data)
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("创建文章")
    @allure.title("desc为空")
    def test_add_article_desc_empty(self, base_url, auth_url):
        tag_id = self._create_tag(base_url, auth_url)
        data = self._article_data(tag_id)
        data["desc"] = ""
        resp = requests.post(f"{base_url}/api/v1/articles{auth_url}", data=data)
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("创建文章")
    @allure.title("content为空")
    def test_add_article_content_empty(self, base_url, auth_url):
        tag_id = self._create_tag(base_url, auth_url)
        data = self._article_data(tag_id)
        data["content"] = ""
        resp = requests.post(f"{base_url}/api/v1/articles{auth_url}", data=data)
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("创建文章")
    @allure.title("created_by为空")
    def test_add_article_created_by_empty(self, base_url, auth_url):
        tag_id = self._create_tag(base_url, auth_url)
        data = self._article_data(tag_id)
        data["created_by"] = ""
        resp = requests.post(f"{base_url}/api/v1/articles{auth_url}", data=data)
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("创建文章")
    @allure.title("cover_image_url为空")
    def test_add_article_cover_empty(self, base_url, auth_url):
        tag_id = self._create_tag(base_url, auth_url)
        data = self._article_data(tag_id)
        data["cover_image_url"] = ""
        resp = requests.post(f"{base_url}/api/v1/articles{auth_url}", data=data)
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("创建文章")
    @allure.title("不带Token")
    def test_add_article_without_token(self, base_url):
        data = self._article_data(1)
        resp = requests.post(f"{base_url}/api/v1/articles", data=data)
        assert resp.status_code == 401
        assert resp.json()["code"] == 400

    @allure.story("创建文章")
    @allure.title("title刚好100字符")
    def test_add_article_title_boundary_100(self, base_url, auth_url):
        tag_id = self._create_tag(base_url, auth_url)
        suffix = random.randint(10000, 90000)
        title = f"{'a' * (99 - len(str(suffix)))}_{suffix}"
        assert len(title) == 100
        data = self._article_data(tag_id)
        data["title"] = title
        resp = requests.post(f"{base_url}/api/v1/articles{auth_url}", data=data)
        assert resp.status_code == 200
        assert resp.json()["code"] == 200

    @allure.story("创建文章")
    @allure.title("title超过100字符")
    def test_add_article_title_over_100(self, base_url, auth_url):
        tag_id = self._create_tag(base_url, auth_url)
        suffix = random.randint(10000, 90000)
        title = f"{'a' * (100 - len(str(suffix)))}_{suffix}"
        assert len(title) == 101
        data = self._article_data(tag_id)
        data["title"] = title
        resp = requests.post(f"{base_url}/api/v1/articles{auth_url}", data=data)
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("创建文章")
    @allure.title("desc刚好255字符")
    def test_add_article_desc_boundary_255(self, base_url, auth_url):
        tag_id = self._create_tag(base_url, auth_url)
        desc = "a" * 255
        assert len(desc) == 255
        data = self._article_data(tag_id)
        data["desc"] = desc
        resp = requests.post(f"{base_url}/api/v1/articles{auth_url}", data=data)
        assert resp.status_code == 200
        assert resp.json()["code"] == 200

    @allure.story("创建文章")
    @allure.title("state=0创建不可见文章")
    def test_add_article_state_zero(self, base_url, auth_url):
        tag_id = self._create_tag(base_url, auth_url)
        data = self._article_data(tag_id)
        data["state"] = 0
        resp = requests.post(f"{base_url}/api/v1/articles{auth_url}", data=data)
        assert resp.status_code == 200
        assert resp.json()["code"] == 200

    # ==================== 获取文章列表 ====================
    @allure.story("获取文章列表")
    @allure.title("正常获取（不筛选）")
    def test_get_articles_success(self, base_url, auth_url):
        resp = requests.get(f"{base_url}/api/v1/articles{auth_url}")
        assert resp.status_code == 200
        assert resp.json()["code"] == 200
        assert "data" in resp.json()
        assert "lists" in resp.json()["data"]
        assert "total" in resp.json()["data"]

    @allure.story("获取文章列表")
    @allure.title("不带Token")
    def test_get_articles_without_token(self, base_url):
        resp = requests.get(f"{base_url}/api/v1/articles")
        assert resp.status_code == 401
        assert resp.json()["code"] == 400

    @allure.story("获取文章列表")
    @allure.title("按tag_id筛选")
    def test_get_articles_filter_by_tag(self, base_url, auth_url):
        tag_id = self._create_tag(base_url, auth_url)
        data = self._article_data(tag_id)
        requests.post(f"{base_url}/api/v1/articles{auth_url}", data=data)

        resp = requests.get(f"{base_url}/api/v1/articles{auth_url}&tag_id={tag_id}")
        assert resp.status_code == 200
        assert resp.json()["code"] == 200
        articles = resp.json()["data"]["lists"]
        assert all(a["tag_id"] == tag_id for a in articles)

    @allure.story("获取文章列表")
    @allure.title("按state=1筛选")
    def test_get_articles_filter_by_state_1(self, base_url, auth_url):
        resp = requests.get(f"{base_url}/api/v1/articles{auth_url}&state=1")
        assert resp.status_code == 200
        assert resp.json()["code"] == 200
        articles = resp.json()["data"]["lists"]
        assert all(a["state"] == 1 for a in articles)

    @allure.story("获取文章列表")
    @allure.title("按state=0筛选")
    def test_get_articles_filter_by_state_0(self, base_url, auth_url):
        resp = requests.get(f"{base_url}/api/v1/articles{auth_url}&state=0")
        assert resp.status_code == 200
        assert resp.json()["code"] == 200
        articles = resp.json()["data"]["lists"]
        assert all(a["state"] == 0 for a in articles)

    @allure.story("获取文章列表")
    @allure.title("tag_id不存在")
    def test_get_articles_tag_not_exist(self, base_url, auth_url):
        resp = requests.get(f"{base_url}/api/v1/articles{auth_url}&tag_id=99999")
        assert resp.status_code == 200
        assert resp.json()["code"] == 200
        assert resp.json()["data"]["total"] == 0

    @allure.story("获取文章列表")
    @allure.title("state非法值")
    def test_get_articles_state_invalid(self, base_url, auth_url):
        resp = requests.get(f"{base_url}/api/v1/articles{auth_url}&state=999")
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    # ==================== 获取单篇文章 ====================
    def _create_article(self, base_url, auth_url):
        tag_id = self._create_tag(base_url, auth_url)
        data = self._article_data(tag_id)
        resp = requests.post(f"{base_url}/api/v1/articles{auth_url}", data=data)
        assert resp.status_code == 200
        assert resp.json()["code"] == 200

        resp = requests.get(f"{base_url}/api/v1/articles{auth_url}&tag_id={tag_id}")
        assert resp.status_code == 200
        articles = resp.json()["data"]["lists"]
        assert len(articles) >= 1
        return articles[0]["id"], articles[0]["title"]

    @allure.story("获取单篇文章")
    @allure.title("正常获取")
    def test_get_article_success(self, base_url, auth_url):
        article_id, title = self._create_article(base_url, auth_url)
        resp = requests.get(f"{base_url}/api/v1/articles/{article_id}{auth_url}")
        assert resp.status_code == 200
        assert resp.json()["code"] == 200
        data = resp.json()["data"]
        assert data["id"] == article_id
        assert data["title"] == title

    @allure.story("获取单篇文章")
    @allure.title("文章不存在")
    def test_get_article_not_exist(self, base_url, auth_url):
        resp = requests.get(f"{base_url}/api/v1/articles/99999{auth_url}")
        assert resp.status_code == 200
        assert resp.json()["code"] == 10011

    @allure.story("获取单篇文章")
    @allure.title("ID为负数")
    def test_get_article_negative_id(self, base_url, auth_url):
        resp = requests.get(f"{base_url}/api/v1/articles/-1{auth_url}")
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("获取单篇文章")
    @allure.title("ID为非数字")
    def test_get_article_non_numeric_id(self, base_url, auth_url):
        resp = requests.get(f"{base_url}/api/v1/articles/abc{auth_url}")
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    # ==================== 更新文章 ====================
    def _update_article_data(self, tag_id):
        suffix = random.randint(10000, 90000)
        return {
            "tag_id": tag_id,
            "title": f"test_article_title_update_{suffix}",
            "desc": f"test_article_desc_update_{suffix}",
            "content": f"test_article_content_update_{suffix}",
            "modified_by": "test_admin_update",
            "cover_image_url": f"http://example.com/cover_update_{suffix}.jpg",
            "state": 1
        }

    @allure.story("更新文章")
    @allure.title("正常更新")
    def test_edit_article_success(self, base_url, auth_url):
        article_id, _ = self._create_article(base_url, auth_url)
        tag_id = self._create_tag(base_url, auth_url)
        data = self._update_article_data(tag_id)
        resp = requests.put(f"{base_url}/api/v1/articles/{article_id}{auth_url}", data=data)
        assert resp.status_code == 200
        assert resp.json()["code"] == 200

    @allure.story("更新文章")
    @allure.title("更新不存在的文章")
    def test_edit_article_not_exist(self, base_url, auth_url):
        tag_id = self._create_tag(base_url, auth_url)
        data = self._update_article_data(tag_id)
        resp = requests.put(f"{base_url}/api/v1/articles/99999{auth_url}", data=data)
        assert resp.status_code == 200
        assert resp.json()["code"] == 10011

    @allure.story("更新文章")
    @allure.title("tag_id改为不存在的标签")
    def test_edit_article_tag_not_exist(self, base_url, auth_url):
        article_id, _ = self._create_article(base_url, auth_url)
        data = self._update_article_data(99999)
        resp = requests.put(f"{base_url}/api/v1/articles/{article_id}{auth_url}", data=data)
        assert resp.status_code == 200
        assert resp.json()["code"] == 10003

    @allure.story("更新文章")
    @allure.title("title为空")
    def test_edit_article_title_empty(self, base_url, auth_url):
        article_id, _ = self._create_article(base_url, auth_url)
        tag_id = self._create_tag(base_url, auth_url)
        data = self._update_article_data(tag_id)
        data["title"] = ""
        resp = requests.put(f"{base_url}/api/v1/articles/{article_id}{auth_url}", data=data)
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("更新文章")
    @allure.title("modified_by为空")
    def test_edit_article_modified_by_empty(self, base_url, auth_url):
        article_id, _ = self._create_article(base_url, auth_url)
        tag_id = self._create_tag(base_url, auth_url)
        data = self._update_article_data(tag_id)
        data["modified_by"] = ""
        resp = requests.put(f"{base_url}/api/v1/articles/{article_id}{auth_url}", data=data)
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("更新文章")
    @allure.title("不带Token")
    def test_edit_article_without_token(self, base_url):
        data = self._update_article_data(1)
        resp = requests.put(f"{base_url}/api/v1/articles/1", data=data)
        assert resp.status_code == 401
        assert resp.json()["code"] == 400

    @allure.story("更新文章")
    @allure.title("ID为负数")
    def test_edit_article_negative_id(self, base_url, auth_url):
        tag_id = self._create_tag(base_url, auth_url)
        data = self._update_article_data(tag_id)
        resp = requests.put(f"{base_url}/api/v1/articles/-1{auth_url}", data=data)
        assert resp.status_code == 400
        assert resp.json()["code"] == 400

    @allure.story("更新文章")
    @allure.title("title刚好100字符")
    def test_edit_article_title_boundary_100(self, base_url, auth_url):
        article_id, _ = self._create_article(base_url, auth_url)
        tag_id = self._create_tag(base_url, auth_url)
        data = self._update_article_data(tag_id)
        suffix = random.randint(10000, 90000)
        title = f"{'c' * (99 - len(str(suffix)))}_{suffix}"
        assert len(title) == 100
        data["title"] = title
        resp = requests.put(f"{base_url}/api/v1/articles/{article_id}{auth_url}", data=data)
        assert resp.status_code == 200
        assert resp.json()["code"] == 200

    # ==================== 删除文章 ====================
    @allure.story("删除文章")
    @allure.title("正常删除")
    def test_delete_article_success(self, base_url, auth_url):
        article_id, _ = self._create_article(base_url, auth_url)
        resp = requests.delete(f"{base_url}/api/v1/articles/{article_id}{auth_url}")
        assert resp.status_code == 200
        assert resp.json()["code"] == 200

    @allure.story("删除文章")
    @allure.title("删除不存在的文章")
    def test_delete_article_not_exist(self, base_url, auth_url):
        resp = requests.delete(f"{base_url}/api/v1/articles/99999{auth_url}")
        assert resp.status_code == 200
        assert resp.json()["code"] == 10011

    @allure.story("删除文章")
    @allure.title("重复删除同一个ID")
    def test_delete_article_twice(self, base_url, auth_url):
        article_id, _ = self._create_article(base_url, auth_url)

        resp = requests.delete(f"{base_url}/api/v1/articles/{article_id}{auth_url}")
        assert resp.status_code == 200
        assert resp.json()["code"] == 200

        resp = requests.delete(f"{base_url}/api/v1/articles/{article_id}{auth_url}")
        assert resp.status_code == 200
        assert resp.json()["code"] == 10011

    @allure.story("删除文章")
    @allure.title("ID为负数")
    def test_delete_article_negative_id(self, base_url, auth_url):
        resp = requests.delete(f"{base_url}/api/v1/articles/-1{auth_url}")
        assert resp.status_code == 200
        assert resp.json()["code"] == 400

    @allure.story("删除文章")
    @allure.title("不带Token")
    def test_delete_article_without_token(self, base_url):
        resp = requests.delete(f"{base_url}/api/v1/articles/1")
        assert resp.status_code == 401
        assert resp.json()["code"] == 400

    @allure.story("删除文章")
    @allure.title("ID为非数字")
    def test_delete_article_non_numeric_id(self, base_url, auth_url):
        resp = requests.delete(f"{base_url}/api/v1/articles/abc{auth_url}")
        assert resp.status_code == 200
        assert resp.json()["code"] == 400


