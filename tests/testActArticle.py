'''
测试用户发布动态行为
获取用户所有动态
获取单个动态
删除动态
点赞
设置公开
获取所有用户所有动态
'''
import time
import requests

headers = {
    'token': '用户token',
}

params = {}

def ret_info(func):
    def wrapper():
        response = func()
        response = response.json()
        if response.get('code') == 1:
            print('成功')
        else:
            print(response.get('msg'))
    return wrapper

@ret_info
def get_user_all_arts():
    '''
    获取一个用户所有动态
    '''
    url = '127.0.0.1:8058/Article/get?artUserId=1&isPublic=2'
    return requests.get(url)

@ret_info
def get_user_all_public_Arts():
    '''
    获取一个用户所有公开动态
    '''
    url = '127.0.0.1:8058/Article/get&artUserId=1&isPublic=1'
    return requests.get(url)

@ret_info
def get_user_one_art():
    '''
    获取单个动态
    '''
    url = '127.0.0.1:8058/Article/get?artSeqid=2&isPublic=1'
    return requests.get(url)