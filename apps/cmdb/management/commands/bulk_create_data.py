import random
from django.core.management.base import BaseCommand, CommandError

from apps.cmdb.models import CMDBBase


class Command(BaseCommand):
    help = 'Auto bulk insert data to db'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for x in range(3, 254):
            # data = {
            #     "name": "monkey-redis{}.ops.prod.ali".format(x),
            #     "private_ip": "192.168.3.{}".format(x),
            #     "hostname": "monkey-redis{}.ops.prod.ali".format(x),
            #     "mem_total": 16,
            #     "cpu_total": 8,
            #     "type": 3,
            #     "state": 2,
            #     "zone": "wangjing",
            #     "region": "beijing",
            #     "platform": 0,
            # }

            data = {
            	"private_ip": "172.17.118.{}".format(x),
            	"public_ip": "121.4.224.{}".format(random.randint(1, 253)),
            	"extra_private_ip": [],
            	"extra_public_ip": [],
            	"hostname": "monkey-redis{}.ops.prod.ali".format(x),
            	"cpu_total": 1,
            	"mem_total": 2.0,
            	"state": 2,
            	"type": 3,
            	"platform": 2,
            	"os_system": "CentOS",
            	"os_version": "7.8",
            	"disks": [{
            		"disk_type": "system"
            	}],
            	"create_user": "zhengyansheng",
            	"zone_name": "cn-beijing-3",
            	"region_name": "beijing",
            	"instance_id": "i-2zed2cbgi4jowvumrvs9",
            	"instance_type": "ecs.n4.small",
            	"image_id": "centos_7_8_x64_20G_alibase_20200914.vhd",
            	"security_group_ids": ["sg-2zeb9n0qzygmjwn7hwae"],
            	"region_id": "cn-beijing",
            	"zone_id": "cn-beijing-3",
            	"vpc_id": "vpc-2ze80et76jwcsuc2asobq",
            	"subnet_id": "vsw-2zelzctt7aougw3bhz5ev",
            	"instance_charge_type": "PostPaid",
            	"account": "ali.corp",
            	"root_id": "2837484018928304",
            	"create_server_time": "2021-03-24 17:24:00"
            }


            # print(data)
            ins = CMDBBase.objects.create(**data)
            self.stdout.write('Successfully closed poll "%s"' % ins)
