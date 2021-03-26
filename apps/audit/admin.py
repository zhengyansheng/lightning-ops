from .models import AuditLog

from django.contrib import admin

# Register your models here.


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "url",
        "method",
        "query_string",
        "body",
        "remote_ip",
        "username",
        "status_code",
        "create_time",
        "update_time",
    )
