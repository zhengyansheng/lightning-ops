from base.views import BaseModelViewSet
from base.response import json_api_response

from .models import CMDBBase
from .serializers import CMDBBaseModelSerializer
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