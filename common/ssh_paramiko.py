import sys

#from apps.cmdb.models import SSH, Asset

import paramiko

class Paramiko():
    def __init__(self, host_list,  local_file, remote_file, command, timeout=30):
        self.host_list = host_list
        self.timeout = timeout
        self.command = command
        self.local_file = local_file
        self.remote_file = remote_file

    # 发送要执行的命令
    def ssh_exec(self,):
        try:
            res = {'code': 0, 'data': []}
            failed = 0
            success = 0
            host_total = 0
            host_error = []
            for ip in self.host_list:
                host_total += 1
                host_obj = Asset.objects.filter(manage_ip=ip).first()
                if host_obj.ssh:
                    sftp_put_info = self.sftp_put(ip=ip, user=host_obj.ssh.user, port=host_obj.ssh.port, password=host_obj.ssh.password)
                    sftp_put_info['data'].append('[脚本执行]')
                    if sftp_put_info['code'] == 0:
                        ssh = paramiko.SSHClient()
                        policy = paramiko.AutoAddPolicy()
                        ssh.set_missing_host_key_policy(policy)
                        ssh.connect(
                            hostname=ip,  # 服务器的ip
                            port=host_obj.ssh.port,  # 服务器的端口
                            username=host_obj.ssh.user,  # 服务器的用户名
                            password=host_obj.ssh.password  # 用户名对应的密码
                        )
                        stdin, stdout, stderr = ssh.exec_command(self.command)
                        stdout = stdout.read()
                        stderr = stderr.read()
                        if stderr:
                            failed += 1
                            host_error.append(ip)
                            sftp_put_info['data'].append('status: failed')
                            sftp_put_info['data'].append(f'details: {str(stderr, encoding="utf-8").strip()}')
                        else:
                            success += 1
                            sftp_put_info['data'].append('status: success')
                            sftp_put_info['data'].append(f'details: {str(stdout, encoding="utf-8").strip()}')
                    else:
                        failed += 1
                        host_error.append(ip)
                        sftp_put_info['data'].append('status: failed')
                        sftp_put_info['data'].append('details: 脚本传输失败，无法执行脚本')

                    res['data'] += (sftp_put_info['data'])
                else:
                    failed += 1
                    host_error.append(ip)
                    res['data'] += [f'{ip} ===>', 'status: failed', '未绑定ssh']
            res['data'].insert(0, f'失败主机列表： {str(host_error)}')
            res['data'].insert(0, f'失败总数： {failed}')
            res['data'].insert(0, f'成功总数： {success}')
            res['data'].insert(0, f'执行总数： {host_total}')
            res['data'] = '\n'.join(res['data'])
            return res
        except Exception as e:
            res['code'] = 10200
            res['data'] = str(e)
            return res

    # # get单个文件
    # def sftp_get(self, remote_file, local_file):
    #     t = paramiko.Transport((self.ip, self.port))
    #     t.connect(username=self.user, password=self.password)
    #     sftp = paramiko.SFTPClient.from_transport(t)
    #     sftp.get(remote_file, local_file)
    #     t.close()

    # put单个文件
    def sftp_put(self, ip, port, user, password):
        res = {'code': 0, 'data':  [f'{ip} ===>', '[脚本传输]']}
        try:
            transport = paramiko.Transport((ip, port))
            transport.connect(username=user, password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            # # 将location.py 上传至服务器 /tmp/test.py   '/tmp/test_from_win'
            put_into = sftp.put(self.local_file, self.remote_file)
            res['data'].append('status: success')
            res['data'].append(f'details: {str(put_into)}')
            transport.close()
            return res
        except Exception as e:
            res['code'] = 10200
            res['data'].append('status: failed')
            res['data'].append(f'details: {str(e)}')
            return res

