import logging

from base.views import BaseApiView
from base.views import BaseModelViewSet
from base.response import json_ok_response
from base.response import json_error_response
from base.mixins import TreeListMixin
from . import models
from . import serializers
from . import filters

from rest_framework.decorators import action

logger = logging.getLogger("django.server")


# Create your views here.


class OrganizationsModelViewSet(TreeListMixin, BaseModelViewSet):
    """
    公司组织架构
    /api/v1/corp/organization/
    /api/v1/corp/organization/<pk>/user/
    """
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationModelSerializer
    search_fields = ('node',)

    @action(methods=['get'], detail=True, url_path="user", url_name="user")
    def filter_user(self, request, pk=None):
        logger.debug("Action pk: {}.".format(pk))
        try:
            instance = models.Organization.objects.get(pk=pk)
        except models.Organization.DoesNotExist:
            return json_error_response(message="pk: {} not found.".format(pk))

        u_ids = []
        query_set = instance.get_descendants(include_self=True)
        for q in query_set:
            _qs = q.userprofile_set.all()
            if not _qs:
                continue
            u_ids.extend([u.pk for u in _qs])
        users = models.UserProfile.objects.filter(pk__in=u_ids)
        s = serializers.UserProfileModelSerializer(users, many=True)
        return json_ok_response(data=s.data)


class UserModelViewSet(BaseModelViewSet):
    """
    公司用户信息
    /v1/corp/user/
    """
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileModelSerializer
    search_fields = ('name', 'username')


class UserInfoApiView(BaseApiView):
    """
    通过token公司用户信息
    /v1/corp/user/info
    """

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            u = models.UserProfile.objects.get(pk=user.pk)
        except models.UserProfile.DoesNotExist:
            return json_error_response(message="not found")
        s = serializers.UserProfileModelSerializer(u)
        return json_ok_response(data=s.data)
