# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore, register_events

# 实例化
# scheduler = BackgroundScheduler()
# scheduler.add_jobstore(DjangoJobStore())
# scheduler.start()  # 此处不能过早启动


# class Scheduler(object):
#
#     @staticmethod
#     def get_job(task_id):
#         """查询指定任务信息"""
#         return None
#         job = scheduler.get_job(task_id)
#         return job
#
#     @staticmethod
#     def start_job(task_id):
#         """启动任务"""
#         scheduler.resume_job(task_id)
#
#     @staticmethod
#     def stop_job(task_id):
#         """暂停任务"""
#         scheduler.pause_job(task_id)
#
#     @staticmethod
#     def rm_job(task_id):
#         """删除定时任务"""
#         scheduler.remove_job(task_id)
#
#     @staticmethod
#     def add_job(func, args, task_id, timing):
#         """
#         :param func: 添加任务指定的函数
#         :param args: 函数的参数
#         :param task_id: 唯一标识
#         :param timing: crontab 格式执行时间
#         :return:
#         """
#         scheduler.add_job(
#             func,
#             'cron',
#             args=args,
#             id=task_id,
#             **timing,
#         )
#         register_events(scheduler)
