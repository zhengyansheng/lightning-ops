import json

from rest_framework.decorators import action

from base.response import json_ok_response, json_error_response
from base.views import BaseModelViewSet
from ..models import TableClassify, TableRelation
from ..serializers import TableClassifySerializer
from ..verify.operate import OperateInstance


class TableClassifyViewSet(BaseModelViewSet):
    queryset = TableClassify.objects.filter(is_deleted=False).order_by('id')
    serializer_class = TableClassifySerializer
    ordering_fields = ('id', 'name', 'pid')
    filter_fields = ('id', 'name', 'pid')
    search_fields = ('name',)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        field_obj = OperateInstance.get_table_field(instance.id)
        if field_obj:
            data['rules'] = field_obj.rules
            data['fields'] = field_obj.fields
        else:
            data['rules'] = None
            data['fields'] = None
        children_all = OperateInstance.get_table_relation_list(instance.id)
        data['children'] = []
        data['relevant'] = []
        if children_all:
            for item in children_all:
                dic = self.get_serializer(item.child_table).data
                dic['parent_name'] = item.child_table.pid.name
                dic['is_foreign_key'] = item.is_foreign_key
                data['children'].append(dic)

        relevant_all = OperateInstance.get_table_relation_list_c(instance.id)
        if relevant_all:
            for item in children_all:
                dic = self.get_serializer(item.parent_table).data
                dic['parent_name'] = item.parent_table.pid.name
                dic['is_foreign_key'] = item.is_foreign_key
                data['relevant'].append(dic)

        return json_ok_response(data)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     data = []
    #     for item in json.loads(json.dumps(serializer.data)):
    #         if not item['pid']:
    #             for dic in data:
    #                 if dic['id'] == item['id']:
    #                     break
    #             else:
    #                 item['children'] = []
    #                 data.append(item)
    #         else:
    #             for i, dic in enumerate(data):
    #                 print(data)
    #                 if dic['id'] == item['pid']:
    #                     data[i]['children'].append(item)
    #                     break
    #             else:
    #                 parent_data = self.get_serializer(OperateInstance.get_table_classify(item['pid']))
    #                 tmp_data = json.loads(json.dumps(parent_data.data))
    #                 tmp_data['children'] = []
    #                 tmp_data['children'].append(item)
    #                 data.append(tmp_data)
    #     return json_ok_response(data)

    @action(methods=['get'], detail=False)
    def tree(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        data = []
        for item in json.loads(json.dumps(serializer.data)):
            if not item['pid']:
                for dic in data:
                    if dic['id'] == item['id']:
                        break
                else:
                    item['children'] = []
                    data.append(item)
            else:
                for i, dic in enumerate(data):
                    print(data)
                    if dic['id'] == item['pid']:
                        data[i]['children'].append(item)
                        break
                else:
                    parent_data = self.get_serializer(OperateInstance.get_table_classify(item['pid']))
                    tmp_data = json.loads(json.dumps(parent_data.data))
                    tmp_data['children'] = []
                    tmp_data['children'].append(item)
                    data.append(tmp_data)
        return json_ok_response(data)

    def create(self, request, *args, **kwargs):
        data = request.data
        pid = data.get('pid')

        # 如果新建数据存在PID
        if pid:
            # 查询 id = pid 的实例, 如果实例的PID不为Null则返回错误
            if OperateInstance.get_table_classify(pid).pid:
                return json_error_response(f'指定的pid:({pid}) 不是主分类表.')

        return super(TableClassifyViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        pid = request.data.get('pid')
        # 判断是否存在PID
        if pid:
            # 查询 pid = instance.id 的表, 如果存在则报错.
            if OperateInstance.get_children_table_classify(instance.id):
                return json_error_response('无法修改, 此类型表存在子分类表.')
            # 获取要要指定为主类的实例, 并判断是否为主类 也就是 PID == Null
            parent_table_classify = OperateInstance.get_table_classify(pid)
            if not parent_table_classify or parent_table_classify.pid:
                return json_error_response('指定的 pid 不存在或者不是主分类表.')
        return super(TableClassifyViewSet, self).update(request, *args, **kwargs)

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     if instance.pid:
    #         parent_table_all = OperateInstance.get_parent_table_relation(instance.id)
    #         child_table_all = OperateInstance.get_child_table_relation(instance.id)
    #         if parent_table_all:
    #             for p_instance in parent_table_all:
    #                 if p_instance.child_table.is_forbid_bind:
    #                     TableData.objects.filter(table_classify_id=p_instance.child_table.id).update(is_deleted=True)
    #                     p_instance.child_table.is_deleted = True
    #
    #                 AssetsRelation.objects.filter(table_relation_id=p_instance.id).update(is_deleted=True)
    #                 p_instance.is_deleted = True
    #                 p_instance.save()
    #
    #         elif child_table_all and len(child_table_all) == 1:
    #             AssetsRelation.objects.filter(table_relation_id=child_table_all[0].id).update(is_deleted=True)
    #             child_table_all[0].is_deleted = True
    #             child_table_all[0].save()
    #         else:
    #             return json_error_response("指定的类型绑定了多个主类型表,请先手动解绑后在删除.")
    #
    #     else:
    #         if OperateInstance.get_children_table_classify(instance.id):
    #             return json_error_response('删除主类型请先该主类型下所属的子类型.')
    #
    #     TableData.objects.filter(table_classify=instance.id).update(is_deleted=True)
    #     instance.is_deleted = True
    #     instance.save()
    #     return json_ok_response('删除成功')

    @action(methods=['post'], detail=False)
    def relation(self, request, *args, **kwargs):
        data = request.data
        parent_table_id = data['parent_table_id']
        child_table_id = data['child_table_id']
        if not parent_table_id or not child_table_id:
            return json_error_response('parent_table_id and child_table_id 是必传参数.')

        parent_classify = OperateInstance.get_table_classify(parent_table_id)
        child_classify = OperateInstance.get_table_classify(child_table_id)

        # 验证表是否存在
        if not parent_classify or not child_classify:
            return json_error_response('parent分类表或者child分类表不存在')

        # 验证 有主分类表
        if not parent_classify.pid or not child_classify.pid:
            return json_error_response('parent分类表或者child分类表是主分类表, 不允许进行绑定操作.')

        # 验证 是否禁止绑定.
        if parent_classify.is_forbid_bind or child_classify.is_forbid_bind:
            return json_error_response('parent分类表或者child分类表,禁止绑定操作.')

        # 验证是否存在字段表
        parent_field = OperateInstance.get_table_field(parent_table_id)
        child_field = OperateInstance.get_table_field(child_table_id)
        if not parent_field or not child_field:
            return json_error_response('parent类型表或者child类型表没有字段表')

        table_relation_obj = TableRelation.objects.create(parent_table_id=parent_table_id,
                                                          child_table_id=child_table_id,
                                                          is_foreign_key=data.get('is_foreign_key'))
        table_relation_obj.save()

        if request.data.get('is_forbid_bind'):
            child_classify.is_forbid_bind = True
            child_classify.save()

        return json_ok_response('关联成功')

    @action(methods=['delete'], detail=False, url_path='un-relation')
    def un_relation(self, request, *args, **kwargs):
        data = request.data

        parent_table_id = data['parent_table_id']
        child_table_id = data['child_table_id']
        if not parent_table_id or not child_table_id:
            return json_error_response('parent_table_id and child_table_id 是必传参数.')

        classify_relation_obj = OperateInstance.get_table_relation(parent_table_id, child_table_id)
        if not classify_relation_obj:
            return json_error_response(
                f'找不到parent_table_id为:{parent_table_id}, child_table_id为: {child_table_id} 关系记录')

        # 找到绑定资产记录并删除
        asset_relation_all = OperateInstance.get_asset_relation(classify_relation_obj)
        if asset_relation_all:
            for instance in asset_relation_all:
                instance.delete()

        classify_relation_obj.delete()

        # 修改 child_classify_obj 的值
        child_classify_obj = OperateInstance.get_table_classify(child_table_id)
        if child_classify_obj.is_forbid_bind:
            child_classify_obj.is_forbid_bind = False
            child_classify_obj.save()

        return json_ok_response('解除关联成功')
