from collections import OrderedDict

from django.db.models import Q
from django.forms.models import model_to_dict

from ..models import TableClassify, TableField, TableData, AssetsRelation, TableRelation


class OperateInstance:
    @staticmethod
    def get_table_classify(id):
        """通过ID 查找指定分类表"""
        return TableClassify.objects.filter(id=id).first()

    # 获取类型表的 子表
    @staticmethod
    def get_children_table_classify(p_tid):
        """通过 主表ID 查找 子分类表"""
        children_table_classify = TableClassify.objects.filter(pid=p_tid)
        if children_table_classify:
            return children_table_classify
        return None

    @staticmethod
    def get_parent_table_classify(pid):
        parent_table_classify_obj = TableClassify.objects.filter(id=pid).first()
        if parent_table_classify_obj:
            return parent_table_classify_obj
        return None

    # parent_table

    @staticmethod
    def get_parent_table_relation(pid):
        parent_relation_obj = TableRelation.objects.filter(parent_table_id=pid)
        if parent_relation_obj:
            return parent_relation_obj
        return None

    @staticmethod
    def get_child_table_relation(cid):
        """通过child_table_id获取表关系记录"""
        child_table_obj = TableRelation.objects.filter(child_table_id=cid)
        if child_table_obj:
            return child_table_obj
        return None

    @staticmethod
    def get_table_relation(pid, cid):
        """根据 parent_table_id 和 child_table_id 返回分类关系表"""
        table_relation_obj = TableRelation.objects.filter(
            parent_table_id=pid, child_table_id=cid
        ).first()
        if table_relation_obj:
            return table_relation_obj
        return None

    @staticmethod
    def get_abs_asset_relation(p_id, c_id):
        """根据 table_relation_id parent_asset_id child_asset_id 查询asset_relation记录"""
        asset_relation = AssetsRelation.objects.filter(
            parent_asset_id=p_id, child_asset_id=c_id
        ).first()
        if asset_relation:
            return asset_relation
        return None

    @staticmethod
    def get_asset_relation(t_id):
        """
        根据 table_relation_id 查找 资产绑定记录
        """
        asset_relation = AssetsRelation.objects.filter(table_relation_id=t_id)
        if asset_relation:
            return asset_relation
        return None

    @staticmethod
    def get_parent_asset_relation(t_id, p_id):
        """根据 表关系ID 主资产ID,  获取资产数据"""
        asset_relation = AssetsRelation.objects.filter(
            table_relation_id=t_id, parent_asset_id=p_id
        )
        if asset_relation:
            return asset_relation
        return None

    @staticmethod
    def get_child_asset_relation(t_id, c_id):
        """根据 表关系ID 子资产ID 获取资产数据"""
        asset_relation = AssetsRelation.objects.filter(
            table_relation_id=t_id, child_asset_id=c_id
        )
        if asset_relation:
            return asset_relation
        return None

    @staticmethod
    def get_c_asset_relation(c_id):
        """根据 子资产ID 获取资产数据"""
        asset_relation = AssetsRelation.objects.filter(child_asset_id=c_id)
        if asset_relation:
            return asset_relation
        return None

    # @staticmethod
    # def create_asset(c_id, *args):
    #     asset_obj = Asset.objects.create(asset_key=get_md5(*args), classify_id_id=c_id)
    #     asset_obj.save()
    #     return asset_obj

    @staticmethod
    def get_asset(id):
        """根据 ID 获取资产记录"""
        asset_obj = TableData.objects.filter(id=id).first()
        if asset_obj:
            return asset_obj
        return None

    @staticmethod
    def get_classify_asset(id, cid):
        """根据 分类表ID 资产表 ID 获取资产数据"""
        asset_obj = TableData.objects.filter(id=id, table_classify_id=cid).first()
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
        """根据分类表ID返回 fields 字段表"""
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
        """查询 parent_asset_id 或者 child_asset_id 等于指定id的资产"""
        field_all = AssetsRelation.objects.filter(
            Q(parent_asset_id=c_id) | Q(child_asset_id=c_id)
        )
        if field_all:
            return field_all
        return None

    @staticmethod
    def get_p_relation_asset(id, pid):
        """通过主资产ID 和 分类ID 查询关联下 所有的数据"""
        # 获取关联数据类型
        table_relation = OperateInstance.get_parent_table_relation(pid)
        l_c = []
        if table_relation:
            for t_r in table_relation:
                asset_re_all = OperateInstance.get_parent_asset_relation(t_r.id, id)
                data = OrderedDict()
                if not asset_re_all:
                    data["table_name"] = t_r.child_table.name
                    data["table_id"] = t_r.child_table.id
                    data["parent_table_name"] = t_r.child_table.pid.name
                    data["fields"] = t_r.child_table.fields.fields
                    data["data"] = []
                    l_c.append(data)
                    continue
                data["table_name"] = t_r.child_table.name
                data["table_id"] = t_r.child_table.id
                data["parent_table_name"] = t_r.child_table.pid.name
                data["fields"] = t_r.child_table.fields.fields
                data["data"] = [model_to_dict(i.child_asset) for i in asset_re_all]
                l_c.append(data)
            return l_c
        return None

    def get_c_relation_asset(id, cid):
        """通过子资产ID 和 分类ID 查询关联下 所有的数据"""
        table_relation = OperateInstance.get_child_table_relation(cid)
        l_c = []
        if table_relation:
            for t_r in table_relation:
                asset_re_all = OperateInstance.get_child_asset_relation(t_r.id, id)
                if not asset_re_all:
                    continue
                data = OrderedDict()
                data["table_name"] = t_r.parent_table.name
                data["parent_table_name"] = t_r.parent_table.pid.name
                data["fields"] = t_r.parent_table.fields.fields
                data["data"] = [model_to_dict(i.parent_asset) for i in asset_re_all]
                l_c.append(data)
            return l_c
        return None

    @staticmethod
    def get_table_relation_list(pid):
        parent_relation_obj = TableRelation.objects.filter(parent_table_id=pid)
        if parent_relation_obj:
            return parent_relation_obj
        return []

    def get_table_relation_list_c(cid):
        parent_relation_obj = TableRelation.objects.filter(child_table_id=cid)
        if parent_relation_obj:
            return parent_relation_obj
        return []
