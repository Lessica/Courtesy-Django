# 礼记 - 后台业务

## 协议 Protocol

### 通用 Common
POST /api/courtesy

- 通用成功 Common Succeed
```json
{
    "error": 0,
    "timestamp": 1456283003
}
```

- 错误的请求 Bad Request (e.g. Not POST)
```json
{
    "error": 400,
    "timestamp": 1456283003
}
```

- 无效的字段或格式 Invalid Field & Invalid Format (e.g. over-length)
```json
{
    "error": 401,
    "field": "email",
    "timestamp": 1456283003
}
```

- 缺少字段 Missing Field
```json
{
    "error": 402,
    "field": "account",
    "timestamp": 1456283003
}
```

- 无权限 Forbidden (e.g. not login)
```json
{
    "error": 403,
    "timestamp": 1456283003
}
```

- 未找到 Not Found (e.g. action not found)
```json
{
    "error": 404,
    "timestamp": 1456283003
}
```

- 服务器错误 Service Error (e.g. MYSQL error)
```json
{
    "error": 503,
    "timestamp": 1456283003
}
```

### 注册 Register
```json
{
    "action": "user_register",
    "account": {
        "email": "i.82@qq.com",
        "pwd": "5f4dcc3b5aa765d61d8327deb882cf99"
    },
    "version": 2
}
```

- 账户冲突 Conflict
```json
{
    "error": 405,
    "field": "email",
    "timestamp": 1456283003
}
```

### 登录 Login
```json
{
    "action": "user_login",
    "account": {
        "email": "i.82@me.com",
        "pwd": "5f4dcc3b5aa765d61d8327deb882cf99"
    },
    "version": 2
}
```

- 认证失败 Account Not Found & Wrong Password
```json
{
    "error": 406,
    "timestamp": 1456283003
}
```

- 账户被禁用 Account Banned
```json
{
    "error": 407,
    "timestamp": 1456283003
}
```

- 登录成功 Login Succeed (SESSION in Cookie)

### 注销 Logout
```json
{
    "action": "user_logout",
    "version": 2
}
```

### 获取用户信息 Get User Info
```json
{
    "action": "user_info",
    "version": 2
}
```

- 获取成功 Succeed
```json
{
    "error": 0,
    "account_info": {
        "user_id": 1,
        "email": "i.82@me.com",
        "registered_at": 1456283003,
        "last_login_at": 1456283003,
        "card_count": 2,
        "has_profile": true,
        "profile": {
            "nick": "\u6211\u53eb i_82",
            "avatar": "\\static\\avatar\\aaca0f5eb4d2d98a6ce6dffa99f8254b_300.png",
            "mobile": "13800138000",
            "birthday": "1972-03-21",
            "gender": 1,
            "province": "\u6c5f\u82cf",
            "city": "\u5357\u4eac",
            "area": "\u9097\u6c5f\u533a",
            "introduction": ""
        }
    },
    "timestamp": 1456283003
}
```

### 修改用户信息 Edit Profile
```json
{
    "action": "user_edit_profile",
    "version": 2,
    "profile": {
        "nick": "\u6211\u53eb i_82",
        "avatar": "\\static\\avatar\\aaca0f5eb4d2d98a6ce6dffa99f8254b_300.png",
        "mobile": "13800138000",
        "birthday": "1972-03-21",
        "gender": 1,
        "province": "\u6c5f\u82cf",
        "city": "\u5357\u4eac",
        "area": "\u9097\u6c5f\u533a",
        "introduction": ""
    }
}
```

### 上传用户头像 Upload Avatar
POST /upload/avatar (Field: avater)

- 尺寸不合要求 Size Dismatch
```json
{
    "error": 422,
    "timestamp": 1456283003
}
```

- 上传成功 Upload Succeed
```json
{
    "error": 0,
    "id": "59d632f13aef67deace793df18174dc0",
    "time": 1456503286
}
```

### 上传用户背景 Upload Banner
POST /upload/banner (Field: banner)

- 尺寸不合要求 Size Dismatch
```json
{
    "error": 422,
    "timestamp": 1456283003
}
```

- 上传成功 Upload Succeed
```json
{
    "error": 0,
    "id": "59d632f13aef67deace793df18174dc0",
    "time": 1456503286
}
```

## 二维码业务逻辑 QRCode Workflow

![flow]( https://github.com/Lessica/Courtesy-Django/blob/master/flow.png "flow")

### 查询二维码状态 Query QRCode Status
```json
{
    "action":"qr_query",
    "qr_id":"xxxx",
}
```

- 二维码未录入数据 Not Recorded
```json
{
    "error": 0,
    "qr_info": {
        "is_recorded": false,
        "scan_count": 0,
        "created_at": 1456457567,
        "channel": 0,
        "recorded_at": null,
        "card_token": null,
        "unique_id": "3a0137fbecf5a7bfbc25af10c27c54b4"
    },
    "card_info": null,
    "timestamp": 1456283003
}
```

- 二维码已录入数据 Published Card
```json
{
    "error": 0,
    "qr_info": {
        "is_recorded": true,
        "scan_count": 0,
        "created_at": 1456457567,
        "channel": 0,
        "recorded_at": 1456457593,
        "card_token": "daffed346e29c5654f54133d1fc65ccb",
        "unique_id": "3a0137fbecf5a7bfbc25af10c27c54b4"
    },
    "timestamp": 1456283003
}
```

### 查询卡片状态 Query Card Status
```json
{
    "action": "card_query",
    "token": "00b3eed3b733afba6e45cdedf0036801"
}
```

- 成功 Succeed
```json
{
    "error": 0,
    "card_info": {
        "read_by": {
            "user_id": 5,
            "email": "test005@126.com",
            "profile": {
                "nick": "test005",
                "avatar": "f7ba6151aadf2379394678ac754c9b28"
            }
        },
        "is_editable": true,
        "is_public": true,
        "local_template": "%xml_data%",
        "view_count": 1,
        "author": {
            "user_id": 4,
            "email": "test004@126.com",
            "profile": {
                "nick": "test004",
                "avatar": "1a86a0de6143dfa55d87a70ab0f302ce"
            }
        },
        "created_at": 1456547164,
        "modified_at": 1456547164,
        "first_read_at": null,
        "token": "00b3eed3b733afba6e45cdedf0036801",
        "edited_count": 0,
        "stars": 0
    },
    "timestamp": 1456283003
}
```

- 卡片被禁用 Banned Card
```json
{
    "error": 426,
    "timestamp": 1456283198
}
```

- 卡片未到查询时间 Card Not Visible (local_template = null)

### 修改卡片内容 Edit Card
```json
{
    "action": "card_edit",
    "token": "00b3eed3b733afba6e45cdedf0036801",
    "card_info": {
        "local_template": "%xml_data%",
        "is_editable": true,
        "is_public": true,
        "visible_at": "1999-02-02 00:00:00"
    }
}
```

- 成功 Succeed
```json
{
    "error": 0,
    "card_info": {
        "read_by": {
            "user_id": 5,
            "email": "test005@126.com",
            "profile": {
                "nick": "test005",
                "avatar": "f7ba6151aadf2379394678ac754c9b28"
            }
        },
        "is_editable": true,
        "is_public": true,
        "local_template": "%xml_data%",
        "view_count": 1,
        "author": {
            "user_id": 4,
            "email": "test004@126.com",
            "profile": {
                "nick": "test004",
                "avatar": "1a86a0de6143dfa55d87a70ab0f302ce"
            }
        },
        "created_at": 1456547164,
        "modified_at": 1456548900,
        "first_read_at": null,
        "token": "00b3eed3b733afba6e45cdedf0036801",
        "edited_count": 1,
        "stars": 0
    },
    "timestamp": 1456283003
}
```

- 修改用户无权限 No Card Privilege
```json
{
    "error": 425,
    "timestamp": 1456283098
}
```

- 卡片被禁用 Banned Card (同上)

### 同步确认请求 Sync Query
```json
{
    "action": "card_create_query",
    "card_info": {
        "token": "8FF5D3B4-FDC4-4326-9D75-CEACFD700EA3",
        "qr_id": "3a0137fbecf5a7bfbc25af10c27c54b4",
        "local_template": "%xml_data%",
        "is_editable": true,
        "is_public": true,
        "visible_at": "1999-02-02 00:00:00"
    }
}
```

- 校验成功，请客户端开始同步 Succeed, Ready For Sync
```json
{
    "time": 1456622272,
    "token": "8FF5D3B4-FDC4-4326-9D75-CEACFD700EA3",
    "error": 0
}
```

### 发布卡片 Publish New Card
```json
{
    "action": "card_create",
    "card_info": {
        "token": "8FF5D3B4-FDC4-4326-9D75-CEACFD700EA3",
        "qr_id": "3a0137fbecf5a7bfbc25af10c27c54b4",
        "local_template": "%xml_data%",
        "is_editable": true,
        "is_public": true,
        "visible_at": "1999-02-02 00:00:00"
    }
}
```

- 成功 Succeed
```json
{
    "error":0,
    "time":1461246479,
    "card_info":{
        "is_public":true,
        "author":{
            "registered_at":1459181174,
            "last_login_at":1461243724,
            "card_count":0,
            "user_id":4,
            "email":"i.82@qq.com",
            "profile":{
                "avatar":"b10eec2cdaf08abd437a70dbfe82d221",
                "nick":"i_82",
                "city":"扬州市",
                "mobile":"13800138000",
                "gender":0,
                "area":"邗江区",
                "birthday":"1972-03-21",
                "introduction":"Love is a play that a person who gets gains and losses!",
                "province":"江苏省"
            }
        },
        "is_editable":false,
        "visible_at":0,
        "created_at":1461246479,
        "view_count":0,
        "read_by":"",
        "local_template":{
            "shouldAutoPlayAudio":false,
            "fontType":0,
            "content":"说点什么吧…… ￼ ",
            "fontSize":16,
            "styleID":0,
            "alignmentType":0,
            "attachments":[
                {
                    "length":12,
                    "location":8,
                    "uploaded_at":0,
                    "created_at":1461246475,
                    "salt_hash":"b07a1ae8333671c8d1bd14989e06257a3e6097eebd18bce48306308d67d9057c",
                    "title":"",
                    "type":0,
                    "card_token":"010CF033-CBD4-48CD-844F-26F8ADB698ED"
                }
            ],
            "attachments_hashes":[
                "b07a1ae8333671c8d1bd14989e06257a3e6097eebd18bce48306308d67d9057c"
            ]
        },
        "token":"010CF033-CBD4-48CD-844F-26F8ADB698ED",
        "stars":0,
        "edited_count":0,
        "modified_at":1461246479,
        "first_read_at":null
    }
}
```

- QRCode 已被自己使用 Recorded QRCode
```json
{
    "error": 424,
    "qr_info": {
        "is_recorded": true,
        "scan_count": 0,
        "created_at": 1456457567,
        "channel": 0,
        "recorded_at": 1456457593,
        "unique_id": "3a0137fbecf5a7bfbc25af10c27c54b4",
        "card_token": "daffed346e29c5654f54133d1fc65ccb"
    },
    "timestamp": 1456628034
}
```

### 检查卡片资源是否存在 Query Card Resources
```json
{
    "action": "res_query",
    "hash": "a9993e364706816aba3e25717850c26c9cd0d89d"
}
```

- 资源存在 File Exists
```json
{
    "res": {
        "sha_256": "3120c808d57e9818589b644ae2b6cb956e65f169b1972fa6de745da298a239d7",
        "id": "8c28302bcaa2281eb7c0ff3c3abb30df"
    },
    "time": 1456712336,
    "error": 0
}
```

- 资源不存在 File Not Exists (404)

### 上传卡片资源 Upload Card Resources
POST /upload/card_res (Field: res)

- 成功 Succeed
```json
{
    "time": 1456622272,
    "id": "6859b83bcb97c0a4690ccb950cf3c0da",
    "error": 0
}
```

### 索取新闻 News Query

``` json
{
    "action": "news_query",
    "s_date": "2016-03-28"
}
```

- 成功 Succeed
``` json
{
    "news": [
        {
            "style": {
                "style_id": 0,
                "style_name": "white"
            },
            "string": "News Card",
            "image": {
                "sha256": "",
                "rid": "f5f31fe7306de68436e07ef0fd0a47ee"
            },
            "video": null,
            "date": "2016-03-28",
            "audio": {
                "sha256": "",
                "rid": "e48a31fb7f5e091f3fa22cdf449d5441"
            },
            "url": null,
            "type": 0,
        },
        {
            "style": {
                "style_id": 1,
                "style_name": "black"
            },
            "string": "Link Card",
            "image": {
                "sha256": "",
                "rid": "5f1be1879cf7e69f1507ba14ff7cdcfe"
            },
            "video": null,
            "date": "2016-03-28",
            "audio": null,
            "url": "https://82flex.com",
            "type": 1,
        },
    ],
    "time": 1459172482,
    "error": 0
}
```

### 删除卡片 (实际上是封禁) Delete Card

``` json
{
    "action": "card_delete",
    "token": "8FF5D3B4-FDC4-4326-9D75-CEACFD700EA3"
}
```

- 成功 Succeed
```json
{
    "time": 1456622272,
    "token": "8FF5D3B4-FDC4-4326-9D75-CEACFD700EA3",
    "error": 0
}
```
