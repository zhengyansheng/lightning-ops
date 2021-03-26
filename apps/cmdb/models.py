from django.db import models

from base.models import BaseModel
from base.models import BaseTagModel
from base.models import JSONMulFieldDefault


# Create your models here.

class CMDBBase(BaseModel):
    CHOICE_TYPE = (
        (1, "idc"),
        (2, "vm"),
        (3, "cloud"),
        (4, "container"),
    )
    CHOICE_STATE = (
        (1, "running"),
        (2, "stopped"),
    )
    CHOICE_PLATFORM = (
        (1, "aws"),
        (2, "ali"),
        (3, "ten"),
        (4, "hw"),
        (5, "azure"),
        (0, ""),
    )
    CHOICE_INSTANCE_CHARGE_TYPE = (
        ('PrePaid', '包年包月'),
        ('PostPaid', '按量'),
    )

    # common
    private_ip = models.GenericIPAddressField(unique=True, db_index=True, verbose_name="私有IP地址")
    public_ip = models.GenericIPAddressField(db_index=True, null=True, blank=True, verbose_name="公网IP地址")
    extra_private_ip = models.JSONField(default=JSONMulFieldDefault, null=True, blank=True, verbose_name='扩展私有IP')
    extra_public_ip = models.JSONField(default=JSONMulFieldDefault, null=True, blank=True, verbose_name='扩展公网IP')
    hostname = models.CharField(max_length=100, db_index=True, verbose_name="主机名")
    cpu_total = models.IntegerField(verbose_name="CPU(核)")
    mem_total = models.FloatField(verbose_name="内存(G)")
    state = models.IntegerField(choices=CHOICE_STATE, verbose_name="运行状态")
    type = models.IntegerField(choices=CHOICE_TYPE, verbose_name="机器类型")
    platform = models.IntegerField(choices=CHOICE_PLATFORM, default=0, verbose_name="平台")
    os_system = models.CharField(verbose_name='操作系统', max_length=16, null=True, blank=True)
    os_version = models.CharField(verbose_name='系统版本', max_length=64, blank=True, null=True)
    disks = models.JSONField(default=JSONMulFieldDefault, verbose_name='磁盘')
    create_user = models.CharField(max_length=100, null=True, blank=True, verbose_name='创建用户')
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')

    # idc 
    zone_name = models.CharField(max_length=100, verbose_name="位置/可用区")
    region_name = models.CharField(max_length=100, verbose_name="机房/地域")

    # cloud server
    instance_id = models.CharField(verbose_name='实例ID', max_length=64, blank=True, null=True)
    instance_type = models.CharField(verbose_name='实例类型', max_length=64, blank=True, null=True)
    image_id = models.CharField(max_length=64, blank=True, null=True, verbose_name='镜像ID')
    security_group_ids = models.JSONField(default=JSONMulFieldDefault, blank=True, null=True, verbose_name='安全组')
    region_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="地域ID")
    zone_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="可用区ID")
    vpc_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='VPC ID')
    subnet_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='交换机ID')
    expired_time = models.CharField(max_length=32, null=True, blank=True, verbose_name='过期时间')
    instance_charge_type = models.CharField(choices=CHOICE_INSTANCE_CHARGE_TYPE,
                                            null=True,
                                            blank=True,
                                            max_length=32,
                                            verbose_name='主机付费类型')
    account = models.CharField(max_length=50,  null=True, blank=True, verbose_name='云账号')
    root_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='主账号ID')
    create_server_time = models.CharField(max_length=100, default="0000-00-00 00:00:00", verbose_name='实例创建时间')

    def __str__(self):
        return '{} | {} | {}'.format(self.hostname, self.private_ip, self.get_type_display())

    class Meta:
        verbose_name = "CMDB基表"
        verbose_name_plural = verbose_name


class JoinCMDBBaseTag(BaseTagModel):
    cmdb = models.ForeignKey(to=CMDBBase, on_delete=models.CASCADE, verbose_name='CMDB基表')

    def __str__(self):
        return '{} | {}'.format(self.key, self.value)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = verbose_name
