from ..models import TableClassify, TableField, TableData, AssetsRelation, TableRelation
from django.db.models import Q


class OperateInstance:
    @staticmethod
    def get_table_classify(id):
        return TableClassify.objects.filter(id=id).first()

    @staticmethod
    def get_parent_table_classify(pid):
        parent_table_classify_obj = TableClassify.objects.filter(id=pid).first()
        if parent_table_classify_obj:
            return parent_table_classify_obj
        return None

    @staticmethod
    def get_children_table_classify(id):
        children_table_classify = TableClassify.objects.filter(pid=id)
        if children_table_classify:
            return children_table_classify
        return None

    # parent_table

    @staticmethod
    def get_parent_table_relation(pid):
        parent_relation_obj = TableRelation.objects.filter(parent_table_id=pid)
        if parent_relation_obj:
            return parent_relation_obj
        return None

    @staticmethod
    def get_child_table_relation(pid):
        child_table_obj = TableRelation.objects.filter(child_table_id=pid)
        if child_table_obj:
            return child_table_obj
        return None

    @staticmethod
    def get_asset_relation(t_id):
        asset_relation = AssetsRelation.objects.filter(table_relation=t_id)
        if asset_relation:
            return asset_relation
        return None

    @staticmethod
    def get_parent_asset_relation(t_id, p_id):
        asset_relation = AssetsRelation.objects.filter(table_relation=t_id, parent_asset_id=p_id)
        if asset_relation:
            return asset_relation
        return None

    # @staticmethod
    # def create_asset(c_id, *args):
    #     asset_obj = Asset.objects.create(asset_key=get_md5(*args), classify_id_id=c_id)
    #     asset_obj.save()
    #     return asset_obj

    @staticmethod
    def get_asset(id, c_id):
        asset_obj = TableData.objects.filter(id=id).first()
        if asset_obj:
            return asset_obj
        return None

    @staticmethod
    def get_all_asset(s_id):
        asset_all_obj = TableData.objects.filter(table_classify_id=s_id)
        if asset_all_obj:
            return asset_all_obj
        return None

    @staticmethod
    def get_table_field(c_id):
        field_obj = TableField.objects.filter(table_classify_id=c_id).first()
        if field_obj:
            return field_obj

        return None

    @staticmethod
    def get_all_field_map(c_id):
        field_all = TableClassify.objects.filter(id=c_id).values()
        if field_all:
            return field_all
        return None

    @staticmethod
    def get_asset_relation_exists(c_id):
        field_all = AssetsRelation.objects.filter(Q(parent_asset_id=c_id) | Q(child_asset_id=c_id))
        if field_all:
            return field_all
        return None
