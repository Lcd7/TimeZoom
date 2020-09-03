from tests.testLoginandRegist import login, regist
from tests.testActsUser import change_info, logout, change_avatar, add_friend, delete_friend, answer_friend, get_friend
from tests.testActArticle import get_user_all_arts, get_user_all_public_Arts, get_user_one_art, post_art, delete_art, set_art_isPublic, get_all_art, get_like
from tests.testActComment import add_comment, add_recomment, delete_comment, get_comment, get_comments


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
    'get_user_all_arts': get_user_all_arts,                 # 获取用户所有动态
    'get_user_all_public_Arts': get_user_all_public_Arts,   # 获取用户所有公开动态
    'get_user_one_art': get_user_one_art,                   # 获取一条动态
    'post_art': post_art,                                   # 发表动态
    'delete_art': delete_art,                               # 删除动态
    'set_art_isPublic': set_art_isPublic,                   # 设置动态公开状态
    'get_all_art': get_all_art,                             # 获取大厅所有动态
    'get_like': get_like,                                   # 点赞
    'add_comment': add_comment,             # 新增评论
    'add_recomment': add_recomment,         # 新增回复评论
    'delete_comment': delete_comment,       # 删除评论
    'get_comment': get_comment,             # 获取单个评论
    'get_comments': get_comments,           # 获取动态所有评论
}

if __name__ == "__main__":
    testPyDict['Login']()
    # testPyDict['Regist']()
    # testPyDict['change_info']()
    # testPyDict['logout']()
    # imgName = 'lcd.jpeg'
    # imgPath = 'C:/Users/user/Desktop/lcd.jpeg'
    # testPyDict['change_avatar'](imgName, imgPath)
    # testPyDict['add_friend']()
    # testPyDict['answer_friend']()
    # testPyDict['delete_friend']()
    # testPyDict['get_friend']()
    # testPyDict['get_user_all_arts']()
    # testPyDict['get_user_one_art']()
    # testPyDict['get_user_all_public_Arts']()
    # testPyDict['post_art']()
    # testPyDict['delete_art']()
    # testPyDict['set_art_isPublic']()
    # testPyDict['get_all_art']()
    # testPyDict['get_like']()
    # testPyDict['add_comment']()
    # testPyDict['add_recomment']()
    # testPyDict['delete_comment']()
    # testPyDict['get_comment']()
    # testPyDict['get_comments']()