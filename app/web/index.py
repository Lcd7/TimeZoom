from flask import request, jsonify, g, current_app
from flask_restful import Api, Resource, reqparse
from app.web import blue_index
from app.libs import tableUser, validate
from app.utils import get_hash, AES_Encrypt

import time
from Crypto.Cipher import AES
import base64


api = Api(blue_index)
parser = reqparse.RequestParser()
parser.add_argument('phone_number', type = str)
parser.add_argument('email', type = str)
parser.add_argument('password', type = str)
parser.add_argument('pass2', type = str)
parser.add_argument('nickname', type = str)
parser.add_argument('sign', type = str)
parser.add_argument('timenow', type = str)

retMsg = {
    'code': 0,
    'msg': ''
}


def check_token(func):
    '''
    验证token装饰器
    '''
    def wrapper(*arg, **kwargs):
        token = request.headers.get('token')
        if not token:
            retMsg['msg'] = '需要验证'
            return jsonify(retMsg)
        user = tableUser.get_user_by(token = token)
        if not user:
            retMsg['msg'] = '验证信息错误'
            return jsonify(retMsg)

        return func(*arg, **kwargs)
    return wrapper

def get_user_info_when_login_and_register(func):
    '''
    获取用户登录、注册时的信息
    '''
    def wrapper(self):
        args = parser.parse_args()
        g.phone_number = args.get('phone_number')
        g.password = args.get('password')
        g.email = args.get('email')
        g.sign = args.get('sign')
        g.timenow = args.get('timenow')

        # 验证数据是否被篡改过
        aescryptor = AES_Encrypt.Aescrypt(AES.MODE_CBC, current_app.config['AES_KEY'], current_app.config['IV'])
        dec_sign = aescryptor.AES_Decrypt(g.sign)
        dec_sign = dec_sign[:6]
        if dec_sign == (g.phone_number[:3] + g.timenow[:3]):
            return func(self)
        else:
            retMsg['msg'] = '信息被篡改，请求失败'
            return jsonify(retMsg)
    return wrapper

@blue_index.before_request
def get_base_info():
    token = request.headers.get('token')
    if token:
        user = tableUser.get_user_by(token = token)
        g.user = user
        g.token = token
    else:
        g.user = None

    # return {}

class hello_world(Resource):
    def get(self):
        return 'Hello_world'

class login(Resource):
    '''
    用户登录
    '''
    @get_user_info_when_login_and_register
    def post(self):
        global retMsg

        # phone_number = request.get_json().get('phone_number')
        user = tableUser.get_user_by(phone_number = g.phone_number)
        if not user:
            user = tableUser.get_user_by(email = g.email)

        if not user:
            retMsg['msg'] = '没有此用户'
            return jsonify(retMsg)

        if user.password != g.password:
            retMsg['msg'] = '密码错误'
            return jsonify(retMsg)

        token = get_hash.get_md5(g.phone_number, g.password, str(int(time.time())))
        # 将token保存到数据库
        _update_user_token_dict = {'token': token}
        _res = tableUser.update_user(_update_user_token_dict)
        if _res:
            retMsg['code'] = 1
            retMsg['msg'] = '成功登录'
            retMsg['nickname'] = user.nickname
            retMsg['token'] = token
        else:
            retMsg['msg'] = '数据库错误'
        return jsonify(retMsg)

class register(Resource):
    '''
    用户注册
    '''
    @get_user_info_when_login_and_register
    def post(self):
        # 验证手机号和邮箱是否存在
        _resPhone = tableUser.get_user_by(phone_number = g.phone_number)
        _resEmail = tableUser.get_user_by(email = g.email)
        if _resPhone or _resEmail:
            retMsg['msg'] = '账号已经被注册'
            return jsonify(retMsg)

        # 验证密码
        _resPassw = validate.vali_user_password(g.password, g.pass2)
        if _resPassw:
            retMsg['msg'] = _resPassw
            return jsonify(retMsg)

        # 保存用户数据
        _resUser = tableUser.insert_user(g.phone_number, g.email, g.password, g.nickname)
        if not _resUser:
            retMsg['msg'] = '数据库错误'
            return jsonify(retMsg)
        
        return jsonify(retMsg)

class user(Resource):
    '''
    用户验证
    '''
    global retMsg

    @check_token
    def get(self):
        # args = parser.parse_args()
        obj_user = g.user
        phone_number = obj_user.phone_number
        nickname = obj_user.nickname
        retMsg['code'] = 1
        retMsg['phone_number'] = phone_number
        retMsg['nickname'] = nickname
        return jsonify(retMsg)

class logout(Resource):
    '''
    用户注销
    '''
    @check_token
    def get(self):
        user = g.user
        update_dict = {'token': user.token}
        _ret = tableUser.update_user(update_dict)
        if _ret:
            retMsg['code'] = 1
            retMsg['msg'] = '成功注销'
        else:
            retMsg['msg'] = '数据库错误'
        return jsonify(retMsg)


api.add_resource(hello_world, '/main', endpoint = 'hello_world')
api.add_resource(login, '/login', endpoint = 'login')
api.add_resource(register, '/register', endpoint = 'register')
api.add_resource(user, '/user', endpoint = 'user')
api.add_resource(logout, '/logout', endpoint = 'logout')