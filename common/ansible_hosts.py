import os
import re
from .file import File
from common.get_config_value import get_value


class Ansible(object):

    @staticmethod
    def get_group():
        """ 返回 ansible hosts group """
        ansible_hosts = get_value('ansible', 'ansible_host_path')
        re_pattern = r'^\s*\[(?P<host>.*)\]'
        host_list = [{'name': 'all', 'children': [{'name': 'all'}]}]
        if File.if_file_exists(ansible_hosts):
            host_dic = {'name': File.get_file_name(ansible_hosts), 'children': []}
            with open(ansible_hosts) as f:
                for line in f:
                    hosts = re.match(re_pattern, line)
                    if hosts:
                        host_dic['children'].append({'name': hosts.group('host')})
                host_list.append(host_dic)
        else:
            host_file_list = File.get_dir_list(ansible_hosts)
            for item in host_file_list:
                abs_file = File.get_join_path(ansible_hosts, item)
                if File.if_file_exists(abs_file):
                    host_dic = {'name': item, 'children': []}
                    with open(abs_file) as f:
                        for line in f:
                            hosts = re.match(re_pattern, line)
                            if hosts:
                                host_dic['children'].append({'name': hosts.group('host')})
                        host_list.append(host_dic)
        return host_list

    @staticmethod
    def get_hosts():
        """ 返回 ansible hosts file """
        host_list = []
        ansible_hosts = get_value('ansible', 'ansible_host_path')
        if File.if_file_exists(ansible_hosts):
            host_list.append({'name': File.get_file_name(ansible_hosts)})
        else:
            host_file_list = File.get_dir_list(ansible_hosts)
            for files in host_file_list:
                if File.if_file_exists(File.get_join_path(ansible_hosts, files)):
                    host_list.append({'name': files})
        return host_list
