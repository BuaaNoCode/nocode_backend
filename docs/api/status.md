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

| Code | Detailed Error Code |        Error Msg         |
| :--: | :-----------------: | :----------------------: |
| 400  |       400_00        |       BAD_REQUEST        |
| 400  |       400_01        | INVALID_REQUEST_ARGUMENT |

### 401 Unauthorized 族

| Code | Detailed Error Code |          Error Msg           |
| :--: | :-----------------: | :--------------------------: |
| 401  |       400_00        |         UNAUTHORIZED         |
| 401  |       400_01        | INVALID_USERNAME_OR_PASSWORD |
| 401  |       400_02        |        INVALID_TOKEN         |
| 401  |       400_03        |        TOKEN_EXPIRED         |
| 401  |       400_04        |       ACCOUNT_DISABLED       |

### 403 Refuse Access 族

| Code | Detailed Error Code |     Error Msg     |
| :--: | :-----------------: | :---------------: |
| 403  |       403_00        |   REFUSE_ACCESS   |
| 403  |       403_01        | PERMISSION_DENIED |

### 404 Not Found 族

| Code | Detailed Error Code |   Error Msg    |
| :--: | :-----------------: | :------------: |
| 404  |       404_00        | ITEM_NOT_FOUND |

### 405 Method Not Allowed 族

### 409 Duplicated 族

| Code | Detailed Error Code |      Error Msg      |
| :--: | :-----------------: | :-----------------: |
| 409  |       409_00        | ITEM_ALREADY_EXISTS |

### 413 Resource Too Huge 族

| Code | Detailed Error Code | Error Msg  |
| :--: | :-----------------: | :--------: |
| 413  |       413_00        | IMAGE_HUGE |
