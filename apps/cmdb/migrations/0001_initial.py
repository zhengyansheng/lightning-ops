# Generated by Django 3.1.2 on 2021-06-28 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TableClassify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='变更时间')),
                ('remark', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='名称')),
                ('alias', models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='别名')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='cmdb/icon/%Y/%m/%d/')),
                ('record_log', models.BooleanField(default=False, verbose_name='是否记录日志')),
                ('is_forbid_bind', models.BooleanField(default=False, verbose_name='是否允许绑定')),
                ('pid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdb.tableclassify', verbose_name='父Id')),
            ],
            options={
                'verbose_name': '表分类',
                'verbose_name_plural': '表分类',
            },
        ),
        migrations.CreateModel(
            name='TableRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='变更时间')),
                ('remark', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('is_foreign_key', models.BooleanField(default=True, verbose_name='是ForeignKey')),
                ('child_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child', to='cmdb.tableclassify', verbose_name='子表ID')),
                ('parent_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='cmdb.tableclassify', verbose_name='主表ID')),
            ],
            options={
                'verbose_name': '表关联',
                'verbose_name_plural': '表关联',
                'unique_together': {('parent_table', 'child_table')},
            },
        ),
        migrations.CreateModel(
            name='TableField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='变更时间')),
                ('remark', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('fields', models.JSONField(default=dict, verbose_name='字段元数据')),
                ('rules', models.JSONField(default=dict, verbose_name='字段验证规则')),
                ('table_classify', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='cmdb.tableclassify', verbose_name='关联Classify')),
            ],
            options={
                'verbose_name': '表字段',
                'verbose_name_plural': '表字段',
            },
        ),
        migrations.CreateModel(
            name='TableData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='变更时间')),
                ('remark', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('data', models.JSONField(default=dict, verbose_name='数据值')),
                ('is_forbid_bind', models.BooleanField(default=False, verbose_name='是否允许绑定')),
                ('table_classify', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.tableclassify', verbose_name='关联Classify')),
            ],
            options={
                'verbose_name': '表数据',
                'verbose_name_plural': '表数据',
            },
        ),
        migrations.CreateModel(
            name='ChangeRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='变更时间')),
                ('remark', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('title', models.CharField(max_length=64, verbose_name='变更字段名称')),
                ('detail', models.CharField(max_length=1024, verbose_name='变更详情')),
                ('operator', models.CharField(default='Agent', max_length=64, verbose_name='操作用户')),
                ('table_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='record', to='cmdb.tabledata', verbose_name='关联资产数据')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AssetsRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='变更时间')),
                ('remark', models.CharField(blank=True, max_length=1024, null=True, verbose_name='备注')),
                ('child_asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child', to='cmdb.tabledata', verbose_name='主记录ID')),
                ('parent_asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='cmdb.tabledata', verbose_name='主记录ID')),
                ('table_relation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.tablerelation', verbose_name='表关系')),
            ],
            options={
                'verbose_name': '数据关联',
                'verbose_name_plural': '数据关联',
                'unique_together': {('parent_asset', 'child_asset')},
            },
        ),
    ]
