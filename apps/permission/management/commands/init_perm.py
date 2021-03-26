import random
import string

from apps.user.models import UserProfile
from apps.permission.models import Role, PermRule, RoleBind

from django.core.management.base import BaseCommand, CommandError


def get_pwd(pos=10):
    a = string.ascii_letters + string.digits
    key = random.sample(a, pos)
    keys = "".join(key)
    return keys


class Command(BaseCommand):
    """
    创建admin用户，admin角色， admin权限
    """
    help = '创建admin用户，admin角色， admin权限'

    def handle(self, *args, **options):
        username = "admin"
        pwd = get_pwd()
        role = "admin:role"
        perm = "超级管理员权限"
        email = 'admin@51Reboot.com'

        u = UserProfile.objects.create(username=username, email=email, phone="13333333333")
        u.set_password(pwd)
        u.save()

        r = Role.objects.create(name=role)
        r.save()

        p = PermRule.objects.create(name=perm, path="*", method="*")
        p.role.add(r)
        p.save()

        rb = RoleBind.objects.create(user=u, role=r)
        rb.save()

        # TODO 创建前端路由到数据库中
        print('创建用户完成')
        print('用户名: ', username)
        print('密  码: ', pwd)


