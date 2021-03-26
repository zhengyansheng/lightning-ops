# ops

## 环境依赖

### 版本依赖

- Python 3.6+
- Django 3.1+
- MySQL 5.7+
- Redis 3.2+


## 项目目录结构
```bash
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
$ cd ops
$ python3.6 -m venv .venv
$ source .venv/bin/activate
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
