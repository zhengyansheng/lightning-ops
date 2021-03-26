from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('v1/corp/organizations', views.OrganizationsModelViewSet, basename='organizations')
router.register('v1/corp/users', views.UserModelViewSet, basename='user')

