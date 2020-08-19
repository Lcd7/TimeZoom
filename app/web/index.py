from flask import request, jsonify, g, current_app
from flask_restful import Api, Resource
from app.web import webIndex, retMsg, parser
from app.libs import TableUser, Validator
from app.utils import getHash, aesEncrypt
from app.web import check_token
from Crypto.Cipher import AES
import time


api = Api(webIndex)

def get_user_info_when_login_and_register(func):
    '''
    获取用户登录、注册时的信息
    '''
    def wrapper(self):
        args = parser.parse_args()
        g.phoneNumber = args.get('phoneNumber')
        g.password = args.get('password')
        g.email = args.get('email')
        g.sign = args.get('sign')
        g.timenow = args.get('timenow')

        # 验证数据是否被篡改过
        aescryptor = aesEncrypt.Aescrypt(AES.MODE_CBC, current_app.config['AES_KEY'], current_app.config['IV'])
        decSign = aescryptor.AES_Decrypt(g.sign)
        decSign = decSign[:6]
        if decSign == (g.phoneNumber[:3] + g.timenow[:3]):
            return func(self)
        else:
            retMsg['msg'] = '信息被篡改，请求失败'
            return jsonify(retMsg)
    return wrapper

class HelloWorld(Resource):
    def get(self):
        print(request.args.get('a'))
        return 'Hello_world'

class Login(Resource):
    '''
    用户登录
    '''
    @get_user_info_when_login_and_register
    def post(self):
        # global retMsg

        # phoneNumber = request.get_json().get('phoneNumber')
        user = TableUser.get_user_by(phoneNumber = g.phoneNumber)
        if not user:
            user = TableUser.get_user_by(email = g.email)

        if not user:
            retMsg['msg'] = '没有此用户'
            return jsonify(retMsg)

        if user.password != g.password:
            retMsg['msg'] = '密码错误'
            return jsonify(retMsg)

        token = getHash.get_md5(g.phoneNumber, g.password, str(int(time.time())))
        # 将token保存到数据库
        _tmpTokenDict = {'token': token}
        _tmpRes = TableUser.update_user(user.seqid, _tmpTokenDict)
        if _tmpRes:
            retMsg['code'] = 1
            retMsg['msg'] = '成功登录'
            retMsg['nickname'] = user.nickname
            retMsg['token'] = token
        else:
            retMsg['msg'] = '数据库错误'
        return jsonify(retMsg)

class Register(Resource):
    '''
    用户注册
    '''
    # global retMsg

    @get_user_info_when_login_and_register
    def post(self):
        # 验证手机号和邮箱是否存在
        _tmpResPhone = TableUser.get_user_by(phoneNumber = g.phoneNumber)
        _tmpResEmail = TableUser.get_user_by(email = g.email)
        if _tmpResPhone or _tmpResEmail:
            retMsg['msg'] = '账号已经被注册'
            return jsonify(retMsg)

        # 验证密码
        _tmpResPassw = Validator.vali_user_password(g.password, g.passw2)
        if _tmpResPassw:
            retMsg['msg'] = _tmpResPassw
            return jsonify(retMsg)

        # 保存用户数据
        _tmpResUser = TableUser.insert_user(g.phoneNumber, g.email, g.password, g.nickname)
        if not _tmpResUser:
            retMsg['msg'] = '数据库错误'
            return jsonify(retMsg)
        
        retMsg['code'] = 1
        return jsonify(retMsg)


api.add_resource(HelloWorld, '/main', endpoint = 'HelloWorld')
api.add_resource(Login, '/login', endpoint = 'Login')
api.add_resource(Register, '/register', endpoint = 'Register')