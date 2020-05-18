# HTTP 状态代码

## 成功

HTTP 响应码：200

## 失败

返回体：包含 HTTP 状态代码、具体的错误代码、错误信息的 json 数据

```json
// example
{
  "code": 409,
  "detailed_error_code": 40900,
  "error_msg": "StatusCode.ITEM_ALREADY_EXISTS: Username conflicted"
}
```

### 400 Bad Request 族

| Code | Detailed Error Code |        Error Msg         | Description  |
| :--: | :-----------------: | :----------------------: | :----------: |
| 400  |       400_00        |       BAD_REQUEST        |  请求体错误  |
| 400  |       400_01        | INVALID_REQUEST_ARGUMENT | 请求参数错误 |

### 401 Unauthorized 族

| Code | Detailed Error Code |          Error Msg           |   Description    |
| :--: | :-----------------: | :--------------------------: | :--------------: |
| 401  |       400_00        |         UNAUTHORIZED         |      未认证      |
| 401  |       400_01        | INVALID_USERNAME_OR_PASSWORD | 用户名或密码错误 |
| 401  |       400_02        |        INVALID_TOKEN         | 登录 Token 无效  |
| 401  |       400_03        |        TOKEN_EXPIRED         | 登录 Token 过期  |
| 401  |       400_04        |       ACCOUNT_DISABLED       |    账号已注销    |

### 403 Refuse Access 族

| Code | Detailed Error Code |     Error Msg     | Description |
| :--: | :-----------------: | :---------------: | :---------: |
| 403  |       403_00        |   REFUSE_ACCESS   |  拒绝访问   |
| 403  |       403_01        | PERMISSION_DENIED |  权限不足   |

### 404 Not Found 族

| Code | Detailed Error Code |   Error Msg    |  Description   |
| :--: | :-----------------: | :------------: | :------------: |
| 404  |       404_00        | ITEM_NOT_FOUND | 未找到相应资源 |

### 405 Method Not Allowed 族

### 409 Duplicated 族

| Code | Detailed Error Code |      Error Msg      |   Description    |
| :--: | :-----------------: | :-----------------: | :--------------: |
| 409  |       409_00        | ITEM_ALREADY_EXISTS | 尝试创建资源冲突 |

### 413 Resource Too Huge 族

| Code | Detailed Error Code | Error Msg  |  Description   |
| :--: | :-----------------: | :--------: | :------------: |
| 413  |       413_00        | IMAGE_HUGE | 上传的图片过大 |
