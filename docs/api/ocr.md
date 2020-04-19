# ocr 模块 API

## 总览

以下表格列出了与 OCR 识别相关的 API：

### project

| 方法     | 路径                                                              | 描述             |
| -------- | ----------------------------------------------------------------- | ---------------- |
| `POST`   | [`/ocr/project`](#post-ocrproject)                                | 创建项目         |
| `PUT`    | [`/ocr/project/<int:project_id>`](#put-ocrprojectintprojectid)    | 修改项目信息     |
| `GET`    | [`/ocr/project`](#get-ocrproject)                                 | 获取所有项目信息 |
| `GET`    | [`/ocr/project/<int:project_id>`](#get-ocrprojectintprojectid)    | 获取项目详细信息 |
| `DELETE` | [`/ocr/project/<int:project_id>`](#delete-ocrprojectintprojectid) | 删除项目         |

### recognition_result

| 方法     | 路径                                                                                         | 描述             |
| -------- | -------------------------------------------------------------------------------------------- | ---------------- |
| `POST`   | [`/ocr/project/<int:project_id>`](#post-ocrprojectintprojectid)                              | 上传待识别图片   |
| `GET`    | [`/ocr/project/<int:project_id>/<int:result_id>`](#get-ocrprojectintprojectidintresultid)    | 获取识别结果     |
| `PUT`    | [`/ocr/project/<int:project_id>/<int:result_id>`](#put-ocrprojectintprojectidintresultid)    | 修改识别结果信息 |
| `DELETE` | [`/ocr/project/<int:project_id>/<int:result_id>`](#delete-ocrprojectintprojectidintresultid) | 删除识别结果     |

## 详细描述

### `POST /ocr/project`

创建项目

#### Request Body

|  字段   |  类型  |      描述      |
| :-----: | :----: | :------------: |
|  name   | String |     项目名     |
| comment | String | 可选，项目描述 |

#### Response Body

|    字段    |   类型   |     描述     |
| :--------: | :------: | :----------: |
|     id     | Integer  |   项目 ID    |
| created_at | DateTime | 项目创建时间 |

### `PUT /ocr/project/<int:project_id>`

修改项目信息

#### Request Body

|  字段   |  类型  |      描述      |
| :-----: | :----: | :------------: |
|  name   | String |  可选，项目名  |
| comment | String | 可选，项目描述 |

### `GET /ocr/project`

获取该用户所有项目信息

#### Response Body

|    字段     |  类型   |     描述     |
| :---------: | :-----: | :----------: |
|  projects   |  Array  | 所有项目信息 |
| project_num | Integer |   项目总数   |

projects 字段元素内容

|    字段    |   类型   |     描述     |
| :--------: | :------: | :----------: |
|    name    |  String  |    项目名    |
|  comment   |  String  |   项目描述   |
| created_at | DateTime |   创建时间   |
| result_num | Integer  | 识别结果总数 |

### `GET /ocr/project/<int:project_id>`

获取项目详细信息

#### Response Body

|    字段    |   类型   |     描述     |
| :--------: | :------: | :----------: |
|    name    |  String  |    项目名    |
|  comment   |  String  |   项目描述   |
| created_at | DateTime |   创建时间   |
| result_num | Integer  | 识别结果总数 |
|  results   |  Array   | 所有识别结果 |

results 字段元素内容

|    字段    |   类型   |     描述     |
| :--------: | :------: | :----------: |
|    name    |  String  |  识别结果名  |
|  comment   |  String  | 识别结果描述 |
| created_at | DateTime |   创建时间   |

### `DELETE /ocr/project/<int:project_id>`

删除项目

### `POST /ocr/project/<int:project_id>`

上传待识别图片

#### Request Body(JSON part)

|  字段   |  类型  |        描述        |
| :-----: | :----: | :----------------: |
|  name   | String |  可选，识别结果名  |
| comment | String | 可选，识别结果描述 |

可能的发包方法

```python
import json
import requests

payload = {
    "name": "test",
    "comment": "test comment"
}

files = {
    "json": (None, json.dumps(payload), "application/json"),
    "file": (os.path.basename(file), open(file, "rb"), "image/png")
}

requests.post(url, files=files)
```

#### Response Body

|    字段    |   类型   |    描述     |
| :--------: | :------: | :---------: |
|     id     | Integer  | 识别结果 ID |
| created_at | DateTime |  创建时间   |

### `GET /ocr/project/<int:project_id>/<int:result_id>`

获取识别结果

#### Response Body

|  字段   |  类型  |     描述     |
| :-----: | :----: | :----------: |
|  name   | String |  识别结果名  |
| comment | String | 识别结果描述 |
| result  |  JSON  |   识别结果   |

### `PUT /ocr/project/<int:project_id>/<int:result_id>`

修改识别结果信息

|  字段   |  类型  |        描述        |
| :-----: | :----: | :----------------: |
|  name   | String |  可选，识别结果名  |
| comment | String | 可选，识别结果描述 |

### `DELETE /ocr/project/<int:project_id>/<int:result_id>`

删除识别结果

