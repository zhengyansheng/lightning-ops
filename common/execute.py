import subprocess


def exec_command(cmd):
    """子进程的方式执行"""
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()
        ret_code = p.poll()
        if ret_code != 0:
            return stderr, False

        if stdout:
            return stdout.decode('utf-8'), True
        else:
            return stderr.decode('utf-8'), False

    except Exception as e:
        return e.args, False


def local_cmd(cmd, is_wait=True):
    """
    执行Shell命令
    """
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if is_wait:
        p.wait()
    return p


def local_cmd_with_warning(cmd, is_wait=True):
    """
    执行Shell命令
    """
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if is_wait:
        pipe.wait()
    out, err = pipe.stdout.read(), pipe.stderr.read()
    if out and isinstance(out, bytes):
        return str(out, 'utf-8'), True
    if err and isinstance(err, bytes):
        return str(err, 'utf-8'), False
    return '', False


def local_cmd_out_err(cmd, is_wait=True):
    """
    执行Shell命令
    """
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if is_wait:
        pipe.wait()
    err = pipe.stderr.read()
    if err:
        return err, False
    return pipe.stdout.read(), True
