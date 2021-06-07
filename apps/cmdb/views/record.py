from base.views import BaseModelViewSet
from ..models import ChangeRecord
from ..serializers import ChangeRecordSerializer


class ChangeRecordViewSet(BaseModelViewSet):
    queryset = ChangeRecord.objects.filter().order_by('-id')
    serializer_class = ChangeRecordSerializer
    ordering_fields = ('id', 'title',)
    filter_fields = ('id', 'title', 'table_data_id')
    search_fields = ('title', 'title')
