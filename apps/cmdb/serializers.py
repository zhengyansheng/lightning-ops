from rest_framework import serializers

from .models import CMDBBase

region_id_map = {
    "ali": {
        "cn-beijing": "北京",
    },
    "ten": {
        "ap-beijing": "北京",
        "ap-shanghai": "上海",
        "ap-hangzhou": "杭州",
    }
}

zone_id_map = {
    "ali": {
        "c": "三区",
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


class CMDBBulkListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        instance_mapping = {ins.private_ip: ins for ins in instance}
        data_mapping = {item['private_ip']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for pk, data in data_mapping.items():
            obj = instance_mapping.get(pk, None)
            if obj:
                ret.append(self.child.update(obj, data))
            else:
                ret.append(self.child.create(data))

        return ret

    def example_update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        instance_mapping = {ins.private_ip: ins for ins in instance}
        data_mapping = {item['private_ip']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for pk, data in data_mapping.items():
            obj = instance_mapping.get(pk, None)
            if obj is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(obj, data))

        # Perform deletions.
        for pk, ins in instance_mapping.items():
            if pk not in data_mapping:
                ins.delete()

        return ret

    def to_internal_value(self, data):
        return data


class CMDBBaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMDBBase
        fields = "__all__"
        depth = 2
        list_serializer_class = CMDBBulkListSerializer
