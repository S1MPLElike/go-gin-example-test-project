# go-gin-example 测试场景清单


---

## 模块一：认证

### 1. POST /auth — 用户登录

| # | 场景 | 参数 | 预期 code |
|---|------|------|----------|
| 1 | 正常登录 | username=test, password=test123 | 200 |
| 2 | 密码错误 | username=test, password=wrongpass | 20004 |
| 3 | 用户不存在 | username=nobody_99999, password=123456 | 20004 |
| 4 | 用户名为空 | username=, password=test123 | 400 |
| 5 | 密码为空 | username=test, password= | 400 |
| 6 | 用户名和密码都为空 | username=, password= | 400 |

### 2. POST /register — 用户注册

| # | 场景 | 参数 | 预期 code |
|---|------|------|----------|
| 1 | 正常注册 | username=newuser_xxx（随机后缀）, password=123456 | 200 |
| 2 | 重复用户名 | 用已存在的用户名再注册一次 | 400 |
| 3 | 用户名为空 | username=, password=123456 | 400 |
| 4 | 密码为空 | username=newuser, password= | 400 |
| 5 | 用户名刚好 20 字符 | username=20个a, password=123456 | 200 |
| 6 | 用户名超 20 字符 | username=21个a, password=123456 | 400 |
| 7 | 密码小于 6 位 | username=newuser, password=12345 | 400 |
| 8 | 密码刚好 16 位 | username=newuser, password=16个字符 | 200 |
| 9 | 密码超 16 位 | username=newuser, password=17个字符 | 400 |

---

## 模块二：标签

### 3. POST /api/v1/tags — 创建标签

| # | 场景 | 参数 | 预期 code |
|---|------|------|----------|
| 1 | 正常创建 | name=Go, created_by=admin, state=1 | 200 |
| 2 | 正常创建（不传 state，用默认值） | name=Python, created_by=admin | 200 |
| 3 | 重复名称 | name=Go（已存在）, created_by=admin | 10001 |
| 4 | name 为空 | name=, created_by=admin | 400 |
| 5 | created_by 为空 | name=test, created_by= | 400 |
| 6 | 不带 Token | token 参数缺失 | 20001 |
| 7 | Token 伪造/过期 | token=invalid_token_string | 20001 |
| 8 | state 传非法值 | name=test, created_by=admin, state=999 | 400 |
| 9 | name 刚好 100 字符 | name=100个a, created_by=admin | 200 |
| 10 | name 超 100 字符 | name=101个a, created_by=admin | 400 |
| 11 | created_by 刚好 100 字符 | name=test, created_by=100个a | 200 |

### 4. GET /api/v1/tags — 获取标签列表

| # | 场景 | 参数 | 预期 code |
|---|------|------|----------|
| 1 | 正常获取（不带筛选） | 只带 token | 200，data.list 非空 |
| 2 | 不带 Token | 无 token 参数 | 20001 |
| 3 | Token 伪造 | token=invalid | 20001 |
| 4 | 按 name 筛选 | name=Go | 200，返回匹配结果 |
| 5 | 按 name 筛选（不存在的标签） | name=NoSuchTag999 | 200，total=0 |
| 6 | 按 state=1 筛选 | state=1 | 200，返回启用状态的标签 |
| 7 | 按 state=0 筛选 | state=0 | 200，返回禁用状态的标签 |

### 5. PUT /api/v1/tags/:id — 更新标签

| # | 场景 | 参数 | 预期 code |
|---|------|------|----------|
| 1 | 正常更新 | id=有效ID, name=NewName, modified_by=admin | 200 |
| 2 | 更新不存在的 ID | id=99999, name=test, modified_by=admin | 10003 |
| 3 | ID 为负数 | id=-1, name=test, modified_by=admin | 400 |
| 4 | ID 为非数字 | id=abc, name=test, modified_by=admin | 400 |
| 5 | name 为空 | id=有效ID, name=, modified_by=admin | 400 |
| 6 | modified_by 为空 | id=有效ID, name=test, modified_by= | 400 |
| 7 | 不带 Token | 无 token 参数 | 20001 |
| 8 | name 刚好 100 字符 | id=有效ID, name=100个b, modified_by=admin | 200 |

### 6. DELETE /api/v1/tags/:id — 删除标签

| # | 场景 | 参数 | 预期 code |
|---|------|------|----------|
| 1 | 正常删除 | id=有效ID | 200 |
| 2 | 删除不存在的 ID | id=99999 | 10003 |
| 3 | ID 为负数 | id=-1 | 400 |
| 4 | 重复删除同一个 ID | id=已删除的ID | 10003 |
| 5 | 不带 Token | 无 token 参数 | 20001 |
| 6 | 验证软删除 | 删完后 GET /tags 不出现该标签 | — |
| 7 | ID 为非数字 | id=abc | 400 |

### 7. POST /tags/export — 导出标签

| # | 场景 | 参数 | 预期 code |
|---|------|------|----------|
| 1 | 正常导出（不筛选） | 无参数 | 200，data 含 export_url |
| 2 | 按 name 筛选导出 | name=Go | 200 |
| 3 | 按 state 筛选导出 | state=1 | 200 |
| 4 | 筛选不存在的标签 | name=NoSuchTag999 | 200（或10009，实际验证） |
| 5 | state 非法值 | state=999 | 400 |
| 6 | name 超 100 字符 | name=101个a | 400 |

---

## 模块三：文章

### 8. POST /api/v1/articles — 创建文章

| # | 场景 | 参数 | 预期 code |
|---|------|------|----------|
| 1 | 正常创建 | 所有必填字段正确填写 | 200 |
| 2 | tag_id 指向不存在的标签 | tag_id=99999, 其他字段正常 | 10003 |
| 3 | tag_id 为 0 | tag_id=0, 其他字段正常 | 400 |
| 4 | tag_id 为负数 | tag_id=-1, 其他字段正常 | 400 |
| 5 | title 为空 | title=, 其他字段正常 | 400 |
| 6 | desc 为空 | desc=, 其他字段正常 | 400 |
| 7 | content 为空 | content=, 其他字段正常 | 400 |
| 8 | created_by 为空 | created_by=, 其他字段正常 | 400 |
| 9 | cover_image_url 为空 | cover_image_url=, 其他字段正常 | 400 |
| 10 | 不带 Token | 无 token 参数 | 20001 |
| 11 | title 刚好 100 字符 | title=100个a, 其他正常 | 200 |
| 12 | title 超 100 字符 | title=101个a, 其他正常 | 400 |
| 13 | desc 刚好 255 字符 | desc=255个a, 其他正常 | 200 |
| 14 | state=0（创建不可见文章） | state=0, 其他正常 | 200 |

### 9. GET /api/v1/articles — 获取文章列表

| # | 场景 | 参数 | 预期 code |
|---|------|------|----------|
| 1 | 正常获取（不筛选） | 只带 token | 200 |
| 2 | 不带 Token | 无 token 参数 | 20001 |
| 3 | 按 tag_id 筛选 | tag_id=有效ID | 200 |
| 4 | 按 state=1 筛选 | state=1 | 200 |
| 5 | 按 state=0 筛选 | state=0 | 200 |
| 6 | tag_id 不存在 | tag_id=99999 | 200，total=0 |
| 7 | state 非法值 | state=999 | 400 |

### 10. GET /api/v1/articles/:id — 获取单篇文章

| # | 场景 | 参数 | 预期 code |
|---|------|------|----------|
| 1 | 正常获取 | id=有效文章ID | 200，data 含文章详情 |
| 2 | 文章不存在 | id=99999 | 10011 |
| 3 | ID 为负数 | id=-1 | 400 |
| 4 | ID 为非数字 | id=abc | 400 |
| 5 | 不带 Token | 无 token 参数 | 20001 |

### 11. PUT /api/v1/articles/:id — 更新文章

| # | 场景 | 参数 | 预期 code |
|---|------|------|----------|
| 1 | 正常更新 | id=有效ID, 所有字段正确 | 200 |
| 2 | 更新不存在的文章 | id=99999, 字段正常 | 10011 |
| 3 | tag_id 改为不存在的标签 | tag_id=99999, 其他正常 | 10003 |
| 4 | title 为空 | title=, 其他正常 | 400 |
| 5 | created_by 为空 | created_by=, 其他正常 | 400 |
| 6 | 不带 Token | 无 token 参数 | 20001 |
| 7 | ID 为负数 | id=-1 | 400 |
| 8 | title 刚好 100 字符 | title=100个c, 其他正常 | 200 |

### 12. DELETE /api/v1/articles/:id — 删除文章

| # | 场景 | 参数 | 预期 code |
|---|------|------|----------|
| 1 | 正常删除 | id=有效文章ID | 200 |
| 2 | 删除不存在的文章 | id=99999 | 10011 |
| 3 | 重复删除同一个 ID | id=已删除的文章ID | 10011 |
| 4 | ID 为负数 | id=-1 | 400 |
| 5 | 不带 Token | 无 token 参数 | 20001 |
| 6 | ID 为非数字 | id=abc | 400 |

---

