import logging
from itertools import chain

from base.views import BaseModelViewSet, BaseApiView
from base import response
from . import models
from . import serializers
from .verify import verify_permission
from apps.user.serializers import UserProfileModelSerializer, UserProfile

from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.conf import settings


logger = logging.getLogger("django.server")


class RoleModelViewSet(BaseModelViewSet):
    """
    角色管理
    """
    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleModelSerializer
    search_fields = ('name', 'remark')

    @action(methods=['get'], detail=True, url_path="users", url_name="role_users")
    def role_users(self, request, pk):
        """
        角色包含哪些用户
        :param request:
        :param pk:
        :return:
        """
        role_bind_qs = models.RoleBind.objects.filter(role=pk)
        user_id = [rb.user.id for rb in role_bind_qs]
        user_qs = UserProfile.objects.filter(pk__in=user_id)
        self.queryset = user_qs
        self.serializer_class = UserProfileModelSerializer
        return self.list(request)

    @action(methods=['get', 'post', 'put'], detail=True, url_path="perms", url_name="role_perms")
    def role_perms(self, request, pk):
        """
        角色包含哪些权限
        角色添加权限
        角色更新权限
        :param request:
        :param pk:
        :return:
        """
        if request.method == 'POST':
            serializer = serializers.RolePermSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self._create_perm(serializer.validated_data)
        if request.method == 'PUT':
            serializer = serializers.RolePermSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self._update_perm(serializer.validated_data)

        role_obj = self.get_object()
        self.queryset = role_obj.perm_rule.all()
        self.serializer_class = serializers.PermRuleModelSerializer
        return self.list(request)

    @action(methods=['get', 'post', 'put'], detail=True, url_path="route", url_name="role_route")
    def role_route(self, request, pk):
        """
        角色拥有的视图
        :param request:
        :param pk:
        :return:
        """
        if request.method == 'POST':
            serializer = serializers.RoleRouteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self._create_route(serializer.validated_data)
        if request.method == 'PUT':
            serializer = serializers.RoleRouteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self._update_route(serializer.validated_data)

        role_obj = self.get_object()
        self.queryset = role_obj.router.all()
        self.serializer_class = serializers.RouterSerializer
        return self.list(request)

    def _create_perm(self, validated_data):
        role_obj = self.get_object()
        role_obj.perm_rule.add(*validated_data['perm'])

    def _update_perm(self, validated_data):
        role_obj = self.get_object()
        role_obj.perm_rule.set(list(map(lambda x: x.id, validated_data['perm'])))

    def _create_route(self, validated_data):
        role_obj = self.get_object()
        role_obj.router.add(*validated_data['route'])

    def _update_route(self, validated_data):
        role_obj = self.get_object()
        role_obj.router.set(list(map(lambda x: x.id, validated_data['route'])))


class PermRuleModelViewSet(BaseModelViewSet):
    """
    API权限管理
    """
    queryset = models.PermRule.objects.all()
    serializer_class = serializers.PermRuleModelSerializer
    search_fields = ('name',)

    @action(methods=['get'], detail=True, url_path="role", url_name="get_perm_role")
    def filter_perm_role(self, request: Request, pk):
        """
        权限有哪些角色
        :param request:
        :param pk:
        :return:
        """
        perm_obj = self.get_object()
        self.queryset = perm_obj.role.all()
        self.serializer_class = serializers.RoleModelSerializer
        return self.list(request)


class UserRoleViewSet(BaseModelViewSet):
    """
    用户角色绑定
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileModelSerializer

    def retrieve(self, request, *args, **kwargs):
        return response.json_api_response(400, None, "请求错误")

    def destroy(self, request, *args, **kwargs):
        return response.json_api_response(400, None, "请求错误")

    def update(self, request, *args, **kwargs):
        return response.json_api_response(400, None, "请求错误")

    def _update(self, request, *args, **kwargs):
        data = request.data
        data['user'] = self.get_object().id
        serializer = serializers.UserRoleBindSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        with transaction.atomic():
            models.RoleBind.objects.filter(user=user).delete()
            serializer.create(serializer.validated_data)
        return response.json_api_response(0, None, "更新用户角色成功")

    def create(self, request, *args, **kwargs):
        serializer = serializers.UserRoleBindSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for role in serializer.validated_data['role']:
            if len(models.RoleBind.objects.filter(user=serializer.validated_data['user'], role=role)):
                return response.json_error_response({'role': ["用户已绑定<{}>角色".format(role.id)]})
        serializer.create(serializer.validated_data)
        return response.json_api_response(0, None, "创建成功")

    def list(self, request, *args, **kwargs):
        self._set_qs(models.RoleBind.objects.all(), serializers.RoleBindModelSerializer)
        return super(UserRoleViewSet, self).list(request, *args, **kwargs)

    def _set_qs(self, qs, sc):
        self.queryset = qs
        self.serializer_class = sc

    @action(methods=['get', 'put'], detail=True, url_path="roles", url_name="user_roles")
    def roles(self, request, *args, **kwargs):
        """
        获取指定用户的角色
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if request.method == 'PUT':
            return self._update(request, *args, **kwargs)
        user = self.get_object()
        role_bind_qs = models.RoleBind.objects.filter(user=user)
        role_id = [rb.role.id for rb in role_bind_qs]
        self._set_qs(models.Role.objects.filter(pk__in=role_id), serializers.RoleModelSerializer)
        return super(UserRoleViewSet, self).list(request, *args, **kwargs)

    @action(methods=['get'], detail=True, url_path="perms", url_name="user_perms")
    def perms(self, request, *args, **kwargs):
        """
        获取指定用户的权限
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = self.get_object()
        role_bind_qs = models.RoleBind.objects.filter(user=user)
        perm_id = [perm.id for role_bind_obj in role_bind_qs
                   for perm in role_bind_obj.role.perm_rule.all()]
        self._set_qs(models.PermRule.objects.filter(pk__in=perm_id), serializers.PermRuleModelSerializer)
        return super(UserRoleViewSet, self).list(request, *args, **kwargs)

    @action(methods=['get'], detail=True, url_path="exclusion-roles", url_name="exclusion_roles")
    def exclusion(self, request, *args, **kwargs):
        """
        获取指定用户的未拥有的角色
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = self.get_object()
        role_bind_qs = models.RoleBind.objects.filter(user=user)
        role_id = [rb.role.id for rb in role_bind_qs]
        self._set_qs(models.Role.objects.exclude(pk__in=role_id), serializers.RoleModelSerializer)
        return super(UserRoleViewSet, self).list(request, *args, **kwargs)


class HasPermissionView(BaseApiView):
    """
    判断请求url是否有权限
    {
        "path": "/api/v1/xxx/",
        "method": "GET"
    }
    """
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        username = request.user.username
        serializer = serializers.HasPermSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        path = serializer.data.get("path")
        method = serializer.data.get("method")
        return response.json_ok_response() \
            if verify_permission(username, path, method) else response.json_error_response("没有权限")


class RouterViewSet(BaseModelViewSet):
    """前端路由管理"""
    pagination_class = None
    queryset = models.Router.objects.all()
    serializer_class = serializers.RouterSerializer

    @action(methods=['get'], detail=False, url_path="menu", url_name="menu")
    def menu(self, request):
        parents_qs = self.queryset.filter(isParent=True, parent=None)
        return response.json_ok_response(self._get_children_route(parents_qs))

    def _get_children_route(self, parents_qs):
        ret = []
        for route_obj in parents_qs:
            parent_serializer = self.get_serializer(instance=route_obj, many=False)
            sub_qs = self.queryset.filter(parent=route_obj)
            sub_serializer = self.get_serializer(instance=sub_qs, many=True)
            data = parent_serializer.data
            if len(sub_serializer.data):
                data['children'] = sub_serializer.data
            ret.append(data)
        return ret


class UserGetRoute(BaseApiView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        role_bind_user_qs = request.user.role_bind.all()
        for rb in role_bind_user_qs:
            if rb.role.name == settings.ADMIN_ROLE:
                return response.json_ok_response(self._get_admin_route())

        router_chain = chain(*[rb.role.router.all() for rb in role_bind_user_qs])
        route_qs = models.Router.objects.filter(pk__in=[r.id for r in router_chain])
        ret = self._get_children_route(route_qs)
        return response.json_ok_response(ret)

    def _get_children_route(self, qs):
        route_related = {route.id: [] for route in qs.filter(isParent=True)}
        result_route = []

        for sub_route in qs.filter(isParent=False):
            route_related.setdefault(sub_route.parent.id, [])
            route_related[sub_route.parent.id].append(sub_route.id)

        for parent_id, child_ids in route_related.items():
            parent_obj = models.Router.objects.get(pk=parent_id)
            data = self._get_route_serializer_data(parent_obj)

            if child_ids:
                data['children'] = []
                for child_id in child_ids:
                    sub_route_obj = models.Router.objects.get(pk=child_id)
                    sub_data = self._get_route_serializer_data(sub_route_obj)
                    data['children'].append(sub_data)
            result_route.append(data)

        return result_route

    def _get_route_serializer_data(self, route_obj):
        return serializers.RouterSerializer(instance=route_obj, many=False).data

    def _get_admin_route(self):
        parents_qs = self.get_queryset().filter(isParent=True, parent=None)
        ret = []
        for route_obj in parents_qs:
            parent_serializer = self.get_serializer(instance=route_obj, many=False)
            sub_qs = self.get_queryset().filter(parent=route_obj)
            sub_serializer = self.get_serializer(instance=sub_qs, many=True)
            data = parent_serializer.data
            if len(sub_serializer.data):
                data['children'] = sub_serializer.data
            ret.append(data)
        return ret

    def get_serializer(self, *args, **kwargs):
        return serializers.RouterSerializer(*args, **kwargs)

    def get_queryset(self):
        return models.Router.objects.all()

