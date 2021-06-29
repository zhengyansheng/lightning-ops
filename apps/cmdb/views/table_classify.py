import json

from rest_framework.decorators import action
from django.core.files.uploadedfile import InMemoryUploadedFile

from ..models import TableClassify, TableRelation, AssetsRelation, TableData
from ..serializers import TableClassifySerializer
from ..verify.operate import OperateInstance
from base.views import BaseModelViewSet
from base.response import json_ok_response, json_error_response


class TableClassifyViewSet(BaseModelViewSet):
    queryset = TableClassify.objects.filter().order_by("id")
    serializer_class = TableClassifySerializer
    ordering_fields = ("id", "name", "pid")
    filter_fields = ("id", "name", "pid", "is_forbid_bind")
    search_fields = ("name",)

    def create(self, request, *args, **kwargs):
        data = request.data
        pid = data.get("pid")
        # 如果新建数据存在PID
        if pid:
            # 查询 id = pid 的实例, 如果实例的PID不为Null则返回错误
            if OperateInstance.get_table_classify(pid).pid:
                return json_error_response(f"指定的pid:({pid}) 不是主分类表.")
        return super(TableClassifyViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        # data = json.loads(json.dumps(request.data))
        pid = data.get("pid")
        # 判断是否存在PID
        if pid:
            # 查询 pid = instance.id 的表, 如果存在则报错.
            if OperateInstance.get_children_table_classify(instance.id):
                return json_error_response("无法修改, 此类型表存在子分类表.")
            # 获取要指定为主类的实例, 并判断是否为主类 也就是 PID == Null
            parent_table_classify = OperateInstance.get_table_classify(pid)
            if not parent_table_classify or parent_table_classify.pid:
                return json_error_response("指定的 pid 不存在或者不是主分类表.")
        if data.get("icon"):
            if not isinstance(data.get("icon"), InMemoryUploadedFile):
                del data["icon"]
        serializer = self.get_serializer(
            instance, data=data, partial=kwargs.pop("partial", False)
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}
        return json_ok_response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 如果没有 pid 则为主分类表
        if not instance.pid:
            child_table_all = OperateInstance.get_children_table_classify(instance.id)
            if child_table_all:
                return json_error_response("如果删除主类型请先删除实体模型表.")

        # 清理关联表
        table_relation = OperateInstance.get_parent_table_relation(instance.id)
        if table_relation:
            for inc in table_relation:
                if inc.child_table.is_forbid_bind:
                    inc.delete()

        instance.delete()
        return json_ok_response("删除成功")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        field_obj = OperateInstance.get_table_field(instance.id)
        if field_obj:
            data["rules"] = field_obj.rules
            data["field_id"] = field_obj.id
            data["fields"] = field_obj.fields
        else:
            data["field_id"] = None
            data["rules"] = None
            data["fields"] = None
        children_all = OperateInstance.get_table_relation_list(instance.id)
        data["children"] = []
        data["relevant"] = []
        if children_all:
            for item in children_all:
                dic = self.get_serializer(item.child_table).data
                dic["parent_name"] = item.child_table.pid.name
                dic["is_foreign_key"] = item.is_foreign_key
                data["children"].append(dic)
        relevant_all = OperateInstance.get_table_relation_list_c(instance.id)
        if relevant_all:
            for item in relevant_all:
                dic = self.get_serializer(item.parent_table).data
                dic["parent_name"] = item.parent_table.pid.name
                dic["is_foreign_key"] = item.is_foreign_key
                data["relevant"].append(dic)

        return json_ok_response(data)

    @action(methods=["get"], detail=False)
    def tree(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = []
        for item in json.loads(json.dumps(serializer.data)):
            if not item["pid"]:
                for dic in data:
                    if dic["id"] == item["id"]:
                        break
                else:
                    item["children"] = []
                    data.append(item)
            else:
                for i, dic in enumerate(data):
                    if dic["id"] == item["pid"]:
                        data[i]["children"].append(item)
                        break
                else:
                    parent_data = self.get_serializer(
                        OperateInstance.get_table_classify(item["pid"])
                    )
                    tmp_data = json.loads(json.dumps(parent_data.data))
                    tmp_data["children"] = []
                    tmp_data["children"].append(item)
                    data.append(tmp_data)
        return json_ok_response(data)

    @action(methods=["post"], detail=False)
    def relation(self, request, *args, **kwargs):
        data = request.data
        parent_table_id = data.get("parent_table_id")
        child_table_id = data.get("child_table_id")

        if not parent_table_id or not child_table_id:
            return json_error_response("parent_table_id and child_table_id 是必传参数.")

        parent_classify = OperateInstance.get_table_classify(parent_table_id)
        child_classify = OperateInstance.get_table_classify(child_table_id)

        # 验证表是否存在
        if not parent_classify or not child_classify:
            return json_error_response("parent分类表或者child分类表不存在")

        # 验证 是否有
        if not parent_classify.pid or not child_classify.pid:
            return json_error_response("parent分类表或者child分类表是主分类表, 不允许进行绑定操作.")
        # 验证 child 和 parent 是否为同一个表
        if parent_classify.id == child_classify.id:
            return json_error_response("不支持自关联.")

        # 验证 是否禁止绑定.
        if child_classify.is_forbid_bind:
            return json_error_response("child表,禁止绑定操作.")

        # 验证是否存在字段表
        parent_field = OperateInstance.get_table_field(parent_table_id)
        child_field = OperateInstance.get_table_field(child_table_id)
        if not parent_field or not child_field:
            return json_error_response("parent类型表或者child类型表没有字段表")

        table_relation_obj = TableRelation.objects.create(
            parent_table_id=parent_table_id,
            child_table_id=child_table_id,
            is_foreign_key=data.get("is_foreign_key"),
        )

        if request.data.get("is_forbid_bind"):
            child_classify.is_forbid_bind = True
            child_classify.save()

        table_relation_obj.save()
        return json_ok_response("关联成功")

    @action(methods=["delete"], detail=False, url_path="un-relation")
    def un_relation(self, request, *args, **kwargs):
        data = request.data

        parent_table_id = data.get("parent_table_id")
        child_table_id = data.get("child_table_id")

        if not parent_table_id or not child_table_id:
            return json_error_response("parent_table_id and child_table_id 是必传参数.")

        classify_relation_obj = OperateInstance.get_table_relation(
            parent_table_id, child_table_id
        )
        if not classify_relation_obj:
            return json_error_response(
                f"找不到parent_table_id为:{parent_table_id}, child_table_id为: {child_table_id} 关系记录"
            )

        # 修改 child_classify_obj 的值
        child_classify_obj = OperateInstance.get_table_classify(child_table_id)
        if child_classify_obj.is_forbid_bind:
            child_classify_obj.is_forbid_bind = False
            child_classify_obj.save()

        classify_relation_obj.delete()
        return json_ok_response("解除关联成功")

    @action(methods=["get"], detail=False)
    def classify(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(pid=None)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return json_ok_response(serializer.data)
