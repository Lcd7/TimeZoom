'''
请求测试脚本
'''
import requests
from Crypto.Cipher import AES
import base64
import datetime
import time
import os
import json

from app.utils.aesEncrypt import Aescrypt

env_dist = os.environ

IV = env_dist.get('IV')
KEY = env_dist.get('AES_KEY')


def login_test(phoneNumber, email, nickname, sex, timenow, passw, url):
    aescryptor = Aescrypt(AES.MODE_CBC, KEY, IV) # CBC模式
    passw = aescryptor.AES_Encrypt(passw)
    sign = aescryptor.AES_Encrypt(phoneNumber[:3] + timenow[:3] + passw)

    # 解密sign
    decText = aescryptor.AES_Decrypt(sign)
    decText = decText[6:]
    aescryptor.AES_Decrypt(decText)

    params = {
        'phoneNumber': phoneNumber,
        'password': passw,
        'email': email,
        'nickname': nickname,
        'sex': sex,
        'timenow': timenow,
        'sign':sign
    }
    print(f"上传数据: {params}")
    response = requests.post(url, params)
    response = response.json()
    print(f"响应数据: {response}")
    if response.get('code') == 1:
        print('成功')
    else:
        print('失败')

def start():
    phoneNumber = '13512019674'
    email = '521463258@qq.com'
    nickname = '大学生'
    sex = '男'
    timenow = str(int(time.time()))
    passw = 'qwerasdf'
    url1 = 'http://127.0.0.1:8058/register'         # 注册
    # url2 = 'http://127.0.0.1:8058/login'            # 登录
    login_test(phoneNumber, email, nickname, sex, timenow, passw, url1)

if __name__ == "__main__":
    pass
    