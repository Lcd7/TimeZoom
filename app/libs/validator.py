import hashlib
import time
import re

class Validator:
    @classmethod
    def vali_user_phone(cls, phone):
        '''
        验证手机号
        return: True or False
        '''
        ret = re.match(r"^1[35678]\d{9}$", phone)
        if ret:
            return True
        else:
            return False

    @classmethod
    def vali_user_email(cls, email):
        '''
        验证邮箱
        return: True or False
        '''
        ret = re.match(r"^\w+@(\w+.)+(com|cn|net)$", email)
        if ret:
            return True
        else:
            return False

    @classmethod
    def vali_user_password(cls, pass1, pass2):
        '''
        验证密码
        pass1: 密码
        pass2: 再次确认的密码
        return: 失败返回错误信息 or 成功返回False
        '''
        if len(pass1) <= 20:
            if pass1 == pass2:
                return False
            else:
                return '两次密码不一致'
        return '密码长度要小于20'