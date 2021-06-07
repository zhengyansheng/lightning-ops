from rest_framework import serializers

from .models import CMDBBase
from .models import TableClassify
from .models import TableField
from .models import TableData

# from apps.cmdb.verify.check_filed import check_field
# from apps.cmdb.verify.check_data import check_data
# from apps.cmdb.verify.operate import OperateInstance



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



class TableClassifyModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TableClassify
        fields = "__all__"


class TableFieldModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TableField
        fields = "__all__"


class TableDataModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TableData
        fields = "__all__"
