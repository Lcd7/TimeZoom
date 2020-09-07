from flask import Blueprint, request, jsonify, g, current_app
webIndex = Blueprint('webIndex', __name__)
webBack = Blueprint('webBack', __name__, url_prefix = '/admin')

import time
from functools import wraps
from flask_restful import reqparse
from app.libs import TableUser, TableArticle, TableComment, TableImg, TableLetter, TableAdmin

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
parser.add_argument('friendSeqid', type = str)      # 好友id


import jwt
from jwt import exceptions
def create_token(payload):
    '''
    创建token
    '''
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    exp = int(time.time() + 86400)
    payload['exp'] = exp
    token = jwt.encode(
        payload = payload,
        key = current_app.config['IV'],
        algorithm = "HS256",
        headers = headers
        ).decode('utf-8')
    return token

def validate_token(token):
    '''
    校验token
    '''
    payload = None
    msg = None
    try:
        payload = jwt.decode(token, current_app.config['IV'], True, algorithm = 'HS256')

    except exceptions.ExpiredSignatureError:
        msg = 'token已失效'
    except jwt.DecodeError:
        msg = 'token认证失败'
    except jwt.InvalidTokenError:
        msg = '非法的token'
    return payload, msg

def check_token(func):
    '''
    验证token装饰器
    '''
    @wraps(func)
    def wrapper(*arg, **kwargs):
        token = request.headers.get('token')
        if not token:
            g.retMsg['msg'] = '请登录'
            return jsonify(g.retMsg)

        payload, msg = validate_token(token)
        if msg:
            g.retMsg['msg'] = msg
        nickname = payload['nickname']
        user = g.tableUser.get_user_by(nickname = nickname)
        if not user:
            g.retMsg['msg'] = '用户不存在'
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
        g.artUserid = 0 if args.get('artUserid') in ('', None) else int(args.get('artUserid'))
        g.isPublic = None if args.get('isPublic') in ('', None) else int(args.get('isPublic'))
        
        return func(*arg, **kwargs)
    return wrapper

def admin_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('token')
        if not token:
            g.retMsg['msg'] = '请登录'
            return jsonify(g.retMsg)

        payload, msg = validate_token(token)
        if msg:
            g.retMsg['msg'] = msg
        userName = payload['userName']
        admin = g.tableAdmin.get_admin(userName = userName)
        if not admin:
            g.retMsg['msg'] = '用户不存在'
            return jsonify(g.retMsg)
        g.admin = admin
        args = parser.parse_args()
        g.userName = args.get('userName')           
        g.password = args.get('password')   
        g.userSeqid = args.get('userSeqid')                                                              
        g.artText = args.get('artText')
        g.friendSeqid = 0 if args.get('friendSeqid') in ('', None) else int(args.get('friendSeqid'))
        g.artSeqid = 0 if args.get('artSeqid') in ('', None) else int(args.get('artSeqid'))
        g.artUserid = 0 if args.get('artUserid') in ('', None) else int(args.get('artUserid'))
        g.isPublic = None if args.get('isPublic') in ('', None) else int(args.get('isPublic'))

        return func(*args, **kwargs)
    return wrapper

@webIndex.before_request
def get_base_info():
    g.tableArticle = TableArticle()
    g.tableComment = TableComment()
    g.tableImg = TableImg()
    g.tableUser = TableUser()
    g.tableLetter = TableLetter()
    g.retMsg = {
        'status': 0,
        'code': 500,
        'msg': '',
        'data': {}
    }

@webBack.before_request
def back_base():
    g.tableArticle = TableArticle()
    g.tableImg = TableImg()
    g.tableUser = TableUser()
    g.tableAdmin = TableAdmin()
    g.retMsg = {
        'status': 0,
        'code': 500,
        'msg': '',
        'data': {}
    }
    

import app.web.index
import app.web.users
import app.web.comments
import app.web.articles
import app.web.letter