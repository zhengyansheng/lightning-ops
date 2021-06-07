from django.contrib import admin


from . import models
# Register your models here.

#
# @admin.register(models.TableClassify)
# class TableClassifyAdmin(admin.ModelAdmin):
#     list_display = (
#         "pk",
#         "name",
#         "pid",
#     )
#
#     search_fields = (
#         'name',
#     )
#
#
# @admin.register(models.TableField)
# class TableFieldAdmin(admin.ModelAdmin):
#     list_display = (
#         "pk",
#         "classify",
#         "fields",
#         "rules",
#     )
#
#
# @admin.register(models.TableData)
# class TableDataAdmin(admin.ModelAdmin):
#     list_display = (
#         "pk",
#         "classify",
#         "data",
#         "is_deleted",
#     )
#
#
# @admin.register(models.TableRelation)
# class TableRelationAdmin(admin.ModelAdmin):
#     list_display = (
#         "pk",
#         "parent_table_id",
#         "child_table_id",
#         "is_foreign_key",
#     )
#
#
# @admin.register(models.AssetsRelation)
# class AssetsRelationAdmin(admin.ModelAdmin):
#     list_display = (
#         "pk",
#         "parent_asset_id",
#         "child_asset_id",
#         # "table_relation",
#     )