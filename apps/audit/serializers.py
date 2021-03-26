from .models import AuditLog

from rest_framework.serializers import ModelSerializer


class AuditLogModelSerializer(ModelSerializer):

    class Meta:
        model = AuditLog
        fields = "__all__"
