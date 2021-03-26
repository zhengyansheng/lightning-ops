from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password
from apps.user.models import UserProfile
from faker import Faker

from common.convert import chinese_to_pinyin


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        password = make_password('123456')
        faker = Faker(locale="zh_CN")
        for _ in range(100):
            pinyin_username = chinese_to_pinyin(faker.name_male())
            data = {
                'name': faker.name_male(),
                'username': pinyin_username,
                'phone': faker.phone_number(),
                'password': password,
                'is_superuser': False,
                'email': "{}@gmail.com".format(pinyin_username),
            }
            try:
                # u = UserProfile.objects.create(**data)
                # u.save()
                u, ok = UserProfile.objects.get_or_create(username=pinyin_username, defaults=data)
                self.stdout.write(self.style.SUCCESS(f'Create user {pinyin_username} {ok}.'))
            except Exception as e:
                raise CommandError('创建失败！', e.args)
