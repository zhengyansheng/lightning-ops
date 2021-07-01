from rest_framework import routers

from .views.record import ChangeRecordViewSet
from .views.table_classify import TableClassifyViewSet
from .views.table_data import TableDataViewSet
from .views.table_field import TableFieldViewSet

# from .views.table_relation import SchemaRelationViewSet

router = routers.DefaultRouter()
router.register(r"v1/cmdb/table-classify", TableClassifyViewSet)
router.register(r"v1/cmdb/table-field", TableFieldViewSet)
router.register(r"v1/cmdb/table-data", TableDataViewSet)
router.register(r"v1/cmdb/record", ChangeRecordViewSet)
