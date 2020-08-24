
from flask import request, jsonify, g, current_app
from flask_restful import Api, Resource
from app.web import webIndex
from app.libs import TableUser, TableImg, Validator
from app.web import check_token
from app.utils.qiNiu import QiNiuImage


api = Api(webIndex)

class getInfo(Resource):
    '''
    获取用户信息
    params: none 
    '''
    @check_token
    def get(self):
        g.retMsg['data'] = {
            'phoneNumber': g.user.phoneNumber,
            'email': g.user.email,
            'nickname': g.user.nickname,
            'sex': g.user.sex,
            }
        avatar = g.tableImg.get_avatar(g.user.seqid)
        if avatar:
            g.retMsg['data']['avatar'] =  avatar.headPic,
        
        return jsonify(g.retMsg)

class ChageInfo(Resource):
    '''
    修改用户信息
    params: *password
    params: *newpassw
    params: *nickname
    params: *sex
    '''
    @check_token
    def post(self):
        # 修改密码
        if g.password and g.newpassw:
            if g.user.password == g.password:
                _tmpUpdateDict = {'password': g.newpassw}
                if not g.tableUser.update_user(g.user.seqid, _tmpUpdateDict):
                    g.retMsg['msg'] = '密码修改失败'
                    return jsonify(g.retMsg)
            else:
                g.retMsg['msg'] = '原密码错误'
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
 
class Logout(Resource):
    '''
    用户注销
    params: none
    '''
    @check_token
    def get(self):
        _tmpUpdateDict = {'token': ''}
        _ret = g.tableUser.update_user(g.user.seqid, _tmpUpdateDict)
        if _ret:
            g.retMsg['code'] = 1
            g.retMsg['msg'] = '成功注销'
        else:
            g.retMsg['msg'] = '数据库错误'
        return jsonify(g.retMsg)

class ChangeAvatar(Resource):
    '''
    更换头像
    params: imgName
    params: imgPath
    '''
    @check_token
    def post(self):
        if g.imgName:
            Q = QiNiuImage(current_app.config['QN_BUCKET'], current_app.config['QN_AK'], current_app.config['QN_KEY'])
            _tmpResUpload = Q.upload_image(g.imgName, g.imgPath)

            # 保存头像链接
            if _tmpResUpload:
                # 先删除当前头像
                # g.tableImg.delete_img(g.user.seqid, imgType = 2)

                # 上传新头像
                headPic = current_app.config['QN_URL'] + g.imgName
                _tmpRes = g.tableImg.insert_img(g.imgName, headPic, g.user.seqid, imgType = 2)
                if not _tmpRes:
                    g.retMsg['msg'] = '头像上传失败'
                else:
                    g.retMsg['code'] = 1
        else:
            g.retMsg['msg'] = '头像上传失败：没有文件名'

        return jsonify(g.retMsg)

class AddFriend(Resource):
    '''
    添加好友
    params: friendSeqid
    '''
    @check_token
    def post(self):
        '''
        添加好友
        '''
        friendId = request.args.get('friendSeqid')
        if friendId:
            if len(g.tableUser.get_friends(g.user.seqid)) <= 50:
                _tmpRes = g.tableUser.add_friend(g.user.seqid, friendId)
                if not _tmpRes:
                    g.retMsg['msg'] = '添加好友失败'
                    return jsonify(g.retMsg)
            else:
                g.retMsg['msg'] = '好友超过上限'
                return jsonify(g.retMsg)
        else:
            g.retMsg['msg'] = f"无效id：'{friendId}'"

        g.retMsg['code'] = 1
        return jsonify(g.retMsg)
    
class DeleteFriend(Resource):
    '''
    删除好友
    params: friendSeiqd
    '''
    @check_token
    def post(self):
        friendId = request.args.get('FriendSeqid')
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
    params: friendSeqid
    params: answer
    '''
    @check_token
    def post(self):
        friendId = int(request.args.get('friendSeqid'))
        answer = bool(request.args.get('answer'))
        _tmpRes = g.tableUser.answer_friend(g.user.seqid, friendId, answer)
        if _tmpRes:
            g.retMsg['code'] = 1
        else:
            g.retMsg['msg'] = '请求失败'
                
            
        return jsonify(g.retMsg)   

class GetFriends(Resource):
    '''
    获取好友列表
    params: none
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
api.add_resource(DeleteFriend, '/deleteFriend', endpoint = 'DeleteFriend')
api.add_resource(AnswerFriend, '/answerFriend', endpoint = 'AnsweeFriend')
api.add_resource(GetFriends, '/getFriends', endpoint = 'GetFriends')