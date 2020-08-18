
from flask import request, jsonify, g, current_app
from flask_restful import Api, Resource
from app.web import web_user, retMsg
from app.libs import tableUser, tableImg, validator
from app.web import check_token
from app.utils.qiniu import QiNiuImage


api = Api(web_user)

class chageInfo(Resource):
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

class changeAvatar(Resource):
    '''
    更换头像
    '''
    @check_token
    def post(self):
        if g.img_name:
            Q = QiNiuImage(current_app.config['BUCKET'], current_app.config['AK'], current_app.config['SK'])
            _res_upload = Q.upload_image(g.img_name, g.img_path)

            # 保存图片链接
            if _res_upload:
                head_pic = '七牛云路径' + g.img_name
                _res = tableImg.insert_img(g.img_name, head_pic, g.user.seqid, img_type = 2)
                if not _res:
                    retMsg['msg'] = '动态上传失败'
                else:
                    retMsg['code'] = 1

class addFriend(Resource):
    '''
    添加好友
    '''
    @check_token
    def get(self):
        f_seqid = request.args.get('seqid')
        if len(tableUser.get_friends(g.user.seqid)) <= 50:
            _res = tableUser.add_friend(g.user.seqid, f_seqid)
            if not _res:
                retMsg['msg'] = '添加好友失败'
                return jsonify(retMsg)
        else:
            retMsg['msg'] = '好友超过上限'
            return jsonify(retMsg)

        retMsg['code'] = 1
        return jsonify(retMsg)

class getFriends(Resource):
    '''
    获取好友列表
    '''
    @check_token
    def get(self):
        _res = tableUser.get_friends(g.user.seqid)
        if not _res:
            retMsg['msg'] = '查询失败'
        else:
            retMsg['data'] = ','.join(_res)
            retMsg['code'] = 1
        return jsonify(retMsg)



api.add_resource(chageInfo, '/chageInfo', endpoint = 'chageInfo')
api.add_resource(logout, '/logout', endpoint = 'logout')
api.add_resource(changeAvatar, '/changeAvatar', endpoint = 'changeAvatar')
api.add_resource(addFriend, '/addFriend', endpoint = 'addFriend')
api.add_resource(getFriends, '/getFriends', endpoint = 'getFriends')