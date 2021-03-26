# 作业平台


## 脚本目录
> 以业务线为参考，如果private只能本业务线用，否则所有人可以用.
```text
/data/tasks/
    公司/业务线/script/public_脚本名称.sh
    公司/业务线/script/private_脚本名称.sh
    公司/业务线/playbook/public_脚本名称.sh
    公司/业务线/playbook/private_脚本名称.sh

/data/tasks/<script|palybook>/...

```

## API

```text
http://121.4.224.236:9000/api/v1/tasks/exec/command

{
	"name": "exec df command",
    "hosts": ["172.17.0.13", "localhost", "127.0.0.1"],
    "script_name": "df.sh" 
}
```