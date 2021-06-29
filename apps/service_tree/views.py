from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import action

# from apps.cmdb.models import CMDBBase
# from apps.cmdb.serializers import CMDBBaseModelSerializer
from base.mixins import BulkCreateModelMixin
from base.response import json_api_response
from base.views import BaseApiView
from base.views import BaseModelViewSet
from .filters import ServiceTreeFilter
from .models import NodeJoinTag
from .models import NodeLinkOperaPermission
from .models import NodeLinkServer
from .models import ServiceTree
from .serializers import NodeJoinTagSerializer
from .serializers import NodeLinkOperaPermissionModelSerializer
from .serializers import NodeLinkServerSerializer
from .serializers import ServiceTreeListSerializer


# Create your views here.


def show_genres(request):
    return render(
        request,
        "service_tree/genres.html",
        {'genres': ServiceTree.objects.all()}
    )


class ServiceTreeModelViewSet(BulkCreateModelMixin, BaseModelViewSet):
    """服务树"""
    queryset = ServiceTree.objects.all()
    serializer_class = ServiceTreeListSerializer
    pagination_class = None
    filterset_class = ServiceTreeFilter


    def get_queryset(self):
        queryset = super(ServiceTreeModelViewSet, self).get_queryset()
        u = self.request.user
        if u.username in ["admin", "root"]:
            return queryset
        
        node_pks = []
        # u = UserProfile.objects.get(username=self.request.user)
        # write member
        for x in u.write_member.all():
            up_nodes = x.node.get_ancestors(ascending=False, include_self=True)
            node_pks.extend([n.pk for n in up_nodes])

        # read member
        for x in u.read_member.all():
            up_nodes = x.node.get_ancestors(ascending=False, include_self=True)
            node_pks.extend([n.pk for n in up_nodes])

        return queryset.filter(pk__in=list(set(node_pks)))
        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(queryset.filter(parent=None), many=True).data
        for instance in data:
            instance['children'] = self.set_children_nodes(instance["pk"], queryset)

        return json_api_response(code=0, data=data, message="")

    def set_children_nodes(self, pk, qs):
        children_set = qs.filter(parent=pk)  # 第2层 ops, ter, prt
        children_data = self.get_serializer(children_set, many=True).data
        for child in children_data:
            child_qs = qs.filter(parent=child['pk'])  # 第3层 monkey, api-gw
            if child_qs.exists():
                child['children'] = self.set_children_nodes(child['pk'], qs)
        return children_data

    @action(methods=["get"], detail=True)
    def opera_permission_member(self, request, pk=None):
        ret = {
            "read_member": [],
            "write_member": [],
            "read_member_ref": [],  # 继承 read
            "write_member_ref": []  # 继承 write
        }
        # 当前节点
        node = self.get_object()

        # 当前节点下所有的叶子节点
        _nodes = node.get_ancestors(ascending=True, include_self=True)

        # OneToOneField
        for idx, n in enumerate(_nodes):
            try:
                read_member_set = n.nodelinkoperapermission.read_member.all()
                write_member_set = n.nodelinkoperapermission.write_member.all()
                read_member = [{'id': o.pk, 'username': o.username, 'email': o.email, 'name': o.name} for o in read_member_set]
                write_member = [{'id': o.pk, 'username': o.username, 'email': o.email, 'name': o.name} for o in write_member_set]
            except ServiceTree.nodelinkoperapermission.RelatedObjectDoesNotExist:
                continue

            if idx == 0:
                ret['read_member'] = read_member
                ret['write_member'] = write_member
            else:
                ret['read_member_ref'].extend(read_member)
                ret['write_member_ref'].extend(write_member)

        return json_api_response(code=0, data=ret, message=None)

    @action(methods=["get"], detail=True)
    def server(self, request, pk=None, *args, **kwargs):
        """
        查询节点下所有叶子节点的机器信息
        /api/v1/service_tree/<pk>/server/?page=1&page_size=100
        /api/v1/service_tree/<pk>/server/?page=1&page_size=100&hostname=<>&private_ip=<>
        @param request:
        @param pk:
        @return:
        """
        is_pagination = False

        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 15)
        if page:
            is_pagination = True

        # 当前节点
        node = self.get_object()

        # 当前节点下所有的叶子节点
        _nodes = node.get_descendants(include_self=True)
        _leaf_nodes = [n for n in _nodes if n.is_leaf_node()]

        # OneToOneField
        cmdb_pks = []
        for leaf_node in _leaf_nodes:
            try:
                link_server = leaf_node.nodelinkserver.cmdbs.all()
            except:
                pass
            else:
                cmdb_pks.extend([s.pk for s in link_server])

        # # ForeignKey
        # node_set = []
        # for leaf_node in _leaf_nodes:
        #     node_set.extend(leaf_node.nodelinkserver_set.all())
        # cmdb_pks = []
        # for s in node_set:
        #     cmdb_pks.extend([_s.pk for _s in s.cmdbs.all()])

        qs = CMDBBase.objects.filter(pk__in=cmdb_pks, is_deleted=False)
        qs = self.server_filter(qs, request.query_params)
        count = qs.count()
        if is_pagination:
            start = (int(page) - 1) * int(page_size)
            stop = start + int(page_size)
            qs = qs[start:stop]

        response = {
            "count": count,
            "results": CMDBBaseModelSerializer(qs, many=True).data
        }
        return json_api_response(code=0, data=response, message=None)

    @action(methods=["get"], detail=True)
    def tag(self, request, pk=None, *args, **kwargs):
        """
        查询节点关联的tag
        /api/v1/service_tree/<pk>/tag/
        - 不需要分页
        {
            "tag": []
            "tag_ref": [[],[]]
        }
        """
        response = {"tag": [], "tag_ref": []}

        # 当前节点
        node = self.get_object()

        # 当前节点含当前节点上继承的tag
        _nodes = node.get_ancestors(ascending=True, include_self=True)
        for idx, n in enumerate(_nodes):
            kvs = [{"key": info.key, "value": info.value, "id": info.pk} for info in n.nodejointag_set.all()]
            if idx == 0:
                response['tag'] = kvs
                continue
            if not kvs:
                continue
            response['tag_ref'].append(kvs)
        return json_api_response(code=0, data=response, message=None)

    @action(methods=["get"], detail=True)
    def tag_v2(self, request, pk=None, *args, **kwargs):
        """
        查询节点关联的tag
        /api/v1/service_tree/<pk>/tag/
        - 不需要分页
        @param request:
        @param pk:
        @return:
        {
            "tag": {}
            "tag_ref": [{},{}]
        }
        """
        response = {"tag": {}, "tag_ref": []}

        # 当前节点
        node = self.get_object()

        # 当前节点含当前节点上继承的tag
        _nodes = node.get_ancestors(ascending=True, include_self=True)
        for idx, n in enumerate(_nodes):
            kvs = {info.key: info.value for info in n.nodejointag_set.all()}
            if idx == 0:
                response['tag'] = kvs
                continue
            if not kvs:
                continue
            response['tag_ref'].append(kvs)
        return json_api_response(code=0, data=response, message=None)

    def server_filter(self, qs, query):
        # 全局模糊搜索
        dft_v = query.get('default')
        if dft_v:
            qs = qs.filter(
                Q(hostname__contains=dft_v) |
                Q(private_ip__contains=dft_v)
            )
        else:
            # 精准搜索
            hostname_v = query.get('hostname')
            if hostname_v:
                qs = qs.filter(hostname=hostname_v)
            private_ip_v = query.get('private_ip')
            if private_ip_v:
                qs = qs.filter(private_ip=private_ip_v)
        return qs

    def destroy(self, request, *args, **kwargs):
        ins = self.get_object()
        # 不允许跨层级删除
        if not ins.is_leaf_node():
            return json_api_response(code=-1, data=None, message="不允许跨层级删除.")
        return super(ServiceTreeModelViewSet, self).destroy(request, *args, **kwargs)


class NodeOperaPermissionModelViewSet(BaseModelViewSet):
    """服务树 关联节点操作权限"""
    queryset = NodeLinkOperaPermission.objects.all()
    serializer_class = NodeLinkOperaPermissionModelSerializer
    pagination_class = None

    def create(self, request, *args, **kwargs):
        """
        如果 node 不存在时，则添加，否则修改
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return json_api_response(code=0, data=serializer.data, message=None)

        print("data", serializer.data)
        try:
            instance = self.queryset.get(node_id=serializer.data['node'])
        except NodeLinkOperaPermission.DoesNotExist:
            return json_api_response(code=-1, data=None, message="not found.")

        partial = kwargs.pop('partial', True)
        s = self.get_serializer(instance, data=request.data, partial=partial)
        s.is_valid(raise_exception=True)
        try:
            instance.read_member.add(*serializer.data['read_member'])
            instance.write_member.add(*serializer.data['write_member'])
        except Exception as e:
            return json_api_response(code=-1, data=e.args, message=None)
        return json_api_response(code=0, data=s.data, message=None)

    def destroy(self, request, *args, **kwargs):
        """
        /api/v1/service_tree/opera_permission/<node_id>/
        {
            read_member: []
            write_member: []
        }
        """
        data = request.data

        try:
            node = ServiceTree.objects.get(pk=kwargs['pk'])
        except ServiceTree.DoesNotExist:
            return json_api_response(code=-1, data=None, message=f"node {kwargs['pk']} not found")

        node.nodelinkoperapermission.read_member.remove(*data.get('read_member', []))
        node.nodelinkoperapermission.write_member.remove(*data.get('write_member', []))
        return json_api_response(code=0, data=None, message="删除成功.")


class NodeLinkServerModelViewSet(BaseModelViewSet):
    """
    服务树 关联服务器
    """
    queryset = NodeLinkServer.objects.all()
    serializer_class = NodeLinkServerSerializer
    pagination_class = None

    def create(self, request, *args, **kwargs):
        """
        如果 node 不存在时，则添加，否则修改
        """
        if 'app_key' in request.data:

            try:
                node = self.queryset.get(node__appkey=request.data['app_key'])
            except NodeLinkServer.DoesNotExist:
                return json_api_response(code=-1, data=None, message="app_key not found.")

            request_data = {
                "node": node.node_id,
                "cmdbs": request.data['cmdbs'],
            }
        else:
            request_data = request.data

        serializer = self.get_serializer(data=request_data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return json_api_response(code=0, data=serializer.data, message=None)
        else:
            try:
                instance = self.queryset.get(node_id=serializer.data['node'])
            except NodeLinkServer.DoesNotExist:
                return json_api_response(code=-1, data=None, message="not found.")

            partial = kwargs.pop('partial', True)
            s = self.get_serializer(instance, data=request_data, partial=partial)
            s.is_valid(raise_exception=True)
            instance.cmdbs.add(*serializer.data['cmdbs'])
            return json_api_response(code=0, data=serializer.data, message=None)


class NodeLinkTagModelViewSet(BaseModelViewSet):
    """
    服务树 关联Tag
    https://help.aliyun.com/document_detail/171446.html?spm=5176.2020520101manager.0.0.12914a9cStpRuR
    """
    queryset = NodeJoinTag.objects.all()
    serializer_class = NodeJoinTagSerializer
    pagination_class = None


class UnlinkNodeServerApiView(BaseApiView):
    """
    从服务树解绑Server
    delete /api/v1/service_tree/unlink/<node_id>/
    {
        "server_ids": [1, 2, 3]  # cmdb的id
    }
    """

    def delete(self, request, *args, **kwargs):
        data = request.data
        node_id = kwargs['pk']
        server_ids = data['server_ids']

        try:
            node_link_server = NodeLinkServer.objects.get(node_id=node_id)
        except NodeLinkServer.DoesNotExist:
            return json_api_response(code=-1, data=None, message=f"node_id {node_id} not found.")

        instances = CMDBBase.objects.filter(pk__in=server_ids)
        node_link_server.cmdbs.remove(*[x.pk for x in instances])
        return json_api_response(code=0, data=None, message=None)


class ParentNodeInfoApiView(BaseApiView):
    """
    查询节点上所有的父节点

    /api/v1/service_tree/parents/100/
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk, *args, **kwargs):
        try:
            node = ServiceTree.objects.get(pk=pk)
        except ServiceTree.DoesNotExist:
            return json_api_response(code=-1, data=None, message=f"pk {pk} not found.")

        s = ServiceTreeListSerializer(node.get_ancestors(ascending=True, include_self=True), many=True)
        return json_api_response(code=0, data=s.data, message=None)
