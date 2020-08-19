from flask import Blueprint, request, jsonify, g, current_app
webIndex = Blueprint('webIndex', __name__, url_prefix = '/index')
# web_user = Blueprint('web_user', __name__, url_prefix = '/user')


from flask_restful import reqparse
from app.libs.tableUser import TableUser

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
parser.add_argument('imgName', type = str)         # 上传图片名
parser.add_argument('imgPath', type = str)         # 上传图片的本地路径
parser.add_argument('artText', type = str)         # 动态内容
parser.add_argument('artSeqid', type = str)        # 动态id
parser.add_argument('artUserId', type = str)      # 动态所属用户id

retMsg = {
    'code': 0,
    'msg': '',
    'data': {}
}

def check_token(func):
    '''
    验证token装饰器
    '''
    def wrapper(*arg, **kwargs):
        # token = request.headers.get('token')
        if not g.token:
            retMsg['msg'] = '需要验证'
            return jsonify(retMsg)
        user = TableUser.get_user_by(token = g.token)
        if not user:
            retMsg['msg'] = '验证信息错误'
            return jsonify(retMsg)

        args = parser.parse_args()
        g.user = user
        g.phoneNumber = args.get('phone_number')           
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
        g.artSeqid = args.get('artSeqid')
        g.artUserId = args.get('artUserId')

        return func(*arg, **kwargs)
    return wrapper


@webIndex.before_request
def get_base_info():
    token = request.headers.get('token')
    if token:
        user = TableUser.get_user_by(token = token)
        g.user = user
        g.token = token
    else:
        g.user = None
    # return {}


import app.web.index