import os

from celery import Celery, platforms

platforms.C_FORCE_ROOT = True
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ops.settings')  # 设置django环境

# 创建实例

app = Celery('ops')
app.config_from_object('django.conf:settings', namespace='CELERY')

# 加载任务
app.autodiscover_tasks([
    # 'apps.tasks.celery_tasks.paramiko_ssh_task',
    # 'apps.tasks.celery_tasks.ansible_runner_task',
    # 'apps.tasks.celery_tasks.local_command_task',
])

# app.autodiscover_tasks()
#
# app.conf.update(
#     CELERYBEAT_SCHEDULE={
#     }
# )
