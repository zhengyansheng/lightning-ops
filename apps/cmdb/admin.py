from django.contrib import admin

# Register your models here.
from . import models


# for table in models.__all__:
#     admin.site.register(getattr(models,table))


@admin.register(models.TableClassify)
class TableClassifyAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "alias",
        "pid",
        "icon",
    )


@admin.register(models.TableField)
class TableFieldAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "table_classify",
        "fields",
        "rules",
    )


@admin.register(models.TableData)
class TableDataAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "table_classify",
        "data",
    )
