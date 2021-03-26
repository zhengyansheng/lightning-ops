# permission 文档

- api权限管理
    - 角色
    - 权限
    - 用户角色
    - 权限api
    - 前端路由

## 1. 权限接口
```text
Uri: /api/v1/has-perm
Method: POST
Authorization: JWT xxx

请求参数:
{
    "path": "/api/v1/user/"
    "method": "GET"
}

```

## 2. 角色管理
```text
Uri: /api/v1/perm/role
Method: GET,POST,PUT,DELETE
Authorization: JWT xxx

角色拥有的权限(GET POST PUT)
/api/v1/perm/role/<pk>/perms/
角色角色包含哪些用户(GET POST PUT)
/api/v1/perm/role/<pk>/users/
角色拥有的前端路由(GET POST PUT)
/api/v1/perm/role/<pk>/route/
```

## 3. 权限
```text
Uri: /api/v1/perm/perm
Method: GET,POST,PUT,DELETE
Authorization: JWT xxx

权限包含的角色
/api/v1/perm/perm/<pk>/role/
```

## 4. 用户角色
```text
Uri: /api/v1/perm/user/
Method: GET,POST
Authorization: JWT xxx

用户拥有的角色
/api/v1/perm/user/<pk>/roles/
用户拥有的权限
/api/v1/perm/user/<pk>/perms/
用户未拥有的权限
/api/v1/perm/user/<pk>/exclusion-roles/
用户修改角色(PUT)
/api/v1/perm/user/<pk>
```

## 4. 前端视图
```test
视图增删改查
Uri: /api/v1/perm/route
Method: GET,POST,PUT,DELETE
Authorization: JWT xxx

查询格式化视图
api/v1/perm/route/menu

不同用户访问的视图
/api/v1/route
```