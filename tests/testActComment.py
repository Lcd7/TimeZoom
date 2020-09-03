'''
测试评论功能
评论动态
评论已有评论
删除单个评论
删除动态所有评论(删除动态即可)
获取单个评论
获取所有动态所有
'''
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
def add_comment():
    url = '127.0.0.1:8058/comment/add'
    params['text'] = '1asgaew'
    params['artSeqid'] = 123
    return requests.post(url, headers = headers, params = params)

@ret_info
def add_recomment():
    url = '127.0.0.1:8058/comment/add'
    params['commentSeqid'] = 123
    params['artSeqid'] = 123
    return requests.post(url, headers = headers, params = params)

@ret_info
def delete_comment():
    url = '127.0.0.1:8058/comment/delete'
    params['commentSeqid'] = 123
    params['artSeqid'] = 123
    return requests.post(url, headers = headers, params = params)

@ret_info
def get_comment():
    commentSeqid = 123
    url = f'127.0.0.1:8058/comment/get?commentSeqid={commentSeqid}'
    return requests.get(url, headers = headers)

@ret_info
def get_comments():
    artSeqid = 123
    url = f'127.0.0.1:8058/comment/get?artSeqid={artSeqid}'
    return requests.get(url, headers = headers)