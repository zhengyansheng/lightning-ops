from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('v1/service_tree/nodes', views.ServiceTreeModelViewSet, basename='service_tree_node')
router.register('v1/service_tree/opera_permission', views.NodeOperaPermissionModelViewSet, basename='link_opera_permission')
router.register('v1/service_tree/server', views.NodeLinkServerModelViewSet, basename='link_server')
router.register('v1/service_tree/tag', views.NodeLinkTagModelViewSet, basename='link_tag')
