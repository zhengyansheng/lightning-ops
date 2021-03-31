# lightning-ops

## 环境依赖

### 版本依赖

- Python 3.6+
- Django 3.1+
- MySQL 5.7+
- Redis 3.2+


## 模块介绍
- [x] 用户管理
- [X] LDAP登陆
- [x] API权限
- [x] 服务树
- [x] CMDB
- [x] 作业平台 
- [ ] 流量调度


## 项目目录结构
```text
$ tree -L 1
.
├── LICENSE
├── Makefile   # 命令行快捷方式
├── README.md  # 说明文档
├── apps       # 项目app
├── base       # 基础库
├── common     # 通用工具函数
├── config     # 配置文件
├── data       # 上传的图片/脚本等
├── docs       # 文档
├── logs       # 日志目录
├── manage.py  # 默认命令行脚本入口文件
├── middleware # 项目中间件
├── ops        # 项目目录 
├── requirements.txt # 项目依赖的第三方包
├── start.sh   # 启动脚本
├── static     # 项目静态文件目录
└── stop.sh    # 停止脚本
```

## 部署

- 克隆代码
```bash
$ git clone git@github.com:zhengyansheng/lightning-ops.git 
```

- 虚拟环境
```bash
$ cd lightning-ops
$ python3.6 -m venv .venv
$ source .venv/bin/activate
```

```bash
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

- 同步数据库
```bash
$ make migrate 
```

- 启动服务
```bash
$ make run 
```
```bash
$ ./start.sh
```

- supervisor

```bash
[program:lightning-ops]
directory=/opt/lightning-ops
command=/opt/lightning-ops/.venv/bin/gunicorn ops.wsgi:application -b 0.0.0.0:9000 -w 4 -k gthread
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/opt/lightning-ops/logs/supervisor.log
startsecs=0
```

- systemd支持

```
cat >/usr/lib/systemd/system/lightning-ops.service<<\EOF
[Unit]
Description='The lightning-ops server'
After=network.target

[Service]
Type=forking
PrivateTmp=true
Restart=on-failure
PIDFile=/run/gunicorn.pid
ExecStart=/opt/lightning-ops/.venv/bin/gunicorn -c /opt/lightning-ops/config/gunicorn.conf.py ops.wsgi:application --pid /run/gunicorn.pid
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable lightning-ops
systemctl restart lightning-ops
systemctl status lightning-ops
```
