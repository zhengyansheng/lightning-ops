from django.db import models
from jsonfield import JSONField


def JSONFieldDefault():
    return {}


def JSONMulFieldDefault():
    return []


# 基类
class BaseModel(models.Model):

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='变更时间')
    remark = models.CharField(max_length=1024, null=True, blank=True, verbose_name='备注')

    class Meta:
        abstract = True
        ordering = ['-id']


class BaseTagModel(BaseModel):
    """
    Tag
    """
    key = models.CharField(max_length=32, db_index=True, verbose_name='Key')
    value = JSONField(default={}, null=False, blank=False, verbose_name='Value')

    class Meta:
        abstract = True




