from django.db import models

from base.models import BaseModel
from base.models import JSONFieldDefault
# Create your models here.


class TaskHistory(BaseModel):
    task_id = models.CharField(verbose_name='任务ID', max_length=128, unique=True)
    task_name = models.CharField(verbose_name='任务名称', max_length=32)
    task_hosts = models.JSONField(verbose_name="目标主机", default=JSONFieldDefault)
    script_file = models.CharField(verbose_name='执行脚本', max_length=128, null=True, blank=True)
    task_result = models.JSONField(default=JSONFieldDefault, null=True, blank=True, verbose_name='返回结果')
    exec_interval = models.IntegerField(default=0, verbose_name="运行时长(s)")
    src_ip = models.GenericIPAddressField(verbose_name="来源IP", max_length=50, null=True, blank=True)
    create_user = models.CharField(verbose_name="操作用户", max_length=50, null=True, blank=True)
    task_state = models.BooleanField(default=True, verbose_name='任务执行结果')

    def __str__(self):
        return self.create_user

    class Meta:
        verbose_name = '任务历史'
        verbose_name_plural = verbose_name