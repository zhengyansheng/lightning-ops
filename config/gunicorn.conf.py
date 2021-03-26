import os
import logging
import logging.handlers
import multiprocessing
from logging.handlers import WatchedFileHandler


# 绑定ip和端口号
port = 9000
bind = '0.0.0.0:{}'.format(port)

# 监听队列
backlog = 512

# gunicorn要切换到的目的工作目录
chdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 超时
timeout = 60


# 设置请求后端的真实IP
# x_forwarded_for_header = "X-Real-IP"

# forwarded_allow_ips = "127.0.0.1, localhost"

daemon = True

# 使用gevent模式，还可以使用sync 模式，默认的是sync模式
worker_class = 'gevent'

# 进程数
workers = 2
# workers = multiprocessing.cpu_count() * 2 + 1

# 指定每个进程开启的线程数
threads = 4

# 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
loglevel = 'info'

# 设置gunicorn访问日志格式，错误日志无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'

"""
其每个选项的含义如下：
h          remote address
l          '-'
u          currently '-', may be user name in future releases
t          date of the request
r          status line (e.g. ``GET / HTTP/1.1``)
s          status
b          response length or '-'
f          referer
a          user agent
T          request time in seconds
D          request time in microseconds
L          request time in decimal seconds
p          process ID
"""

# 访问日志文件
accesslog = "logs/access.log"

# 错误日志文件
errorlog = "logs/error.log"
