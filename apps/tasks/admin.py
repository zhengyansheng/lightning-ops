from django.contrib import admin

from . import models
# Register your models here.



@admin.register(models.TaskHistory)
class TaskHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "task_id",
        "task_name",
        "create_user",
        "task_state",
        "src_ip",
        "create_time",
    )