from .pagination import CustomPageNumberPagination
from .response import json_ok_response
from .serializers import TreeSerializer
from .permissions import ApiRBACPermission

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework.parsers import JSONParser
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.renderers import JSONRenderer
from rest_framework.renderers import AdminRenderer
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework_csv.renderers import CSVRenderer


__all__ = (
    "BaseModelViewSet",
    "BaseApiView",
    "TreeModelViewSet",
)



def valid_field_required(field_array, data_map):
    for field in field_array:
        if field not in data_map:
            raise ParseError(f"{field} is required.")


class BaseModelViewSet(ModelViewSet):
    """
        视图集合基类
    """
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    # permission_classes = [ApiRBACPermission, ]
    pagination_class = CustomPageNumberPagination
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, AdminRenderer, CSVRenderer]
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = []  # search=<field>

    def create(self, request, *args, **kwargs):
        response = super(BaseModelViewSet, self).create(request, *args, **kwargs)
        return json_ok_response(response.data)

    def update(self, request, *args, **kwargs):
        response = super(BaseModelViewSet, self).update(request, *args, **kwargs)
        return json_ok_response(response.data)

    def destroy(self, request, *args, **kwargs):
        response = super(BaseModelViewSet, self).destroy(request, *args, **kwargs)
        return json_ok_response(response.data)

    def list(self, request, *args, **kwargs):
        response = super(BaseModelViewSet, self).list(request, *args, **kwargs)
        return json_ok_response(response.data)

    def retrieve(self, request, *args, **kwargs):
        response = super(BaseModelViewSet, self).retrieve(request, *args, **kwargs)
        return json_ok_response(response.data)


class BaseApiView(APIView):
    """
        APIView视图类
    """
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated, ]


class TreeModelViewSet(BaseModelViewSet):
    serializer_class = TreeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        s = self.get_serializer(queryset, many=True)
        response = []
        try:
            tree_dict = {item['id']: item for item in s.data}
            for i in tree_dict:
                if tree_dict[i]['pid']:
                    pid = tree_dict[i]['pid']
                    parent = tree_dict[pid]
                    parent.setdefault('children', []).append(tree_dict[i])
                else:
                    response.append(tree_dict[i])
        except KeyError:
            response = s.data
        if page is not None:
            response = self.get_paginated_response(response)
            return json_ok_response(response.data)
        return json_ok_response(response)



