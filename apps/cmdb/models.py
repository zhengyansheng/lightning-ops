from django.db import models

# Create your models here.
from base.models import BaseModel

__all__ = ['TableClassify', 'TableField', 'TableData', 'TableRelation', 'AssetsRelation']


class TableBaseModel(BaseModel):
    is_deleted = models.BooleanField(default=False, verbose_name='已删除')

    class Meta:
        abstract = True


class TableClassify(TableBaseModel):
    # 分类表
    name = models.CharField(max_length=32, unique=True, verbose_name='名称')
    alias = models.CharField(max_length=32, unique=True, verbose_name='别名', null=True, blank=True)
    pid = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='父Id')
    icon = models.ImageField(upload_to="cmdb/icon/%Y/%m/%d/", blank=True, null=True)
    record_log = models.BooleanField(default=False, verbose_name='是否记录日志')
    is_forbid_bind = models.BooleanField(default=False, verbose_name='是否允许绑定')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '表分类'
        verbose_name_plural = verbose_name


class TableField(TableBaseModel):
    # 表字段 和 验证规则
    table_classify = models.OneToOneField(to=TableClassify, on_delete=models.CASCADE, verbose_name='关联Classify',
                                          related_name='fields')
    # name / order
    fields = models.JSONField(default=dict, verbose_name='字段元数据', )
    rules = models.JSONField(default=dict, verbose_name='字段验证规则')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = '表字段'
        verbose_name_plural = verbose_name


class TableData(TableBaseModel):
    # 表数据
    table_classify = models.ForeignKey(to=TableClassify, on_delete=models.CASCADE, verbose_name='关联Classify')
    data = models.JSONField(default=dict, verbose_name='数据值')

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        verbose_name = '表数据'
        verbose_name_plural = verbose_name


class TableRelation(TableBaseModel):
    # 两表之间的关联关系 ForeignKey or OneToOne
    parent_table = models.ForeignKey(to=TableClassify, on_delete=models.CASCADE, related_name='parent',
                                     verbose_name='主表ID')
    child_table = models.ForeignKey(to=TableClassify, on_delete=models.CASCADE, related_name='child',
                                    verbose_name='子表ID')
    is_foreign_key = models.BooleanField(default=True, verbose_name='是ForeignKey')

    class Meta:
        unique_together = ('parent_table', 'child_table')
        verbose_name = '表关联'
        verbose_name_plural = verbose_name


class AssetsRelation(TableBaseModel):
    # 资产关系对应表
    parent_asset = models.ForeignKey(to=TableData, on_delete=models.CASCADE, related_name='parent',
                                     verbose_name='主记录ID')
    child_asset = models.ForeignKey(to=TableData, on_delete=models.CASCADE, related_name='child',
                                    verbose_name='主记录ID')
    table_relation = models.ForeignKey(to=TableRelation, on_delete=models.CASCADE, verbose_name='表关系')

    class Meta:
        unique_together = ('parent_asset', 'child_asset')
        verbose_name = '数据关联'
        verbose_name_plural = verbose_name


class ChangeRecord(TableBaseModel):
    # 资产变更记录表
    table_data = models.ForeignKey(to=TableData, on_delete=models.CASCADE, related_name='record', verbose_name='关联资产数据')
    title = models.CharField(max_length=64, verbose_name='变更字段名称')
    detail = models.CharField(max_length=1024, verbose_name='变更详情')
    operator = models.CharField(max_length=64, verbose_name='操作用户', default='Agent')
