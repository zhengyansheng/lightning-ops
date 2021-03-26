import datetime

from ansible.plugins.callback import CallbackBase


class ResultCallback(CallbackBase):
    """
        重写callbackBase类的部分方法,可以获得执行后返回的结果和状态
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

        self.host_all_info = []
        self.host_failed_iplist = []
        self.host_unreachabled_iplist = []
        self.host_summarize = []

        self.total = 0
        self.success_total = 0
        self.error_total = 0
        self.unreachable_total = 0
        self.skip_total = 0
        self.unreachable_list = []
        self.error_list = []
        self.skip_list = []

    def v2_runner_on_unreachable(self, result):
        """ 主机不可达回调 """
        self.host_unreachable[result._host.get_name()] = result

        exec_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        host_ip = result._host.get_name()
        task_name = result.task_name
        result_info = result._result

        result_dict = {"exec_time": exec_time, "host_ip": host_ip, "task_name": task_name, "status": "unreachable",
                       "result_info": result_info}

        self.total += 1
        self.unreachable_list.append(host_ip)
        self.unreachable_total += 1
        self.host_all_info.append(result_dict)

    def v2_runner_on_ok(self, result, **kwargs):
        """ 任务成功回调 """
        self.host_ok[result._host.get_name()] = result

        exec_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        host_ip = result._host.get_name()
        task_name = result.task_name
        result_info = result._result
        # if result_info['invocation']:
        #     result_info.pop('invocation')
        # if result_info['deprecations']:
        #     result_info.pop('deprecations')
        # if result_info['warnings']:
        #     result_info.pop('warnings')
        result_dict = {"exec_time": exec_time, "host_ip": host_ip, "task_name": task_name, "status": "success",
                       "result_info": result_info}
        self.total += 1
        self.success_total += 1
        self.host_all_info.append(result_dict)

    def v2_runner_on_failed(self, result, ignore_errors=False, **kwargs):
        """任务失败回调"""
        self.host_failed[result._host.get_name()] = result

        exec_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        host_ip = result._host.get_name()
        task_name = result.task_name
        result_info = result._result
        result_dict = {"exec_time": exec_time, "host_ip": host_ip, "task_name": task_name, "status": "failed",
                       "result_info": result_info}
        self.total += 1
        self.error_list.append(host_ip)
        self.error_total += 1
        self.host_all_info.append(result_dict)

    def v2_runner_on_skipped(self, result, **kwargs):
        """任务 skip 回调 """
        exec_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        host_ip = result._host.get_name()
        task_name = result.task_name
        result_info = result._result
        result_dict = {"exec_time": exec_time, "host_ip": host_ip, "task_name": task_name, "status": "skip",
                       "result_info": result_info}
        self.total += 1
        self.skip_list.append(host_ip)
        self.skip_count += 1
        self.host_all_info.append(result_dict)

    def v2_playbook_on_task_start(self, task, is_conditional):
        """ 任务 action 都会触发 """
        pass

    def v2_playbook_on_play_start(self, play):
        pass

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.host_summarize.append({h:t})
            if t["failures"] != int(0):
                self.host_failed_iplist.append(h)
            if t["unreachable"] != int(0):
                self.host_unreachabled_iplist.append(h)

    def v2_runner_on_start(self, host, task):
        pass
