from collections import OrderedDict

from rest_framework.decorators import action

from base.response import json_ok_response, json_error_response
from base.views import BaseModelViewSet
from ..models import TableData, AssetsRelation
from ..serializers import TableDataSerializer
from ..verify.check_data import check_data
from ..verify.operate import OperateInstance
from ..verify.record_log import record


class TableDataViewSet(BaseModelViewSet):
    queryset = TableData.objects.filter(is_deleted=False).order_by('id')
    serializer_class = TableDataSerializer
    ordering_fields = ('id',)
    filter_fields = ('id', 'table_classify_id',)
    search_fields = ('data',)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        table_field_obj = OperateInstance.get_table_field(instance.table_classify.id)
        # if fields_obj:
        #     data['fields'] = OperateInstance.get_table_field(instance.id).fields
        #     data['rules'] = OperateInstance.get_table_field(instance.id).rules

        data = OrderedDict()
        data['table_name'] = instance.table_classify.name
        data['parent_table_name'] = instance.table_classify.pid.name
        data['fields'] = table_field_obj.fields
        data['data'] = serializer.data
        # table_relation = OperateInstance.get_parent_table_relation(instance.table_classify.id)
        # if table_relation:
        #     for t_r in table_relation:
        #         OperateInstance.get_p_relation_asset(instance.id, t_r)
        #
        # else:
        #     data['children'] = None

        data['children'] = OperateInstance.get_p_relation_asset(instance.id, instance.table_classify.id)
        data['relevant'] = OperateInstance.get_c_relation_asset(instance.id, instance.table_classify.id)
        return json_ok_response(data)

    def list(self, request, *args, **kwargs):
        table_classify_id = request.query_params.get('table_classify_id')
        if not table_classify_id:
            return json_error_response('资产查询只能通过分类ID查询.')

        table_obj = OperateInstance.get_table_classify(table_classify_id)

        if not table_obj:
            return json_error_response('找不到指定的分类表')

        table_field_obj = OperateInstance.get_table_field(table_classify_id)
        if not table_field_obj:
            return json_error_response('找不到分类表的字段表')

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = {'data': serializer.data,
                    'fields': table_field_obj.fields,
                    }
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = {'data': serializer.data,
                'fields': table_field_obj.fields,
                'rules': table_field_obj.rules,
                }
        return json_ok_response(data)

    def create(self, request, *args, **kwargs):

        # 校验数据
        try:
            data = check_data(request.data, None)
        except ValueError as e:
            return json_error_response(f'数据校验出错: {str(e)}')

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self.get_success_headers(serializer.data)
        return json_ok_response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            data = check_data(request.data, instance)
        except ValueError as e:
            return json_error_response(f'数据校验出错: {str(e)}')

        if data.get('table_classify') and data.get(
            'table_classify') != instance.table_classify.id:
            return json_error_response('数据不可修改类型, 如需更换请进行删除.')

        partial = kwargs.pop('partial', False)

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        try:
            record('update_data', instance, None, request)
        except Exception as e:
            return json_error_response(f'日志记录出错: {str(e)}')

        return json_ok_response(serializer.data)

    @action(methods=['post'], detail=False)
    def relation(self, request, *args, **kwargs):
        data = request.data

        parent_table_id = data['parent_table_id']
        child_table_id = data['child_table_id']
        table_relation_obj = OperateInstance.get_table_relation(parent_table_id, child_table_id)
        # 判断分类关系绑定表是否存在
        if not table_relation_obj:
            return json_error_response('未查询到分类关系绑定表, 请先进行绑定在进行资产绑定操作.')

        parent_asset_obj = OperateInstance.get_classify_asset(data['parent_asset_id'], parent_table_id)
        child_asset_obj = OperateInstance.get_classify_asset(data['child_asset_id'], child_table_id)

        # 判断资产是否存在
        if not parent_asset_obj or not child_asset_obj:
            return json_error_response('资产数据未查询到.')

        # 判断是否为 OneToOne 如果是则判断是否存在绑定记录
        if not table_relation_obj.is_foreign_key:
            asset_relation_obj = OperateInstance.get_child_asset_relation(table_relation_obj.id, data['child_asset_id'])

            if asset_relation_obj:
                return json_error_response('类型表关联模式为: OneToOne, 子资产数据已经被绑定无法进行二次绑定.')

        try:
            new_asset_relation = AssetsRelation.objects.create(parent_asset=parent_asset_obj,
                                                               child_asset=child_asset_obj,
                                                               table_relation=table_relation_obj)
            new_asset_relation.save()
        except Exception as e:
            return json_error_response(f'数据创建出错: {str(e)}')
        try:
            record('relation', parent_asset_obj, child_asset_obj, request)
        except Exception as e:
            return json_error_response(f'日志记录出错: {str(e)}')
        return json_ok_response('资产数据绑定成功')

    @action(methods=['post'], detail=False, url_path='un-relation')
    def un_relation(self, request, *args, **kwargs):
        data = request.data

        table_relation_obj = OperateInstance.get_table_relation(data['parent_table_id'], data['child_table_id'])

        if not table_relation_obj:
            return json_error_response('未查询到关系, 请先进行绑定在进行资产绑定操作.')

        asset_relation_obj = OperateInstance.get_abs_asset_relation(table_relation_obj.id, data['parent_asset_id'],
                                                                    data['child_asset_id'])

        if not asset_relation_obj:
            return json_error_response('未查询到资产绑定记录, 请检查后重试.')

        asset_relation_obj.delete()

        try:
            record('un_relation', asset_relation_obj, None, request)
        except Exception as e:
            return json_error_response(f'日志记录出错: {str(e)}')
        return json_ok_response('资产关联关系解除成功.')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            record('delete_data', instance, None, request)
        except Exception as e:
            return json_error_response(f'日志记录出错: {str(e)}')

        instance.delete()
        return json_ok_response('删除成功')

    @action(methods=['get'], detail=False)
    def search(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        import json

        data = []
        for item in json.loads(json.dumps(serializer.data)):

            for i, dic in enumerate(data):
                if item['table_classify'] in dic.values():
                    print(data[i])
                    data[i]['data'].append(item['data'])
                    break
            else:
                tmp = {}
                classify = OperateInstance.get_table_classify(item['table_classify'])
                tmp['table_id'] = classify.id
                tmp['table_name'] = classify.name
                tmp['fields'] = classify.fields.fields
                tmp['data'] = [item['data']]
                data.append(tmp)
        # {'data': serializer.data,
        #         'fields': table_field_obj.fields,
        #         'rules': table_field_obj.rules,
        #         }
        return json_ok_response(data)
