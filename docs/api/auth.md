# auth 模块 API

## 总览

以下表格列出了与用户认证相关的 API：

| 方法   | 路径                     | 描述     | Response     |
| ------ | ------------------------ | -------- | ------------ |
| `POST` | [`/auth`](#post-auth)    | 用户登录 | access token |
| `POST` | [`/auth/create`](#post-) | 用户创建 | 用户 ID      |
| `POST` | [`/auth/disable`](#post-) | 用户删除 | 空      |
| `POST` | [`/auth/reset_password`](#post-) | 用户修改密码 | 空 |

## 详细描述

### `POST /auth`

使用用户名和密码进行登录，后端生成`access_token`。

后续请求需要带上`access_token`用于鉴权。

如果鉴权得到`access_token`过期的错误信息，将需要重新登录获取新的`access_token`。

#### Request Body

**必要字段**

|   字段   |  类型  |  描述  |
| :------: | :----: | :----: |
| username | String | 用户名 |
| password | String |  密码  |

#### 请求示例

```bash
curl -X POST \
    http://127.0.0.1:8000/auth \
    -F username=test \
    -F password=test
```

#### Response Body

|     字段     |  类型  |   描述    |
| :----------: | :----: | :-------: |
| access_token | String | JWT Token |

```json
// Example
{
  "access_token": "aaa.bbb.ccc"
}
```

### `POST /auth/create`

#### Request Body

**必要字段**

|   字段   |  类型  |   描述   |
| :------: | :----: | :------: |
| username | String |  用户名  |
| password | String |   密码   |
|  email   | String | 电邮地址 |

#### Response Body

| 字段 |  类型   |  描述   |
| :--: | :-----: | :-----: |
|  id  | Integer | 用户 ID |

### `POST /auth/disable`

#### Request Body

**必要字段**

|   字段   |  类型  |   描述   |
| :------: | :----: | :------: |
| username | String |  用户名  |
| password | String |   密码   |

### `POST /auth/reset_password`

#### Request Body

**必要字段**

|     字段     |  类型  |  描述  |
| :----------: | :----: | :----: |
|   username   | String | 用户名 |
|   password   | String |  密码  |
| new_passowrd | String | 新密码 |