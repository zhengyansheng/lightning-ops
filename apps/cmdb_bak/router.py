from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('v1/cmdb/instances', views.CMDBServerModelViewSet)
router.register('v1/cmdb/table-classify', views.ClassifyModelViewSet)
router.register('v1/cmdb/table-field', views.TableFieldModelViewSet)
router.register('v1/cmdb/table-data', views.TableDataModelViewSet)

