from tests.testLoginandRegist import login, regist
from tests.testActsUser import change_info, logout, change_avatar, add_friend, delete_friend, answer_friend, get_friend


testPyDict = {
    'Login': login,                         # 登录
    'Regist': regist,                       # 注册
    'change_info': change_info,             # 修改用户信息
    'logout': logout,                       # 登出
    'change_avatar': change_avatar,         # 上传头像
    'add_friend': add_friend,               # 添加好友
    'answer_friend': answer_friend,         # 回应好友请求
    'delete_friend': delete_friend,         # 删除好友
    'get_friend': get_friend,               # 获取好友列表

}

if __name__ == "__main__":
    testPyDict['Login']()
    testPyDict['Regist']()
    testPyDict['change_info']()
    testPyDict['logout']()
    imgName = 'lcd.jpeg'
    imgPath = 'C:/Users/user/Desktop/lcd.jpeg'
    testPyDict['change_avatar'](imgName, imgPath)
    testPyDict['add_friend']()
    testPyDict['answer_friend']()
    testPyDict['delete_friend']()
    testPyDict['get_friend']()
