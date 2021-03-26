import configparser
import os

from django.conf import settings

config_path = os.path.join(settings.ROOT_DIR, 'config', 'config.ini')


def config(path=config_path):
    obj = configparser.ConfigParser()
    obj.read(path, encoding='utf-8')
    return obj


def get_value(key, value):
    try:
        cfg = config()
        if key in cfg:
            return cfg[key][value]
        return 'key error'
    except Exception as e:
        return str(e)


# def get_ansible_host_list(file):
#     host_list = []
#     with open(file) as f:
#         for line in f:
#             if re.match('^\s*\[.*\]', line):
#                 host_list.append({'name': re.split(r'\[|\]', line)[1].strip()})
#
#     host_list.insert(0, {'name': 'all'})
#     return host_list
# children

def get_ansible_host_list(args):
    host_list = []
    if os.path.isfile(args):
        host_list.append({'name': os.path.basename(args)})
    else:
        files = os.listdir(args)
        for hostfile in files:
            if 'hosts' in hostfile:
                host_list.append({'name': hostfile})
    return host_list
