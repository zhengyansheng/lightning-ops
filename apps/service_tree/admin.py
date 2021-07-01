from .models import ServiceTree
from .models import NodeJoinTag
from .models import NodeLinkServer
from .models import NodeLinkOperaPermission

from django.contrib import admin
from mptt.admin import MPTTModelAdmin


# Register your models here.


@admin.register(ServiceTree)
class ServiceTreeAdmin(MPTTModelAdmin):
    readonly_fields = ('appkey', "abspath")


@admin.register(NodeLinkOperaPermission)
class NodeOwnerAdmin(admin.ModelAdmin):
    list_display = (
        "node",
        "read_member_custom",
        "write_member_custom",
    )
    filter_horizontal = ('read_member', "write_member")

    def read_member_custom(self, obj):
        member = obj.read_member.all()
        return [m.username for m in member]

    def write_member_custom(self, obj):
        member = obj.write_member.all()
        return [m.username for m in member]

    read_member_custom.short_description = "读权限"
    write_member_custom.short_description = "写权限"


@admin.register(NodeLinkServer)
class NodeLinkServerAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "node",
        # "cmdbs_custom",
    )

    # filter_horizontal = ('cmdbs',)
    #
    # def cmdbs_custom(self, obj):
    #     return [m.hostname for m in obj.cmdbs.all()]

    # cmdbs_custom.short_description = "Server标识"


@admin.register(NodeJoinTag)
class NodeJoinTagAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "node",
        "key",
        "value",
    )
