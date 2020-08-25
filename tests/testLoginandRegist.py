'''
测试登录注册
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


def post(phoneNumber, email, nickname, sex, timenow, passw, url):
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
        print(response.get('msg'))

def start(url):
    phoneNumber = '15182696454'
    email = ''
    nickname = ''
    sex = ''
    timenow = str(int(time.time()))
    passw = 'Soda.123'
    post(phoneNumber, email, nickname, sex, timenow, passw, url)

def login():
    url = 'http://127.0.0.1:8058/user/login'
    start(url)

def regist():
    url = 'http://127.0.0.1:8058/index/register'
    start(url)

if __name__ == "__main__":
    pass
    