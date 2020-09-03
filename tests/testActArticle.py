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
        print(f'响应数据{response}')
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
    url = 'http://127.0.0.1:8058/article/get?artUserId=1&isPublic=2'
    return requests.get(url)

@ret_info
def get_user_all_public_Arts():
    '''
    获取一个用户所有公开动态
    '''
    url = '127.0.0.1:8058/article/get&artUserId=1&isPublic=1'
    return requests.get(url)

@ret_info
def get_user_one_art():
    '''
    获取单个动态
    '''
    url = '127.0.0.1:8058/article/get?artSeqid=2&isPublic=1'
    return requests.get(url)

@ret_info
def post_art():
    '''
    上传动态
    '''
    url = 'http://127.0.0.1:8058/article/post'
    params['artText'] = 'FP欠我9k'
    params['isPublic'] = 0
    params['imgName'] = None
    params['imgPath'] = None
    return requests.post(url, params = params, headers = headers)

@ret_info
def delete_art():
    '''
    删除动态
    '''
    url = '127.0.0.1:8058/article/delete?artSeqid=10086'
    return requests.post(url, headers = headers)

@ret_info
def set_art_isPublic():
    '''
    设置动态公不公开
    '''
    url = '127.0.0.1:8058/article/set?isPublic=1&artSeqid=10086'
    return requests.post(url, headers = headers, params = params)

@ret_info
def get_all_art():
    '''
    获取大厅动态
    '''
    url = '127.0.0.1:8058/article/getall?artNum=20'
    return requests.get(url, headers = headers)

@ret_info
def get_like():
    '''
    动态点赞
    '''
    url = '127.0.0.1:8058/article/like?artSeqid=1'
    return requests.post(url, headers = headers)