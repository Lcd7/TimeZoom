from flask import Blueprint, request, jsonify, g, current_app
blue_index = Blueprint('blue_index', __name__, url_prefix = '/index')


from flask_restful import reqparse
from app.libs.tableUser import tableUser

parser = reqparse.RequestParser()
parser.add_argument('phone_number', type = str)     # 用户账号 （电话）
parser.add_argument('email', type = str)            # 用户密码
parser.add_argument('password', type = str)         # 用户邮箱
parser.add_argument('passw2', type = str)           # 用户再次确认密码
parser.add_argument('newpassw', type = str)         # 用户新密码
parser.add_argument('nickname', type = str)         # 用户昵称
parser.add_argument('sex', type = str)              # 用户性别
parser.add_argument('sign', type = str)             # 防篡改标志 sign
parser.add_argument('timenow', type = str)          # 用户当前时间戳
parser.add_argument('img_name', type = str)         # 上传图片名
parser.add_argument('img_path', type = str)         # 上传图片的本地路径
parser.add_argument('art_text', type = str)         # 动态内容

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

        args = parser.parse_args()
        g.user = user
        g.phone_number = args.get('phone_number')           
        g.password = args.get('password')                   
        g.email = args.get('email')                         
        g.passw2 = args.get('passw2')                       
        g.newpassw = args.get('newpassw')                   
        g.nickname = args.get('nickname')                   
        g.sex = args.get('sex')                             
        g.sign = args.get('sign')                           
        g.timenow = args.get('timenow')                     
        g.img_name = args.get('img_name')                   
        g.img_path = args.get('img_path')                   
        g.art_text = args.get('art_text')

        return func(*arg, **kwargs)
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


import app.web.users