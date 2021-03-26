from . import models

from django.contrib import admin


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "remark",
        "create_time",
        "update_time",
    )


@admin.register(models.PermRule)
class PermRuleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        'remark',
        "path",
        "method",
        "create_time",
        "update_time",
    )


@admin.register(models.RoleBind)
class RoleBindAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "role",
        "create_time",
        "update_time",
    )


@admin.register(models.Router)
class RouteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "index",
        "desc",
        "icon",
        "routeName",
        "go",
        "isParent"
    )