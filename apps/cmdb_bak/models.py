from django.db import models
from base.models import BaseModel
from base.models import BaseTagModel
from base.models import JSONMulFieldDefault

__all__ = [
    'TableClassify',
    'TableField',
    'TableData',
    'TableRelation',
    'AssetsRelation'
]


class TableBaseModel(BaseModel):
    is_deleted = models.BooleanField(default=False, verbose_name="已删除")

    class Meta:
        abstract = True


class TableClassify(TableBaseModel):
    # 分类表
    name = models.CharField(max_length=32, unique=True, verbose_name="名称")
    pid = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='父Id')
    is_forbid_bind = models.BooleanField(default=False, verbose_name="默认允许绑定")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '表分类'
        verbose_name_plural = verbose_name


class TableField(TableBaseModel):
    # 表字段 和 验证规则
    table_classify = models.OneToOneField(to=TableClassify, on_delete=models.CASCADE, verbose_name="关联Classify",
                                          related_name='fields')
    # name / order
    fields = models.JSONField(default=dict, verbose_name="字段元数据", )
    rules = models.JSONField(default=dict, verbose_name="字段验证规则")

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = '表字段'
        verbose_name_plural = verbose_name


class TableData(TableBaseModel):
    # 表数据
    table_classify = models.ForeignKey(to=TableClassify, on_delete=models.CASCADE, verbose_name="关联Classify")
    data = models.JSONField(default=dict, verbose_name="数据值")

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = '表数据'
        verbose_name_plural = verbose_name


class TableRelation(TableBaseModel):
    # 两表之间的关联关系 ForeignKey or OneToOne
    parent_table = models.ForeignKey(to=TableClassify, on_delete=models.CASCADE, related_name="parent",
                                     verbose_name="主表ID")
    child_table = models.ForeignKey(to=TableClassify, on_delete=models.CASCADE, related_name="child",
                                    verbose_name="子表ID")
    is_foreign_key = models.BooleanField(default=True, verbose_name='是ForeignKey')

    class Meta:
        unique_together = ('parent_table', 'child_table')
        verbose_name = '表关联'
        verbose_name_plural = verbose_name


class AssetsRelation(TableBaseModel):
    # 资产关系对应表
    parent_asset = models.ForeignKey(to=TableData, on_delete=models.CASCADE, related_name="parent",
                                     verbose_name="主记录ID")
    child_asset = models.ForeignKey(to=TableData, on_delete=models.CASCADE, related_name="child",
                                    verbose_name="主记录ID")
    table_relation = models.ForeignKey(to=TableRelation, on_delete=models.CASCADE, verbose_name="表关系")

    class Meta:
        unique_together = ('parent_asset', 'child_asset')
        verbose_name = '数据关联'
        verbose_name_plural = verbose_name


class ChangeRecord(TableBaseModel):
    # 资产变更记录表
    asset_id = models.ForeignKey(to=TableData, on_delete=models.CASCADE, related_name='record', verbose_name='关联资产数据')
    title = models.CharField(max_length=64, verbose_name='变更字段名称')
    detail = models.CharField(max_length=1024, verbose_name='变更详情')


######
class CMDBBase(BaseModel):

    class Meta:
            verbose_name = "CMDB基表"
            verbose_name_plural = verbose_name
# class CMDBBase(BaseModel):
#     CHOICE_TYPE = (
#         ("idc", "IDC机房"),
#         ("cloud", "云主机"),
#         ("container", "容器"),
#     )
#     CHOICE_STATE = (
#         ("running", "运行"),
#         ("stopped", "停止"),
#     )
#     CHOICE_PLATFORM = (
#         ("aws", "亚马逊"),
#         ("ali", "阿里云"),
#         ("ten", "腾讯云"),
#         ("hw", "华为云"),
#         ("azure", "微软云"),
#         ("other", "其它"),
#     )
#     CHOICE_INSTANCE_CHARGE_TYPE = (
#         ('PrePaid', '包年包月'),
#         ('PostPaid', '按量'),
#     )
#
#     # common
#     private_ip = models.GenericIPAddressField(unique=True, db_index=True, verbose_name="私有IP地址")
#     public_ip = models.CharField(max_length=100, null=True, blank=True, verbose_name="公网IP地址")
#     eip_ip = models.CharField(max_length=100, null=True, blank=True, verbose_name="弹性IP地址")
#     extra_private_ip = models.JSONField(default=JSONMulFieldDefault, null=True, blank=True, verbose_name='扩展私有IP')
#     extra_public_ip = models.JSONField(default=JSONMulFieldDefault, null=True, blank=True, verbose_name='扩展公网IP')
#     hostname = models.CharField(max_length=100, db_index=True, verbose_name="主机名")
#     cpu_total = models.IntegerField(verbose_name="CPU(核)")
#     mem_total = models.FloatField(verbose_name="内存(G)")
#     state = models.CharField(max_length=50, choices=CHOICE_STATE, verbose_name="运行状态")
#     type = models.CharField(max_length=50, choices=CHOICE_TYPE, verbose_name="机器类型")
#     platform = models.CharField(max_length=50, choices=CHOICE_PLATFORM, default=0, verbose_name="平台")
#     os_system = models.CharField(verbose_name='操作系统', max_length=16, null=True, blank=True)
#     os_version = models.CharField(verbose_name='系统版本', max_length=64, blank=True, null=True)
#     disks = models.JSONField(default=JSONMulFieldDefault, verbose_name='磁盘')
#     create_user = models.CharField(max_length=100, null=True, blank=True, verbose_name='创建用户')
#     is_deleted = models.BooleanField(default=False, verbose_name='是否删除')
#
#     # idc & cloud
#     region_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="机房/地域")
#     zone_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="位置/可用区")
#
#     # cloud server
#     instance_id = models.CharField(verbose_name='实例ID', max_length=64, blank=True, null=True)
#     instance_type = models.CharField(verbose_name='实例类型', max_length=64, blank=True, null=True)
#     image_id = models.CharField(max_length=64, blank=True, null=True, verbose_name='镜像ID')
#     security_group_ids = models.JSONField(default=JSONMulFieldDefault, blank=True, null=True, verbose_name='安全组')
#
#     vpc_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='VPC ID')
#     subnet_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='交换机ID')
#     instance_charge_type = models.CharField(choices=CHOICE_INSTANCE_CHARGE_TYPE,
#                                             null=True,
#                                             blank=True,
#                                             max_length=32,
#                                             verbose_name='主机付费类型'
#                                             )
#     account = models.CharField(max_length=50, null=True, blank=True, verbose_name='云账号')
#     root_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='主账号ID')
#
#     start_time = models.CharField(max_length=100, default="0000-00-00 00:00:00", null=True, blank=True,
#                                   verbose_name='实例启动时间')
#     create_server_time = models.CharField(max_length=100, default="0000-00-00 00:00:00", verbose_name='实例创建时间')
#     expired_time = models.CharField(max_length=32, null=True, blank=True, verbose_name='过期时间')
#
#     def __str__(self):
#         return '{} | {} | {}'.format(self.hostname, self.private_ip, self.get_type_display())
#
#     class Meta:
#         verbose_name = "CMDB基表"
#         verbose_name_plural = verbose_name
#
#
# class JoinCMDBBaseTag(BaseTagModel):
#     cmdb = models.ForeignKey(to=CMDBBase, on_delete=models.CASCADE, verbose_name='CMDB基表')
#
#     def __str__(self):
#         return '{} | {}'.format(self.key, self.value)
#
#     class Meta:
#         verbose_name = "Tag"
#         verbose_name_plural = verbose_name
