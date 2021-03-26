import re


class Validate(object):

    @staticmethod
    def is_valid_mobile_phone(phone):
        """
        判断是否为手机号
        """
        return re.match('^1[34578]\d{9}$', phone)

    @staticmethod
    def is_safe_password(password):
        """
        检查密码强度
        密码要求包含大小写字母和数字,密码长度至少8位
        """
        return re.match('(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$', password)
