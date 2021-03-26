from base.models import BaseModel
from apps.user.models import UserProfile

from django.db import models


class Role(BaseModel):
    """角色"""
    name = models.CharField(verbose_name='名称', help_text='名称', max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'role'
        unique_together = ('name',)
        verbose_name = verbose_name_plural = '角色'


class PermRule(BaseModel):
    """API权限"""
    name = models.CharField(verbose_name='名称', help_text='名称', max_length=256)
    ptype = models.CharField(max_length=1, default="p", verbose_name="权限类型")
    role = models.ManyToManyField(to=Role, related_name="perm_rule", blank=True, verbose_name="角色")
    path = models.CharField(max_length=128, verbose_name="api路径")
    method = models.CharField(max_length=128, verbose_name="请求方法")

    def __str__(self):
        return self.name

    def adapter(self):
        return [{
            "ptype": self.ptype,
            "role": role.name,
            "path": self.path,
            "method": self.method,
        } for role in self.role.all()]

    class Meta:
        db_table = 'perm_rule'
        verbose_name_plural = verbose_name = '权限规则'
        unique_together = ('name', 'path', 'method')


class RoleBind(BaseModel):
    """角色绑定用户"""
    ptype = models.CharField(max_length=1, default="g", verbose_name="权限类型")
    user = models.ForeignKey(to=UserProfile, verbose_name="用户", related_name="role_bind", on_delete=models.CASCADE)
    role = models.ForeignKey(to=Role, verbose_name="角色", related_name="role_bind", on_delete=models.CASCADE)

    def __str__(self):
        return "{}-{}".format(self.ptype, self.role)

    def adapter(self):
        return [{
            "ptype": self.ptype,
            "user": self.user.username,
            "role": self.role.name,
        }]

    class Meta:
        db_table = 'role_bind'
        verbose_name_plural = verbose_name = '角色绑定'
        unique_together = ("user", "role")


class Router(BaseModel):
    title = models.CharField(max_length=128, verbose_name="标题", help_text='标题')
    index = models.CharField(max_length=64, verbose_name="索引", help_text='索引')
    desc = models.CharField(max_length=256, verbose_name="描述", help_text='描述', null=True, blank=True)
    icon = models.CharField(max_length=256, verbose_name="图表", help_text="图表", null=True, blank=True)
    routeName = models.CharField(max_length=128, verbose_name="路由名", help_text="路有名", null=True, blank=True)
    go = models.CharField(max_length=128, verbose_name="URL", help_text="URL", null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name="父路由", on_delete=models.CASCADE)
    isParent = models.BooleanField(verbose_name="是否顶级路由", default=True)
    role = models.ManyToManyField(to=Role, related_name="router", blank=True, verbose_name="角色")

    class Meta:
        db_table = 'route'
        verbose_name_plural = verbose_name = '前端路由'

    def __str__(self):
        return self.title
