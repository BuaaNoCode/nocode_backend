# auth 模块 API

## 总览

以下表格列出了与用户认证相关的 API：

| 方法   | 路径                                 | 描述         | Response     |
| ------ | ------------------------------------ | ------------ | ------------ |
| `POST` | [`/auth/`](#post-auth)               | 用户登录     | access token |
| `POST` | [`/auth/captcha`](#post-captcha)     | 获取验证码   | 成功信息     |
| `POST` | [`/auth/create`](#post-authcreate)   | 用户创建     | 用户 ID      |
| `POST` | [`/auth/disable`](#post-authdisable) | 用户删除     | 成功信息     |
| `POST` | [`/auth/reset`](#post-authreset)     | 用户修改密码 | 成功信息     |
| `POST` | [`/auth/forgot`](#post-forgot)       | 用户忘记密码 | 成功信息     |

## 详细描述

### `POST /auth/`

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
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"username":"test","password":"test"}' \
  http://127.0.0.1:8000/auth/
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

#### Error

| code | detailed_code |          description           |
| :--: | :-----------: | :----------------------------: |
| 400  |    400_01     | 请求参数错误，缺少用户名或密码 |
| 401  |    401_01     |        用户名或密码错误        |

#### 其他与登录相关的 Error

#### Error

| code | detailed_code |     description      |
| :--: | :-----------: | :------------------: |
| 401  |    401_01     | 请求体错误，无法解析 |
| 401  |    401_02     |      Token 无效      |
| 401  |    404_03     |      Token 过期      |
| 401  |    401_04     |      用户已注销      |

### `POST /auth/captcha`

#### Request Body

| 字段  |  类型  |   描述   |
| :---: | :----: | :------: |
| email | String | 邮箱地址 |

#### Error

| code | detailed_code | description  |
| :--: | :-----------: | :----------: |
| 400  |    400_00     |  请求体错误  |
| 400  |    400_01     | 邮箱地址无效 |

### `POST /auth/create`

#### Request Body

**必要字段**

|   字段   |  类型  |   描述   |
| :------: | :----: | :------: |
| username | String |  用户名  |
| password | String |   密码   |
|  email   | String | 电邮地址 |
| captcha  | String |  验证码  |

#### Response Body

| 字段 |  类型   |  描述   |
| :--: | :-----: | :-----: |
|  id  | Integer | 用户 ID |

#### Error

| code | detailed_code |               description                |
| :--: | :-----------: | :--------------------------------------: |
| 400  |    400_00     |           请求体错误，无法解析           |
| 400  |    400_01     | 请求参数错误，缺少用户名、密码或邮箱地址 |
| 400  |    400_02     |                验证码错误                |
| 409  |    409_00     |                用户名冲突                |

### `POST /auth/disable`

#### Request Body

**必要字段**

|   字段   |  类型  |  描述  |
| :------: | :----: | :----: |
| username | String | 用户名 |
| password | String |  密码  |

#### 请求示例

```bash
curl --header "Content-Type: application/json" \
-H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE1ODgwNjYwNTIsImlhdCI6MTU4Nzk3OTY1MiwidHlwZSI6ImFjY2Vzc190b2tlbiJ9.XTUzaKgtalNsZHARfv3GzDmLyg4QaW3bbcmLHtUfeso" \
--request POST   --data '{"username":"test","password":"new_password"}' \
http://127.0.0.1:8000/auth/disable
```

#### Error

| code | detailed_code |          description           |
| :--: | :-----------: | :----------------------------: |
| 400  |    400_00     |      请求体错误，无法解析      |
| 400  |    400_01     | 请求参数错误，缺少用户名或密码 |
| 401  |    401_01     |        用户名或密码错误        |
| 404  |    404_00     |          此用户不存在          |


### `POST /auth/reset`

#### Request Body

**必要字段**

|     字段     |  类型  |  描述  |
| :----------: | :----: | :----: |
|   username   | String | 用户名 |
|   password   | String |  密码  |
| new_password | String | 新密码 |

#### Error

| code | detailed_code |               description                |
| :--: | :-----------: | :--------------------------------------: |
| 400  |    400_00     |           请求体错误，无法解析           |
| 400  |    400_01     | 请求参数错误，缺少用户名、旧密码或新密码 |
| 401  |    401_01     |             用户名或密码错误             |
| 404  |    404_00     |               此用户不存在               |


### `POST /auth/forgot`

#### Request Body

|   字段   |  类型  |   描述   |
| :------: | :----: | :------: |
| username | String |  用户名  |
| password | String |  新密码  |
|  email   | String | 邮箱地址 |
| captcha  | String |  验证码  |

#### Error

| code | detailed_code |     description      |
| :--: | :-----------: | :------------------: |
| 400  |    400_00     | 请求体错误，无法解析 |
| 400  |    400_01     |     请求参数错误     |
| 400  |    400_02     |      验证码错误      |
| 404  |    404_00     |     此用户不存在     |
