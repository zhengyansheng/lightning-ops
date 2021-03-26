# user api 文档

- 用户管理
    - 组织架构
    - 岗位管理

## 1. 查看公司组织架构
```text
Uri: /api/v1/corp/organizations/
Method: GET
Authorization: JWT xxx

请求参数:



返回: 
{
    "code": 0,
    "data": {
        "count": 12,
        "next": "http://127.0.0.1:9000/api/v1/corp/organizations/?page=2",
        "previous": null,
        "results": [
            {
                "id": 1,
                "node": "北京在线教育科技公司",
                "lft": 1,
                "rght": 24,
                "tree_id": 2,
                "level": 0,
                "parent": null
            },
            {
                "id": 5,
                "node": "人力资源中心",
                "lft": 2,
                "rght": 3,
                "tree_id": 2,
                "level": 1,
                "parent": 1
            },
            {
                "id": 2,
                "node": "技术研发中心",
                "lft": 4,
                "rght": 19,
                "tree_id": 2,
                "level": 1,
                "parent": 1
            },
            {
                "id": 8,
                "node": "AI平台部",
                "lft": 5,
                "rght": 6,
                "tree_id": 2,
                "level": 2,
                "parent": 2
            },
            {
                "id": 6,
                "node": "信息安全部",
                "lft": 7,
                "rght": 8,
                "tree_id": 2,
                "level": 2,
                "parent": 2
            },
            {
                "id": 7,
                "node": "基础架构部",
                "lft": 9,
                "rght": 10,
                "tree_id": 2,
                "level": 2,
                "parent": 2
            },
            {
                "id": 9,
                "node": "运维部",
                "lft": 11,
                "rght": 18,
                "tree_id": 2,
                "level": 2,
                "parent": 2
            },
            {
                "id": 11,
                "node": "云平台研发",
                "lft": 12,
                "rght": 13,
                "tree_id": 2,
                "level": 3,
                "parent": 9
            },
            {
                "id": 10,
                "node": "系统网络",
                "lft": 14,
                "rght": 15,
                "tree_id": 2,
                "level": 3,
                "parent": 9
            },
            {
                "id": 12,
                "node": "运维研发",
                "lft": 16,
                "rght": 17,
                "tree_id": 2,
                "level": 3,
                "parent": 9
            }
        ]
    },
    "message": null
}
```

## 2. 查看公司, 部门下的用户列表
```text
Uri: /api/v1/corp/organizations/<pk>/user/
Method: GET
Authorization: JWT xxx

请求: 


返回: 
{
    "code": 0,
    "data": [
        {
            "id": 3,
            "last_login": null,
            "is_superuser": false,
            "username": "hehe",
            "first_name": "",
            "last_name": "",
            "is_staff": false,
            "is_active": true,
            "date_joined": "2021-01-10T23:46:00+08:00",
            "name": "",
            "phone": "13260071987",
            "email": "zhengyansheng@qq.com",
            "image": "static/image/default.png",
            "position": null,
            "staff_id": 3,
            "job_status": true,
            "department": {
                "id": 10,
                "name": "系统网络",
                "lft": 14,
                "rght": 15,
                "tree_id": 2,
                "level": 3,
                "parent": 9
            },
            "superior": null,
            "groups": [],
            "user_permissions": []
        }
    ],
    "message": null
}

# ⚠️⚠️⚠️
pk: 公司组织架构的id.
```

## 3. 查看用户列表
```text
Uri: /api/v1/corp/users/
Method: GET
Authorization: JWT xxx

请求: 


返回: 
{
    "code": 0,
    "data": {
        "count": 3,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "last_login": "2021-01-10T22:06:00+08:00",
                "is_superuser": true,
                "username": "root",
                "first_name": "",
                "last_name": "",
                "is_staff": true,
                "is_active": true,
                "date_joined": "2021-01-05T11:27:00+08:00",
                "name": "",
                "phone": "132xxx",
                "email": "root@qq.com",
                "image": "http://127.0.0.1:9000/api/v1/corp/users/data/upload/2021/01/default_gvTnIyc.jpeg",
                "position": null,
                "staff_id": 2,
                "job_status": true,
                "department": {
                    "id": 11,
                    "node": "云平台研发",
                    "lft": 12,
                    "rght": 13,
                    "tree_id": 2,
                    "level": 3,
                    "parent": 9
                },
                "superior": null,
                "groups": [],
                "user_permissions": []
            },
            {
                "id": 2,
                "last_login": null,
                "is_superuser": false,
                "username": "zhengshuai",
                "first_name": "帅",
                "last_name": "郑",
                "is_staff": true,
                "is_active": true,
                "date_joined": "2021-01-10T23:14:00+08:00",
                "name": "",
                "phone": "13260071987",
                "email": "zhengshuai@qq.com",
                "image": "http://127.0.0.1:9000/api/v1/corp/users/data/upload/2021/01/default.jpeg",
                "position": null,
                "staff_id": 1,
                "job_status": true,
                "department": {
                    "id": 12,
                    "node": "运维研发",
                    "lft": 16,
                    "rght": 17,
                    "tree_id": 2,
                    "level": 3,
                    "parent": 9
                },
                "superior": null,
                "groups": [],
                "user_permissions": []
            },
            {
                "id": 3,
                "last_login": null,
                "is_superuser": false,
                "username": "hehe",
                "first_name": "",
                "last_name": "",
                "is_staff": false,
                "is_active": true,
                "date_joined": "2021-01-10T23:46:00+08:00",
                "name": "",
                "phone": "13260071987",
                "email": "zhengyansheng@qq.com",
                "image": "http://127.0.0.1:9000/api/v1/corp/users/data/upload/2021/01/default_FVbRCBA.jpeg",
                "position": null,
                "staff_id": 3,
                "job_status": true,
                "department": {
                    "id": 10,
                    "node": "系统网络",
                    "lft": 14,
                    "rght": 15,
                    "tree_id": 2,
                    "level": 3,
                    "parent": 9
                },
                "superior": null,
                "groups": [],
                "user_permissions": []
            }
        ]
    },
    "message": null
}

# ⚠️⚠️⚠️
pk: 公司组织架构的id.
```