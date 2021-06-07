from rest_framework import serializers

from .models import TableClassify, TableField, TableData, TableRelation, AssetsRelation, ChangeRecord


class TableClassifyS(serializers.ModelSerializer):
    class Meta:
        model = TableClassify
        fields = '__all__'


class TableClassifySerializer(serializers.ModelSerializer):
    class Meta:
        model = TableClassify
        fields = '__all__'


class TableFieldSerializer(serializers.ModelSerializer):
    fields = serializers.JSONField()

    def validate_phone(self, fields):
        return fields

    class Meta:
        model = TableField
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(TableFieldSerializer, self).to_representation(instance)
        representation['parent_table_classify'] = instance.table_classify.pid.name
        return representation


# children
class TableDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableData
        fields = '__all__'


class TableRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableRelation
        fields = '__all__'


class AssetsRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetsRelation
        fields = '__all__'


class ChangeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeRecord
        fields = '__all__'
