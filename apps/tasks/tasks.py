import datetime

import celery
from django.conf import settings

from apps.tasks.models import TaskHistory
from common.ansible_api import BaseAnsible
from ops.celery import app


class BaseCeleryTask(celery.Task):
    """ celery 任务回调父类 """

    def on_success(self, retval, task_id, args, kwargs):
        try:
            th = TaskHistory.objects.get(task_id=task_id)
        except TaskHistory.DoesNotExist:
            return

        run_time = (datetime.datetime.now() - th.create_time).seconds
        args = str(args) + str(kwargs)
        result_dic = {
            'task_code': retval[1],
            'task_result': retval[0],
            'exec_interval': run_time,
            'script_cmd': args,
        }
        for k, v in result_dic.items():
            setattr(th, k, v)
        th.save()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


@app.task(base=BaseCeleryTask)
def runner_task(
    inventory='/etc/ansible/hosts',
    connection='local',
    forks=10,
    remote_user=None,
    passwords=None,
    hosts=None,
    module=None,
    args=None,
):
    """exec script"""

    inventory = settings.ANSIBLE_HOSTS_PATH
    hoc = BaseAnsible(
        inventory=inventory,
        connection=connection,
        forks=forks,
        remote_user=remote_user,
        passwords=passwords
    )

    hoc.run(hosts=hosts, module=module, args=args)
    return hoc.get_runner_result()


@app.task(base=BaseCeleryTask)
def playbook_task(
    inventory='/etc/ansible/hosts',
    connection='local',
    forks=10,
    remote_user=None,
    passwords=None,
    playbook=None,
    extra_vars=None
):
    """exec playbook"""
    inventory = settings.ANSIBLE_HOSTS_PATH
    play = BaseAnsible(
        inventory=inventory,
        connection=connection,
        forks=forks,
        remote_user=remote_user,
        passwords=passwords
    )
    play.playbook(playbooks=[playbook], extra_vars=extra_vars)
    return play.get_play_result()
