# Generated by Django 3.1.2 on 2021-03-31 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0010_auto_20210324_1656'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cmdbbase',
            name='region_name',
        ),
        migrations.RemoveField(
            model_name='cmdbbase',
            name='zone_name',
        ),
        migrations.AlterField(
            model_name='cmdbbase',
            name='region_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='机房/地域'),
        ),
        migrations.AlterField(
            model_name='cmdbbase',
            name='zone_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='位置/可用区'),
        ),
    ]