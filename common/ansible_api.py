import shutil

import ansible.constants as C
from ansible import context
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory.manager import InventoryManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.vars.manager import VariableManager

from .ansible_callback import ResultCallback


class BaseAnsible(object):
    def __init__(self,
                 connection='ssh',
                 remote_user="None",
                 ack_pass=None,
                 sudo=None,
                 sudo_user=None,
                 ask_sudo_pass=None,
                 module_path=None,
                 become=None,
                 become_method=None,
                 become_user=None,
                 check=False,
                 diff=False,
                 listhosts=None,
                 listtasks=None,
                 listtags=None,
                 forks=5,
                 tags=[],
                 skip_tags=[],
                 verbosity=3,
                 syntax=None,
                 start_at_task=None,
                 inventory=None,
                 passwords=None):

        """初始化"""
        context.CLIARGS = ImmutableDict(
            connection=connection,
            remote_user=remote_user,
            ack_pass=ack_pass,
            sudo=sudo,
            sudo_user=sudo_user,
            ask_sudo_pass=ask_sudo_pass,
            module_path=module_path,
            become=become,
            become_method=become_method,
            become_user=become_user,
            verbosity=verbosity,
            listhosts=listhosts,
            listtasks=listtasks,
            listtags=listtags,
            forks=forks,
            tags=tags,
            skip_tags=skip_tags,
            syntax=syntax,
            start_at_task=start_at_task,
        )

        # inventory 文件
        self.inventory = inventory if inventory else "localhost,"

        # 实例化数据解析器,用于解析 存放主机列表的资源库文件
        self.loader = DataLoader()

        # 实例化 资产配置对象,InventoryManager管理资源库
        self.inv_obj = InventoryManager(loader=self.loader, sources=self.inventory)

        # 设置密码，可以为空字典
        self.passwords = {"conn_pass": passwords}

        # 实例化回调插件对象
        self.results_callback = ResultCallback()

        # 变量管理器,假如有变量，所有的变量应该交给他管理。 这里他会从 inventory 对象中获取到所有已定义好的变量。 这里也需要数据解析器。
        self.variable_manager = VariableManager(self.loader, self.inv_obj)

    def run(self, hosts='all', gether_facts="no", module="ping", args=''):
        """ ad-hoc 方式执行 """
        play_source = dict(
            name="Ad-hoc",
            hosts=hosts,
            gather_facts=gether_facts,
            tasks=[
                {"action": {"module": module, "args": args}},
            ])
        # Play()是用于执行 Ad-hoc 的类 ,这里传入一个上面的play_source字典参数 VariableManager变量管理器  DataLoader数据解析器
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        tqm = None
        try:
            # TaskQueueManager 是底层用到的任务队列管理器
            # 要想执行 Ad-hoc ，需要把上面的 play 对象交给任务队列管理器的 run 方法去运行
            tqm = TaskQueueManager(
                inventory=self.inv_obj,
                variable_manager=self.variable_manager,
                loader=self.loader,
                passwords=self.passwords,
                stdout_callback=self.results_callback)

            tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    def playbook(self, playbooks, extra_vars={}):
        """用来调用 playbook 的方法"""
        self.variable_manager.extra_vars.update(extra_vars)

        playbook = PlaybookExecutor(playbooks=playbooks,
                                    inventory=self.inv_obj,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader,
                                    passwords=self.passwords)

        # 使用回调函数
        playbook._tqm._stdout_callback = self.results_callback
        playbook.run()

    def get_runner_result(self):
        """ Ad-hoc 格式化返回信息 """
        result_raw = {
            'simple_info': {
                'total': None,
                'success_total': None,
                'error_total': None,
                'unreachable_total': None,
                'skip_total': None,
                'error_list': None,
                'unreachable_list': None,
                'skip_list': None
            },
            'success': {},
            'failed': {},
            'unreachable': {}
        }

        try:
            for host, result in self.results_callback.host_ok.items():
                result_raw['success'][host] = result._result
            for host, result in self.results_callback.host_failed.items():
                result_raw['failed'][host] = result._result
            for host, result in self.results_callback.host_unreachable.items():
                result_raw['unreachable'][host] = result._result
            result_raw['simple_info']['total'] = self.results_callback.total
            result_raw['simple_info']['success_total'] = self.results_callback.success_total
            result_raw['simple_info']['error_total'] = self.results_callback.error_total
            result_raw['simple_info']['skip_total'] = self.results_callback.skip_total
            result_raw['simple_info']['unreachable_total'] = self.results_callback.unreachable_total
            result_raw['simple_info']['error_list'] = self.results_callback.error_list
            result_raw['simple_info']['unreachable_list'] = self.results_callback.unreachable_list
            result_raw['simple_info']['skip_list'] = self.results_callback.skip_list
            self.results_callback.total = 0
            self.results_callback.success_total = 0
            self.results_callback.error_total = 0
            self.results_callback.skip_total = 0
            self.results_callback.unreachable_total = 0
            self.results_callback.error_list = []
            self.results_callback.unreachable_list = []
            self.results_callback.skip_list = []
            return result_raw, True
        except Exception as e:
            return e.args, False

    def get_play_result(self):
        result_raw = {
            'simple_info':
                {
                    'total': None
                },
            'ummarize': {},
            'info': {}
        }
        try:
            result_raw['ummarize'] = self.results_callback.host_summarize
            for result in self.results_callback.host_all_info:
                host_ip = result.pop('host_ip')
                task_name = result.pop('task_name')
                if not host_ip in result_raw['info']:
                    result_raw['info'][host_ip] = [{task_name: result}]
                else:
                    result_raw['info'][host_ip].append({task_name: result})
            result_raw['simple_info']['total'] = len(result_raw['ummarize'])
            return result_raw, True
        except Exception as e:
            return e.args, False
