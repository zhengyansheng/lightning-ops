import json

from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin



class DisabledDeleteMiddleware(MiddlewareMixin):
    """
    仅限于读操作
    """

    def process_request(self, request):
        """接收请求"""
        if request.META["REQUEST_METHOD"] == "DELETE":
            raise PermissionDenied("此平台为功能展示，删除权限已仅用.")

    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    def process_template_response(self, request, response):
        return response

    def process_exception(self, request, exception):
        """异常"""
        pass

    def process_response(self, request, response):
        """处理完成"""
        return response
