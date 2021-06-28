from base.views import BaseModelViewSet
from base.response import json_ok_response, json_error_response
from ..models import TableField
from ..serializers import TableFieldSerializer
from ..verify.check_filed import check_field
from ..verify.operate import OperateInstance


class TableFieldViewSet(BaseModelViewSet):
    queryset = TableField.objects.filter().order_by("id")
    serializer_class = TableFieldSerializer
    ordering_fields = ("id",)
    filter_fields = ("id",)
    search_fields = ("id",)

    def create(self, request, *args, **kwargs):
        table_classify_obj = OperateInstance.get_table_classify(
            request.data["table_classify"]
        )

        # 判断 table_classify实例是否存在并且不是主分类
        if not table_classify_obj or not table_classify_obj.pid:
            return json_error_response(
                "table_classify实例不存在或者table_classify实例为主分类,主分类不允许创建字段表."
            )
        try:
            check_field(request.data)
        except Exception as e:
            return json_error_response(f"数据校验出错: {str(e)}")
        return super(TableFieldViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        # 判断如果更换 table_classify_id 当前 instance 是否存在资产
        if instance.table_classify.id != data[
            "table_classify"
        ] and OperateInstance.get_all_asset(instance.table_classify.id):
            return json_error_response("分类表已经存在资产, 字段表不允许更换主类.")

        # 判断更换的 table_classify 是否是 主分类表
        if not OperateInstance.get_table_classify(data["table_classify"]).pid:
            return json_error_response("指定的分类表为主分类,主分类无法设置表字段.")

        # 检查数据
        try:
            check_field(data)
        except Exception as e:
            return json_error_response(f"数据校验出错: {str(e)}")
        print(data)
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}
        return json_ok_response(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if OperateInstance.get_all_asset(instance.table_classify.id):
            return json_error_response("删除字段存在数据无法进行删除操作")
        instance.delete()
        return json_ok_response()
