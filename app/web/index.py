from flask import request, jsonify, g, current_app, render_template
from flask_restful import Api, Resource
from app.web import webIndex, parser
from app.libs import TableUser, Validator
from app.utils import getHash, aesEncrypt, valiImg
from app.web import check_token, create_token
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
        g.passw2 = args.get('passw2')
        g.email = args.get('email')
        g.nickname = args.get('nickname')
        g.sign = args.get('sign')
        g.timenow = args.get('timenow')
        g.sex = request.args.get('sex')
        g.tableUser = TableUser()

        # 验证数据是否被篡改过
        aescryptor = aesEncrypt.Aescrypt(AES.MODE_CBC, current_app.config['AES_KEY'], current_app.config['IV'])
        decSign = aescryptor.AES_Decrypt(g.sign)
        decSign = decSign[:6]
        if decSign == (g.phoneNumber[:3] + g.timenow[:3]):
            return func(self)
        else:
            g.retMsg['msg'] = '信息被篡改，请求失败'
            return jsonify(g.retMsg)
    return wrapper

class HelloWorld(Resource):
    def get(self):
        '''
        登录表单页
        params: none
        '''
        # print(request.args.get('a'))
        # img_text, image_base64 = valiImg.Captcha.gene_graph_captcha()
        # g.retMsg['img_text'] = img_text
        # g.retMsg['img_base64'] = image_base64
        # g.retMsg['status'] = 1
        # g.retMsg['code'] = 200
        # return jsonify(g.retMsg)
        render_template('login/login.html')

    def post(self):
        a = request.args.get('a')
        b = request.form.get('b')
        g.retMsg['a'] = a
        g.retMsg['b'] = b
        g.retMsg['status'] = 1
        g.retMsg['code'] = 200
        return jsonify(g.retMsg)

class Login(Resource):
    '''
    用户登录
    params: *phoneNumber
    params: *email
    params: password
    params: timenow
    '''
    @get_user_info_when_login_and_register
    def post(self):

        user = g.tableUser.get_user_by(phoneNumber = g.phoneNumber)
        if not user:
            user = g.tableUser.get_user_by(email = g.email)

        if not user:
            g.retMsg['msg'] = '没有此用户'
            return jsonify(g.retMsg)

        if user.password != g.password:
            g.retMsg['msg'] = '密码错误'
            return jsonify(g.retMsg)

        if user.ban == 1:
            g.retMsg['msg'] = '账号被封禁，请联系管理员'
            g.retMsg['status'] = 1
            g.retMsg['code'] = 200
            return jsonify(g.retMsg)

        payload = {
            'nickname': user.nickname,
        }
        token = create_token(payload)
        g.tableUser.update_user(g.user.seqid, {'token': token})

        g.retMsg['status'] = 1
        g.retMsg['code'] = 200
        g.retMsg['msg'] = '成功登录'        
        g.retMsg['data']['token'] = token
        
        return jsonify(g.retMsg)

class Register(Resource):
    '''
    用户注册
    params: phoneNumber
    params: *email
    params: nickname
    params: *sex
    '''

    @get_user_info_when_login_and_register
    def post(self):
        _tmpResPhone = g.tableUser.get_user_by(phoneNumber = g.phoneNumber)
        _tmpResEmail = g.tableUser.get_user_by(email = g.email)
        _tmpResNickname = g.tableUser.get_user_by(nickname = g.nickname)

        # 验证手机号是否存在
        if _tmpResPhone:
            g.retMsg['msg'] = '电话已经被注册'
            return jsonify(g.retMsg)

        # 验证邮箱是否存在
        if _tmpResEmail:
            g.retMsg['msg'] = '用户名已被注册'
            return jsonify(g.retMsg)

        # 验证用户名是否存在
        if _tmpResNickname:
            g.retMsg['msg'] = '用户名已被注册'
            return jsonify(g.retMsg)

        # 验证密码 (应该是前端验证)
        # _tmpResPassw = Validator.vali_user_password(g.password, g.passw2)
        # if _tmpResPassw:
        #     g.retMsg['msg'] = _tmpResPassw
        #     return jsonify(g.retMsg)

        # 保存用户数据
        _tmpResUser = g.tableUser.insert_user(g.phoneNumber, g.email, g.password, g.nickname, g.sex)
        if not _tmpResUser:
            g.retMsg['msg'] = '数据库错误'
            return jsonify(g.retMsg)
        
        g.retMsg['status'] = 1
        return jsonify(g.retMsg)


api.add_resource(HelloWorld, '/main', endpoint = 'HelloWorld')
api.add_resource(Login, '/user/login', endpoint = 'Login')
api.add_resource(Register, '/index/register', endpoint = 'Register')