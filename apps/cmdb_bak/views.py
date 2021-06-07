from base.views import BaseModelViewSet
from base.response import json_api_response

from .models import CMDBBase
from .models import TableClassify
from .models import TableField
from .models import TableData
from .serializers import CMDBBaseModelSerializer
from .serializers import TableClassifyModelSerializer
from .serializers import TableFieldModelSerializer
from .serializers import TableDataModelSerializer
from .filters import CmdbFilter

from rest_framework.decorators import action

# Create your views here.



class CMDBServerModelViewSet(BaseModelViewSet):
    """服务树 关联服务器"""
    queryset = CMDBBase.objects.all().order_by("id")
    serializer_class = CMDBBaseModelSerializer
    authentication_classes = []
    permission_classes = []
    search_fields = ("hostname", "private_ip")
    filterset_class = CmdbFilter

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return json_api_response(code=0, data=serializer.data, message=None)

    @action(methods=['put'], detail=False, url_path="multi_update")
    def multi_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), data=request.data, partial=False, many=True, context={'request': request})
        if not serializer.is_valid():
            return json_api_response(code=-1, data=None, message="")
        serializer.is_valid(raise_exception=False)
        self.perform_update(serializer)
        return json_api_response(code=0, data=serializer.data, message=None)

    @action(methods=['delete'], detail=False, url_path="multi_delete")
    def multi_delete(self, request, *args, **kwargs):
        return json_api_response(code=-1, data=None, message="Not allowed.")


def verify_classify_data(func):

    def wrapper(*args, **kwargs):
        # View
        view = args[0]
        # content
        from rest_framework.views import APIView
        request = view.request
        if request.method == "GET":
            data = request.POST
            print(dir(view))
            # if pid:

        elif request.method == "POST":
            import json
            data = json.loads(request.body)
            pid = data.get("pid")
            print("pid", pid)
            # if pid:
        elif request.method == "PUT":
            pass
            view.request.data
            # import json
            # json_data = json.loads(view.request.body)
            # print(json_data)
            # OperateInstance.get_children_table_classify
        return func(*args, **kwargs)

    return wrapper


class ClassifyModelViewSet(BaseModelViewSet):
    """分类"""
    queryset = TableClassify.objects.filter(is_deleted=False).order_by('id')
    serializer_class = TableClassifyModelSerializer
    authentication_classes = []
    permission_classes = []

    # @verify_classify_data
    def dispatch(self, request, *args, **kwargs):
        return super(ClassifyModelViewSet, self).dispatch(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        # 1. 校验数据
        pid = data.get("pid")
        if pid and pid != 0:
            try:
                if OperateInstance.get_table_classify(pid).pid:
                    return json_error_response(f'指定的pid:({pid}) 不是主类型模型表.')
            except:
                pass

        # 2. 执行父类
        s = super(ClassifyModelViewSet, self).create(request, *args, **kwargs)
        return json_api_response(code=0, data=s.data, message=None)

        # try:
        #     data = request.data
        #     if data.get('pid') and data.get('pid') != 0:
        #         if OperateInstance.get_table_classify(data['pid']).pid:
        #             return json_error_response(f'指定的pid:({data["pid"]}) 不是主类型模型表.')
        #     serializer = self.get_serializer(data=data)
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save()
        #     return json_ok_response(serializer.data)
        # except Exception as e:
        #     return json_error_response(str(e))
    def update(self, request, *args, **kwargs):
        pid = request.data.get('pid')
        if pid:
            if OperateInstance.get_children_table_classify(self.get_object().instance.id):
                return json_error_response('此类型无法修改, 请先清空此类型下所属的子类型.')
            else:
                parent_table_classify = OperateInstance.get_table_classify(pid)
                if not parent_table_classify or parent_table_classify.pid:
                    return json_error_response('指定的 pid 不是子类型资产无法进行修改')

        s = super(ClassifyModelViewSet, self).create(request, *args, **kwargs)
        return json_api_response(code=0, data=s.data, message=None)


class TableFieldModelViewSet(BaseModelViewSet):
    """分类"""
    queryset = TableField.objects.all().order_by("id")
    serializer_class = TableFieldModelSerializer
    authentication_classes = []
    permission_classes = []
    search_fields = ("name", )


class TableDataModelViewSet(BaseModelViewSet):
    """分类"""
    queryset = TableData.objects.all().order_by("id")
    serializer_class = TableDataModelSerializer
    authentication_classes = []
    permission_classes = []
    search_fields = ("name", )