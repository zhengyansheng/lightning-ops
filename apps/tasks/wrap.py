from .models import TaskHistory


def command_audit_log(view_func):
    def wrapper(request, *args, **kwargs):

        response = view_func(request, *args, **kwargs)
        if response.data['code'] != 0:
            return
        task_id = response.data['data']

        if 'HTTP_X_FORWARDED_FOR' in request.META:
            src_ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            src_ip = request.META['REMOTE_ADDR']

        request_data = request.data
        script_file = request_data.get('script_name') if request_data.get('script_name') else request_data.get('playbook')
        data = {
            'task_id': task_id,
            'task_name': request_data['name'],
            'script_file': script_file,
            'task_hosts': request_data['hosts'],
            'create_user': request.user.username,
            'src_ip': src_ip,
            'exec_interval': 0,
        }
        th = TaskHistory.objects.create(**data)
        th.save()

        return response
    return wrapper
