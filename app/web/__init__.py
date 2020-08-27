from flask import Blueprint, request, jsonify, g, current_app
webIndex = Blueprint('webIndex', __name__)

import time
from flask_restful import reqparse
from app.libs import TableUser, TableArticle, TableComment, TableImg

parser = reqparse.RequestParser()
parser.add_argument('phoneNumber', type = str)      # 用户账号 （电话）
parser.add_argument('email', type = str)            # 用户密码
parser.add_argument('password', type = str)         # 用户邮箱
parser.add_argument('passw2', type = str)           # 用户再次确认密码
parser.add_argument('newpassw', type = str)         # 用户新密码
parser.add_argument('nickname', type = str)         # 用户昵称
parser.add_argument('sex', type = str)              # 用户性别
parser.add_argument('sign', type = str)             # 防篡改标志 sign
parser.add_argument('timenow', type = str)          # 用户当前时间戳
parser.add_argument('imgName', type = str)          # 上传图片名
parser.add_argument('imgPath', type = str)          # 上传图片的本地路径
parser.add_argument('artText', type = str)          # 动态内容
parser.add_argument('artSeqid', type = str)         # 动态id
parser.add_argument('artUserId', type = str)        # 动态所属用户id
parser.add_argument('isPublic', type = str)         # 是否公开 0 1

def check_token(func):
    '''
    验证token装饰器
    '''
    def wrapper(*arg, **kwargs):
        # token = request.headers.get('token')
        if not g.token:
            g.retMsg['msg'] = '请登录'
            return jsonify(g.retMsg)

        user = g.tableUser.get_user_by(token = g.token)
        if not user:
            g.retMsg['msg'] = '验证信息错误'
            return jsonify(g.retMsg)

        args = parser.parse_args()
        g.user = user
        g.phoneNumber = args.get('phoneNumber')           
        g.password = args.get('password')                   
        g.email = args.get('email')                         
        g.passw2 = args.get('passw2')                       
        g.newpassw = args.get('newpassw')                   
        g.nickname = args.get('nickname')                   
        g.sex = args.get('sex')                             
        g.sign = args.get('sign')                           
        g.timenow = args.get('timenow')                     
        g.imgName = args.get('imgName')                   
        g.imgPath = args.get('imgPath')                   
        g.artText = args.get('artText')
        g.friendSeqid = 0 if args.get('friendSeqid') in ('', None) else int(args.get('friendSeqid'))
        g.artSeqid = 0 if args.get('artSeqid') in ('', None) else int(args.get('artSeqid'))
        g.artUserId = 0 if args.get('artUserId') in ('', None) else int(args.get('artUserId'))
        g.isPublic = None if args.get('isPublic') in ('', None) else int(args.get('isPublic'))
        

        return func(*arg, **kwargs)
    return wrapper


@webIndex.before_request
def get_base_info():
    g.tableArticle = TableArticle()
    g.tableComment = TableComment()
    g.tableImg = TableImg()
    g.tableUser = TableUser()
    token = request.headers.get('token')
    g.retMsg = {
        'code': 0,
        'msg': '',
        'data': {}
    }
    if token:
        tableUser = TableUser()
        user = tableUser.get_user_by(token = token)
        if user:
            if int(user.timenow) > (int(time.time()) - (3600 * 24)):
                g.user = user
                g.token = token
            else:
                g.retMsg['msg'] = '请重新登录'
                return jsonify(g.retMsg)
        else:
            g.retMsg['msg'] = '请重新登录'
            return jsonify(g.retMsg)
    else:
        g.token = None
        g.user = None
    # return {}

# @webIndex.after_request
# def clear_g.retMsg(response):
#     global g.retMsg
#     g.retMsg = {
#         'code': 0,
#         'msg': '',
#         'data': {}
#     }
#     return response

import app.web.index
import app.web.users
import app.web.comments
import app.web.articles
import app.web.chat