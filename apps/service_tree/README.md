# API

## 查看节点信息
```text
URI: /api/v1/service_tree/nodes/
Method: POST
Authorization: JWT xxx

请求Body数据: 
[
	{
        "name": "monkey-api",
        "name_cn": "",
        "parent": 22,
        "remark": "",
    }, {
        "name": "monkey-web",
        "name_cn": "",
        "parent": 22,
        "remark": "",
    }	
]

返回数据

```

## 节点绑定Server
```text
URI: /api/v1/service_tree/server/
Method: POST
Authorization: JWT xxx

请求Body数据: 
{
	"node": 7,     # 节点ID
	"cmdbs": [1]   # /api/v1/cmdb/instances 的ID
}

返回数据

```

## 节点解绑Server
```text
URI: /api/v1/service_tree/server/<pk>/
Method: DELETE
Authorization: JWT xxx

请求Body数据: 


返回数据

注意
- pk 是节点信息的ID

```