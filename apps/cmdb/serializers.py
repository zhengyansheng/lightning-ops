import json

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import CMDBBase

region_id_map = {
    "ali": {

    },
    "ten": {
        "ap-beijing": "北京",
        "ap-shanghai": "上海",
        "ap-hangzhou": "杭州",
    }
}

zone_id_map = {
    "ali": {

    },
    "ten": {
        '1': "一区",
        '2': "二区",
        '3': "三区",
        '4': "四区",
        '5': "五区",
        '6': "六区",
        '7': "七区",
    }
}


class CMDBBaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMDBBase
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):
        response = super(CMDBBaseModelSerializer, self).to_representation(instance)
        response['state'] = dict(self.Meta.model.CHOICE_STATE)[response['state']]
        response['type'] = dict(self.Meta.model.CHOICE_TYPE)[response['type']]
        response['platform'] = dict(self.Meta.model.CHOICE_PLATFORM)[response['platform']]
        return response

    def to_internal_value(self, data):
        data = self.replace_region_zone_name(data)
        data = self.replace_type_platform_state(data)
        print(json.dumps(data, indent=4))
        return super(CMDBBaseModelSerializer, self).to_internal_value(data)

    def replace_region_zone_name(self, data):
        """ 自动生成 region and zone name"""
        if data['type'] == "cloud":
            region_platform_dic = region_id_map[data['platform']]
            zone_platform_dic = zone_id_map[data['platform']]
            data['region_name'] = region_platform_dic[data['region_id']]
            data['zone_name'] = region_platform_dic[data['region_id']] + zone_platform_dic[data['zone_id'][-1]]
        return data

    def replace_type_platform_state(self, data):
        """映射 state | platform | type 字母到数字的映射"""
        state_dic = {x[1]: int(x[0]) for x in self.Meta.model.CHOICE_STATE}
        platform_dic = {x[1]: int(x[0]) for x in self.Meta.model.CHOICE_PLATFORM}
        type_dic = {x[1]: int(x[0]) for x in self.Meta.model.CHOICE_TYPE}

        # 验证
        if data['state'] not in state_dic or data['platform'] not in platform_dic or data['type'] not in type_dic:
            raise ValidationError("xxx")

        data['state'] = state_dic[data['state']]
        data['platform'] = platform_dic[data['platform']]
        data['type'] = type_dic[data['type']]
        return data
