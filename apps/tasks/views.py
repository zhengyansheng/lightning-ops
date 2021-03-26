from django.conf import settings
from django.utils.decorators import method_decorator

from base.response import json_api_response
from base.views import BaseApiView
from base.views import BaseModelViewSet
from common.file import File
from .models import TaskHistory
from .serializers import TaskHistorySerializer
from .tasks import playbook_task
from .tasks import runner_task
from .wrap import command_audit_log


# Create your views here.


class ExecCommandApiView(BaseApiView):
    """执行命令"""

    @method_decorator(command_audit_log)
    def post(self, request, *args, **kwargs):
        data = request.data

        # 验证
        """
        hosts []
        hosts中的ip 必须要在/etc/ansible/hosts文件中注册过才行，否则忽略.
        """
        if not (isinstance(data['hosts'], list) and len(data['hosts']) < 100):
            # 安全风险考虑
            # TODO: 100 to config
            return json_api_response(code=-1, data=None, message="一次任务要执行的主机数量不能大于100台.")

        script_name = data["script_name"]
        if script_name.endswith("yaml"):
            # exec script
            task_data = {
                "playbook": File.get_join_path(settings.ANSIBLE_SCRIPT_PATH, data["script_name"]),
                "extra_vars": {
                    "host_list": data['hosts']
                },
                "forks": data.get("forks", 5),
            }
            result = playbook_task.delay(**task_data)
        else:
            # exec playbook
            task_data = {
                "hosts": data['hosts'],
                "forks": data.get("forks", 5),
                "module": "script",
                'args': File.get_join_path(settings.ANSIBLE_SCRIPT_PATH, data["script_name"]),
            }
            result = runner_task.delay(**task_data)

        return json_api_response(code=0, data=result.id, message=None)


class ScriptPlaybookApiView(BaseApiView):
    """查询脚本"""

    def get(self, request, *args, **kwargs):
        filename = kwargs.get('filename')
        if filename:
            result, ok = self.read_file(kwargs['filename'])
            if not ok:
                return json_api_response(code=-1, data=None, message=result)
        else:
            result, ok = self.list_dir()
        return json_api_response(code=0, data=result, message=None)

    def list_dir(self):
        """列出目录下所有脚本和剧本"""
        ret = {
            "script": [],
            "playbook": [],
        }

        file_list = File.list_dir(settings.ANSIBLE_SCRIPT_PATH)
        for x in file_list:
            if x.endswith("sh") or x.endswith("py"):
                ret['script'].append(x)
            elif x.endswith("yaml"):
                ret['playbook'].append(x)

        return ret, True

    def read_file(self, filename):
        """ 读文件内容 """
        file_path = File.get_join_path(settings.ANSIBLE_SCRIPT_PATH, filename)
        return File.read_file(file_path)


class TaskHistoryViewSet(BaseModelViewSet):
    """历史任务"""
    queryset = TaskHistory.objects.all().order_by('-id')
    serializer_class = TaskHistorySerializer
    ordering_fields = ('id', 'task_name')
    search_fields = ('task_name', 'create_user', 'src_ip', 'task_state')
    # filter_fields = ('task_status')
