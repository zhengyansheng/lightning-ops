from base.models import BaseModel

from django.db import models
from django.contrib.auth.models import AbstractUser
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.

class Organization(MPTTModel):
    """
    组织架构
    """
    node = models.CharField(max_length=50, unique=True, verbose_name="名称")
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="上级"
    )

    def __str__(self):
        return self.node

    class MPTTMeta:
        order_insertion_by = ['node']

    class Meta:
        verbose_name = "组织架构"
        verbose_name_plural = verbose_name


class UserProfile(AbstractUser):
    """用户扩展"""
    name = models.CharField(max_length=20, default="", verbose_name="中文姓名")
    phone = models.CharField(max_length=11, default="", verbose_name="手机号码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    image = models.ImageField(
        upload_to="data/upload/%Y/%m",
        default="data/upload/default.jpeg",
        max_length=100,
        null=True,
        blank=True,
    )
    department = models.ForeignKey(
        "Organization",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="部门"
    )
    position = models.CharField(max_length=50, null=True, blank=True, verbose_name="职位")
    superior = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="上级主管")
    staff_id = models.IntegerField(null=True, blank=True, verbose_name='员工编号')
    job_status = models.BooleanField(default=True, verbose_name='员工在职状态')

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username
