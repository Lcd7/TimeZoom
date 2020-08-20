
from flask import request, jsonify, g, current_app
from flask_restful import Api, Resource
from app.web import webIndex
from app.libs import TableUser, TableImg, Validator
from app.web import check_token
from app.utils.qiNiu import QiNiuImage


api = Api(webIndex)

class ChageInfo(Resource):
    '''
    修改用户信息
    '''
    # global g.retMsg

    @check_token
    def get(self):
        if g.user:
            # 修改密码
            if g.password and g.passw2 and g.newpassw:
                # 验证密码
                _tmpResPassw = Validator.vali_user_password(g.password, g.passw2)
                if not _tmpResPassw:
                    _tmpUpdateDict = {'password': g.password}
                    if not g.tableUser.update_user(g.user.seqid, _tmpUpdateDict):
                        g.retMsg['msg'] = '密码修改失败'
                        return jsonify(g.retMsg)
                else:
                    g.retMsg['msg'] = _tmpResPassw
                    return jsonify(g.retMsg)

            # 修改昵称
            if g.nickname:
                if g.tableUser.get_user_by('nickname'):
                    g.retMsg['msg'] = '该昵称已存在'
                    return jsonify(g.retMsg)
                else:
                    _tmpUpdateDict = {'nickname': g.nickname}
                    if not g.tableUser.update_user(g.user.nickname, _tmpUpdateDict):
                        g.retMsg['msg'] = '昵称修改失败'
                        return jsonify(g.retMsg)

            # 修改性别
            if g.sex:
                _tmpUpdateDict = {'sex': g.sex}
                if not g.tableUser.update_user(g.user.seqid, _tmpUpdateDict):
                    g.retMsg['msg'] = '性别修改失败'
                    return jsonify(g.retMsg)

            g.retMsg['code'] = 1 
            g.retMsg['msg'] = '修改成功'
            return jsonify(g.retMsg)
        else:
            g.retMsg['msg'] = '没有用户信息'
            return jsonify(g.retMsg)

class Logout(Resource):
    '''
    用户注销
    '''
    @check_token
    def get(self):
        user = g.user
        _tmpUpdateDict = {'token': user.token}
        _ret = g.tableUser.update_user(user.seqid, _tmpUpdateDict)
        if _ret:
            g.retMsg['code'] = 1
            g.retMsg['msg'] = '成功注销'
        else:
            g.retMsg['msg'] = '数据库错误'
        return jsonify(g.retMsg)

class ChangeAvatar(Resource):
    '''
    更换头像
    '''
    @check_token
    def post(self):
        if g.imgName:
            Q = QiNiuImage(current_app.config['BUCKET'], current_app.config['AK'], current_app.config['SK'])
            _tmpResUpload = Q.upload_image(g.imgName, g.imgPath)

            # 保存图片链接
            if _tmpResUpload:
                headPic = '七牛云路径' + g.imgName
                _tmpRes = g.tableImg.insert_img(g.imgName, headPic, g.user.seqid, imgType = 2)
                if not _tmpRes:
                    g.retMsg['msg'] = '动态上传失败'
                else:
                    g.retMsg['code'] = 1

class AddFriend(Resource):
    '''
    添加好友
    '''
    @check_token
    def get(self):
        '''
        添加好友
        '''
        friendId = request.args.get('seqid')
        if len(g.tableUser.get_friends(g.user.seqid)) <= 50:
            _tmpRes = g.tableUser.add_friend(g.user.seqid, friendId)
            if not _tmpRes:
                g.retMsg['msg'] = '添加好友失败'
                return jsonify(g.retMsg)
        else:
            g.retMsg['msg'] = '好友超过上限'
            return jsonify(g.retMsg)

        g.retMsg['code'] = 1
        return jsonify(g.retMsg)
    
    @check_token
    def post(self):
        '''
        删除好友
        '''
        friendId = request.args.get('seqid')
        if g.tableUser.get_friend(g.user.seqid, friendId):
            _tmpRes = g.tableUser.delete_friend(g.user.seqid, friendId)
            if _tmpRes:
                g.retMsg['code'] = 1
            else:
                g.retMsg['msg'] = '删除好友失败'

        return jsonify(g.retMsg)    

class AnswerFriend(Resource):
    '''
    回应好友请求
    '''
    @check_token
    def post(self):
        friendId = request.args.get('seqid')
        answer = request.args.get('answer')
        _tmpRes = g.tableUser.answer_friend(g.user.seqid, friendId, answer)
        if _tmpRes:
            if _tmpRes:
                g.retMsg['code'] = 1
            else:
                g.retMsg['msg'] = '请求失败'
            
        return jsonify(g.retMsg)   

class GetFriends(Resource):
    '''
    获取好友列表
    '''
    @check_token
    def get(self):
        _tmpRes = g.tableUser.get_friends(g.user.seqid)
        if not _tmpRes:
            g.retMsg['msg'] = '查询失败'
        else:
            g.retMsg['data'] = ','.join(_tmpRes)
            g.retMsg['code'] = 1
        return jsonify(g.retMsg)



api.add_resource(ChageInfo, '/chageInfo', endpoint = 'ChageInfo')
api.add_resource(Logout, '/logout', endpoint = 'Logout')
api.add_resource(ChangeAvatar, '/changeAvatar', endpoint = 'ChangeAvatar')
api.add_resource(AddFriend, '/addFriend', endpoint = 'AddFriend')
api.add_resource(GetFriends, '/getFriends', endpoint = 'GetFriends')