from django.contrib import admin


from . import models
# Register your models here.


@admin.register(models.CMDBBase)
class CMDBBaseAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "private_ip",
        "public_ip",
        "hostname",
        "cpu_total",
        "mem_total",
        "state",
        "region_name",
        "zone_name",
        "type",
    )


@admin.register(models.JoinCMDBBaseTag)
class JoinTagAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "cmdb",
        "key",
        "value",
    )
