# go-gin-example接口清单文档

## 模块一  认证

### POST /auth - 用户登录

| 项目   | 内容                                                    |
|------|-------------------------------------------------------|
| 方法   | POST                                                  |
| URL  | /auth                                                 |
| 鉴权   | 无需,请求成功后获得认证信息                                        |
| 参数格式 | x-www-form-urlencoded(由于用c.PostForm,只可以form系列不可以json) |
| 参数   | username（必填，string）：用户名                               |
|      | password（必填，string）：密码                                |
| 成功响应 | `{"code":200,"msg":"ok","data":{"token":"xxx"}}`      |
| 错误响应 | `{"code": 400,"msg": "请求参数错误","data": null}`          |
|| `{"code": 20004,"msg": "Token错误","data": null}`       |

### POST /register - 用户注册

| 项目   | 内容                                              |
|------|-------------------------------------------------|
| 方法   | POST                                            |
| URL  | /register                                       |
| 鉴权   | 无需                                              |
| 参数格式 | x-www-form-urlencoded                           |
| 参数   | username（必填，string）：用户名(长度不超过20)                |
|      | password（必填，string）：密码(6-16位)                   |
| 成功响应 | `{"code":200,"msg":"ok","data":null}`           |
| 错误响应 | `{"code": 400,"msg": "请求参数错误","data": null}`    |

## 模块二  标签Tags

### POST /api/v1/tags - 创建标签

| 项目   | 内容                                               |
|------|--------------------------------------------------|
| 方法   | POST                                             |
| URL  | /api/v1/tags?token=xxx                           |
| 鉴权   | 需要 Token，Query 参数 ?token=xxx                     |
| 参数格式 | x-www-form-urlencoded/json(由于用c.Bind,所以可以用json)  |
| 参数   | name（必填，string,maxsize(100)）：标签名称，不可重复           |
|      | created_by（必填，string,maxsize(100)）：创建人           |
|      | state（可选，int）：0=禁用 1=启用，默认1                      |
| 成功响应 | `{"code":200,"msg":"ok","data":null}`            |
| 错误响应 | `{"code": 10001,"msg": "已存在该标签名称","data": null}` |

### GET /api/v1/tags - 获取标签列表

| 项目   | 内容                                                     |
|------|--------------------------------------------------------|
| 方法   | GET                                                    |
| URL  | /api/v1/tags?token=xxx                                 |
| 鉴权   | 需要token                                                |
| 参数格式 | 无                                                      |
| 参数   |                                                        |
| 成功响应 | `{"code":200,"msg":"ok","data":{"list":[{xxx},{xxx}],"total":2}}` |
| 错误响应 | `{"code": 20001,"msg": "Token鉴权失败","data": null}`      |


### PUT /api/v1/tags/:id - 根据标签id更新该标签

| 项目   | 内容                                             |
|------|------------------------------------------------|
| 方法   | PUT                                            |
| URL  | /api/v1/tags/:id?token=xxx                     |
| 鉴权   | 需要token                                        |
| 参数格式 | x-www-form-urlencoded/json                     |
| 参数   | name（必填，string,maxsize(100)）：标签新名              |
|| modified_by（必填，string,maxsize(100)）：更新人        | 
|| state（可选，int）：0=禁用，1=启用，默认1                    |
| 成功响应 | `{"code":200,"msg":"ok","data":null`           |
| 错误响应 | `{"code": 10003,"msg": "该标签不存在","data": null}` |

### DELETE /api/v1/:id 删除指定id的标签

| 项目   | 内容                                                       |
|------|----------------------------------------------------------|
| 方法   | DELETE                                                   |
| URL  | /api/v1/tags/:id?token=xxx                               |
| 鉴权   | 需要token                                                  |
| 参数格式 | 无                                                        |
| 参数   |                                                          |
| 成功响应 | `{"code":200,"msg":"ok","data":null}`                    |
| 错误响应 | `{"code": 10003,"msg": "该标签不存在","data": null}`           |
| 备注   | 该业务为软删除，执行后对应数据还在数据库，对应字段delete_on变成当前时间戳，但是获取标签列表后不会出现它 |

### POST /tags/export - 把标签导出为excel表格
| 项目   | 内容                                            |
|------|-----------------------------------------------|
| 方法   | POST                                          |
| URL  | /tags/export                                  |
| 鉴权   | 无需                                            |
| 参数格式 | x-www-form-urlencoded                         |
| 参数   | name（可选，string，maxsize(100)）:标签名，不填则返回所以标签，填则返回指定标签 |
|| state（可选，range（0，1）），:标签状态， 不填则返回所以标签，填则返回指定标签 |
| 成功响应 | `{"code":200,"msg":"ok","data":{"export_save_url":xxx,"export_url":xxx}` |
| 错误响应 | `{"code": 10009,"msg": "导出标签失败","data": null}`|

## 模块三 文章

### POST /api/v1/articles - 创建文章
| 项目   | 内容                                             |
|------|------------------------------------------------|
| 方法   | POST                                           |
| URL  | /api/v1/article?token=xxx                      |
| 鉴权   | 需要token                                        |
| 参数格式 | x-www-form-urlencoded                          |
| 参数   | tag_id(必填，int，min(1)):该文章关联的标签号                |
|| title(必填，string，maxsize(100)):该文章的标题           |
|| desc(必填，string，maxsize(255)):该文章的描述            |
|| content(必填，string，maxsize(65535)):该文章的内容       |
|| created_by(必填，string，maxsize(100)):文章作者        |
|| cover_image_url(必填，string，maxsize(255)):文章的封面  |
|| state(选填，int，range(0,1)):文章可见状态                |
| 成功响应 | `{"code":200,"msg":"ok","data":null}`          |
| 错误响应 | `{"code": 10003,"msg": "该标签不存在","data": null}` |

### GET /api/v1/articles - 获取文章列表

| 项目   | 内容                                                         |
|------|------------------------------------------------------------|
| 方法   | GET                                                        |
| URL  | /api/v1/articles?token=xxx                                 |
| 鉴权   | 需要token                                                    |
| 参数格式 | x-www-form-urlencoded                                      |
| 参数   | state(选填，int，range(0,1)):按照可见状态选择文章                        |
|| tag_id(选填，int，min(1)):根据文章关联的标签号选择                         |
| 成功响应 | `{"code":200,"msg":"ok","data":{"list":[xxx],"total":xxx}` |
| 错误响应 | `{"code":20002,"msg":"Token失效","data":null}`               |


### GET /api/v1/articles/:id - 根据id获取指定文章
| 项目   | 内容                                             |
|------|------------------------------------------------|
| 方法   | GET                                            |
| URL  | /api/v1/articles/:id?token=xxx                 |
| 鉴权   | 需要token                                        |
| 参数格式 | 无                                              |
| 参数   |                                                |
| 成功响应 | `{"code":200,"msg":"ok","data":{xxx}}`         |
| 错误响应 | `{"code": 10011,"msg": "该文章不存在","data": null}` |

### PUT /api/v1/articles/:id - 修改文章
| 项目   | 内容                                             |
|------|------------------------------------------------|
| 方法   | PUT                                            |
| URL  | /api/v1/article/:id?token=xxx                  |
| 鉴权   | 需要token                                        |
| 参数格式 | x-www-form-urlencoded/json                     |
| 参数   | tag_id(必填，int，min(1)):该文章关联的标签号                |
|| title(必填，string，maxsize(100)):该文章的标题           |
|| desc(必填，string，maxsize(255)):该文章的描述            |
|| content(必填，string，maxsize(65535)):该文章的内容       |
|| created_by(必填，string，maxsize(100)):文章作者        |
|| cover_image_url(必填，string，maxsize(255)):文章的封面  |
|| state(选填，int，range(0,1)):文章可见状态                |
| 成功响应 | `{"code":200,"msg":"ok","data":null}`          |
| 错误响应 | `{"code": 10003,"msg": "该标签不存在","data": null}` |

### DELETE /api/v1/articles/:id - 根据id删除指定文章
| 项目   | 内容                                             |
|------|------------------------------------------------|
| 方法   | DELETE                                         |
| URL  | /api/v1/articles/:id?token=xxx                 |
| 鉴权   | 需要token                                        |
| 参数格式 | 无                                              |
| 参数   |                                                |
| 成功响应 | `{"code":200,"msg":"ok","data":null}`          |
| 错误响应 | `{"code": 10011,"msg": "该文章不存在","data": null}` |

