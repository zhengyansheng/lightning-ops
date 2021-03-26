from .models import AuditLog
from .serializers import AuditLogModelSerializer
from base.views import BaseModelViewSet

# Create your views here.


class AuditLogViewSet(BaseModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogModelSerializer
    search_fields = ["url", "username", "status_code"]