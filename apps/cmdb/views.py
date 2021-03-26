from base.views import BaseModelViewSet

from .models import CMDBBase
from .serializers import CMDBBaseModelSerializer
from .filters import CmdbFilter

# Create your views here.


class CMDBServerModelViewSet(BaseModelViewSet):
    """服务树 关联服务器"""
    queryset = CMDBBase.objects.all()
    serializer_class = CMDBBaseModelSerializer
    authentication_classes = []
    permission_classes = []
    search_fields = ("hostname", "private_ip")
    filterset_class = CmdbFilter


