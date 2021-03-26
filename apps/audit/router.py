from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('v1/audit/log', views.AuditLogViewSet, basename='audit_log')
