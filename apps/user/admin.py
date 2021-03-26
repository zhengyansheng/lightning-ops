from . import models

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from mptt.admin import MPTTModelAdmin


# Register your models here.


@admin.register(models.Organization)
class OrganizationAdmin(MPTTModelAdmin):
    # 显示
    pass


@admin.register(models.UserProfile)
class UserProfileAdmin(UserAdmin):
    # 显示
    list_display = (
        'pk',
        'username',
        'name',
        'phone',
        'email',
        "department",
    )

    # 编辑布局
    fieldsets = (
        (None, {
            'fields': (
                'username', 'password'
            )
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'name')
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', "department", 'groups', 'user_permissions',
            ),
        }),
        (_('Important dates'), {
            'fields': (
                'last_login', 'date_joined'
            )
        }),
        (_('User Profile'), {
            'fields': (
                'phone', 'staff_id', 'job_status'
            )
        }),
        (_('User Head'), {
            'fields': (
                'image',
            )
        }),
    )
