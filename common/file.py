import os
import pathlib
import shutil


class File(object):
    """文件管理"""

    @staticmethod
    def if_file_exists(abs_path):
        """
        :return: 判断文件是否存在
        """
        return os.path.isfile(abs_path)

    @staticmethod
    def if_file_endswith(file, patter):
        """
        :return: 判断文件扩展名
        """
        return file.endswith(patter)

    @staticmethod
    def get_file_name(abs_path):
        """
        :return: 返回文件名
        """
        return os.path.basename(abs_path)

    @staticmethod
    def get_abs_path(abs_path):
        """
        :return: 返回绝对路径
        """
        return os.path.dirname(abs_path)

    @staticmethod
    def get_dir_list(dir_path):
        """
        :return: 返回文件夹下文件
        """
        return os.listdir(dir_path)

    @staticmethod
    def get_join_path(*args):
        """
        :return: 返回拼接 path 路径
        """
        return os.path.join(*args)

    @staticmethod
    def if_dir_exists(dir_path):
        """判断目录是否存在"""
        return os.path.exists(dir_path)

    @staticmethod
    def create_dirs(dir_path):
        """创建多层目录"""
        try:
            os.makedirs(dir_path)
        except FileExistsError:
            pass

    @staticmethod
    def move_file(old_abs_file, abs_path):
        """移动文件/文件夹"""
        shutil.move(old_abs_file, abs_path)

    @staticmethod
    def rm_file(file_path):
        os.remove(file_path)

    @staticmethod
    def rm_dir(dir_path):
        """删除最后一层目录"""
        try:
            os.rmdir(dir_path)
        except:
            pass

    @staticmethod
    def rm_dirs(dir_path):
        """级联删除"""
        shutil.rmtree(dir_path)

    @staticmethod
    def read_file(abs_file):
        """读取文件内容"""
        if not File.if_file_exists(abs_file):
            return f"{abs_file} not found.", False
        file_obj = pathlib.Path(abs_file)
        return file_obj.read_text(encoding='utf-8'), True

    @staticmethod
    def write_file(abs_file, content):
        """ 写入内容至文件 """
        file_obj = pathlib.Path(abs_file)
        if not file_obj.is_file():
            file_obj.touch(mode=0o744)
        file_obj.write_text(content, encoding='utf-8')

    @staticmethod
    def rename_dir(dir_name, new_dir_name):
        if not File.if_dir_exists(dir_name):
            return "sre_dir: {} not found.".format(dir_name), False

        try:
            return os.rename(dir_name, new_dir_name), True
        except Exception as e:
            return e.args, False

    @staticmethod
    def list_dir(dir_name):
        return os.listdir(dir_name)
