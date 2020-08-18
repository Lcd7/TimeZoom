from flask import request, jsonify, g, current_app
from flask_restful import Api, Resource
from app.web import blue_index, retMsg, parser
from app.libs import tableUser, validator
from app.utils import get_hash, AES_Encrypt
from app.web import check_token
from Crypto.Cipher import AES
import time


api = Api(blue_index)

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

class helloWorld(Resource):
    def get(self):
        return 'Hello_world'

class login(Resource):
    '''
    用户登录
    '''
    @get_user_info_when_login_and_register
    def post(self):
        # global retMsg

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
        _res = tableUser.update_user(user.seqid, _update_user_token_dict)
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
    # global retMsg

    @get_user_info_when_login_and_register
    def post(self):
        # 验证手机号和邮箱是否存在
        _resPhone = tableUser.get_user_by(phone_number = g.phone_number)
        _resEmail = tableUser.get_user_by(email = g.email)
        if _resPhone or _resEmail:
            retMsg['msg'] = '账号已经被注册'
            return jsonify(retMsg)

        # 验证密码
        _resPassw = validator.vali_user_password(g.password, g.passw2)
        if _resPassw:
            retMsg['msg'] = _resPassw
            return jsonify(retMsg)

        # 保存用户数据
        _resUser = tableUser.insert_user(g.phone_number, g.email, g.password, g.nickname)
        if not _resUser:
            retMsg['msg'] = '数据库错误'
            return jsonify(retMsg)
        
        return jsonify(retMsg)

class chageUserInfo(Resource):
    '''
    修改用户信息
    '''
    # global retMsg

    @check_token
    def get(self):
        if g.user:
            # 修改密码
            if g.password and g.passw2 and g.newpassw:
                # 验证密码
                _resPassw = validator.vali_user_password(g.password, g.passw2)
                if not _resPassw:
                    _tmpUpdateDict = {'password': g.password}
                    if not tableUser.update_user(g.user.seqid, _tmpUpdateDict):
                        retMsg['msg'] = '密码修改失败'
                        return jsonify(retMsg)
                else:
                    retMsg['msg'] = _resPassw
                    return jsonify(retMsg)

            # 修改昵称
            if g.nickname:
                if tableUser.get_user_by('nickname'):
                    retMsg['msg'] = '该昵称已存在'
                    return jsonify(retMsg)
                else:
                    _tmpUpdateDict = {'nickname': g.nickname}
                    if not tableUser.update_user(g.user.nickname, _tmpUpdateDict):
                        retMsg['msg'] = '昵称修改失败'
                        return jsonify(retMsg)

            # 修改性别
            if g.sex:
                _tmpUpdateDict = {'sex': g.sex}
                if not tableUser.update_user(g.user.seqid, _tmpUpdateDict):
                    retMsg['msg'] = '性别修改失败'
                    return jsonify(retMsg)

            retMsg['code'] = 1 
            retMsg['msg'] = '修改成功'
            return jsonify(retMsg)
        else:
            retMsg['msg'] = '没有用户信息'
            return jsonify(retMsg)

class logout(Resource):
    '''
    用户注销
    '''
    @check_token
    def get(self):
        user = g.user
        update_dict = {'token': user.token}
        _ret = tableUser.update_user(user.seqid, update_dict)
        if _ret:
            retMsg['code'] = 1
            retMsg['msg'] = '成功注销'
        else:
            retMsg['msg'] = '数据库错误'
        return jsonify(retMsg)


api.add_resource(helloWorld, '/main', endpoint = 'helloWorld')
api.add_resource(login, '/login', endpoint = 'login')
api.add_resource(register, '/register', endpoint = 'register')
api.add_resource(chageUserInfo, '/chageUserInfo', endpoint = 'chageUserInfo')
api.add_resource(logout, '/logout', endpoint = 'logout')