from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'v1/perm/role', views.RoleModelViewSet, basename='role')
router.register(r'v1/perm/perm', views.PermRuleModelViewSet, basename='perm')
router.register(r'v1/perm/user', views.UserRoleViewSet, basename='perm_user')
router.register(r'v1/perm/route', views.RouterViewSet, basename='route')