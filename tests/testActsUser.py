'''
测试用户行为
修改用户信息，增删好友
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

@ ret_info
def change_info():
    url = 'http://127.0.0.1:8058/user/chageInfo'
    params['sex'] = '男'
    return requests.post(url, headers = headers, params = params)
    
@ ret_info
def logout():
    url = 'http://127.0.0.1:8058/user/logout'
    return requests.get(url, headers = headers)

@ ret_info
def change_avatar(imgName, imgPath):
    url = 'http://127.0.0.1:8058/user/changeAvatar'
    params['imgName'] = imgName
    params['imgPath'] = imgPath
    return requests.post(url, headers = headers, params = params)
    
@ ret_info
def add_friend():
    url = 'http://127.0.0.1:8058/user/addFriend'
    params['friendSeqid'] = 4
    return requests.post(url, headers = headers, params = params)
    
@ ret_info
def delete_friend():
    url = 'http://127.0.0.1:8058/user/deleteFriend'
    params['friendSeqid'] = 4
    return requests.post(url, headers = headers, params = params)
    
@ ret_info
def answer_friend():
    url = 'http://127.0.0.1:8058/user/answerFriend'
    params['answer'] = True
    return requests.post(url, headers = headers, params = params)
   
@ ret_info
def get_friend():
    url = 'http://127.0.0.1:8058/user/getFriends'
    return requests.get(url, headers)


if __name__ == "__main__":
    pass
