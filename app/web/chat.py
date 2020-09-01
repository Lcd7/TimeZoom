import json
from app.web import webIndex, check_token
from flask import request, jsonify, g, current_app, render_template, abort
from flask_restful import Api, Resource
from logger import log

user_dict = {}
api = Api(webIndex)

class Chat(Resource):
    '''
    聊天
    '''
    # @check_token
    def get(self):
        mySeqid = request.args.get('mySeqid')
        # 删除未读聊天
            # pass

        user_socket = request.environ.get('wsgi.websocket') # type:WebSocket
        if not user_socket:
            abort(400, 'Expected WebSocket request.')

        user_dict[mySeqid] = user_socket

        while True:
            try:
                # 等待接收客户端发来的数据
                msg = user_socket.receive()  
                msg_dict = json.loads(msg)
                msg_dict['from_user'] = mySeqid
                to_user = msg_dict.get('to_user')

                # 如果用户名是空表示群发
                # if to_user == "":  
                #     for uname, uwebsocket in user_dict.items():
                #         if uname == mySeqid:  # 群发时不用给自己发
                #             continue
                #         uwebsocket.send(json.dumps(msg_dict))
                #     continue

                to_user_socket = user_dict.get(to_user)
                if not to_user_socket:  # 判断用户字典中是否存在用户的websocket连接
                    continue
                    # 记录存在数据库
                    # g.tableLetter.insert(g.user.seqid, mySeqid, 1, msg_dict['message'])
                try:
                    to_user_socket.send(json.dumps(msg_dict))
                except:
                    user_dict.pop(to_user)
            except Exception as e:
                if mySeqid in user_dict:
                    user_dict.pop(mySeqid)
                log.error(e)

class GetLetter(Resource):
    '''
    获取聊天记录
    '''
    @check_token
    def get(self):
        if g.friendSeqid:
            letterDict = g.tableLetter.get_letter_by(g.user.seqid, g.friendSeqid)
        else:
            g.retMsg['msg'] = '没有好友id'
            return jsonify(g.retMsg)

        g.retMsg['status'] = 1
        g.retMSg['code'] = 200
        g.retMsg['data'] = letterDict
        return jsonify(g.retMsg)

class GetUnreadLetter(Resource):
    '''
    获取未读聊天记录
    '''
    @check_token
    def get(self):
        if g.friendSeqid:
            letterDict = g.tableLetter.get_letter_by(g.user.seqid, g.friendSeqid, status = 0)
        else:
            g.retMsg['msg'] = '没有好友id'
            return jsonify(g.retMsg)

        g.retMsg['status'] = 1
        g.retMSg['code'] = 200
        g.retMsg['data'] = letterDict
        return jsonify(g.retMsg)

class DeleteUserLetter(Resource):
    '''
    删除用户聊天记录
    '''
    @check_token
    def post(self):
        if g.friendSeqid:
            _tmpRes = g.tableLetter.delete_letter(userid = g.user.seqid, friendid = g.friendSeqid)
            if not _tmpRes:
                g.retMsg['msg'] = '删除失败'
        else:
            g.retMsg['msg'] = '没有好友id'
            return jsonify(g.retMsg)

        g.retMsg['status'] = 1
        g.retMSg['code'] = 200
        return jsonify(g.retMsg)
    
class DeleteOneLetter(Resource):
    '''
    删除一条聊天记录
    '''
    @check_token
    def post(self):
        letterid = int(request.args.get('letterid'))
        if letterid:
            _tmpRes = g.tableLetter.delete_letter(seqid = letterid)
            if not _tmpRes:
                g.retMsg['msg'] = '删除失败'
        else:
            g.retMsg['msg'] = '记录不存在'

        g.retMsg['status'] = 1
        g.retMSg['code'] = 200
        return jsonify(g.retMsg)

class Withdrawn(Resource):
    '''
    撤回消息
    '''
    @check_token
    def post(self):
        sendTime = request.args.get('sendTime')
        _tmpRes = g.tableLetter.withdrawn_letter(g.user.seqid, g.friendSeqid, sendTime)
        if not _tmpRes:
            g.retMsg['msg'] = '撤回失败'

        g.retMsg['status'] = 1
        g.retMSg['code'] = 200
        return jsonify(g.retMsg)

class SaveLetter(Resource):
    '''
    保存聊天记录
    '''
    @check_token
    def post(self):
        text = request.args.get('text')
        status = int(request.args.get('status'))
        _tmpRes = g.tableLetter.save_letter(g.user.seqid, g.friendSeqid, text, status)
        if not _tmpRes:
            g.retMsg['msg'] = '保存失败'

        g.retMsg['status'] = 1
        g.retMSg['code'] = 200
        return jsonify(g.retMsg)

api.add_resource(Chat, '/letter', endpoint = 'Chat')
api.add_resource(GetLetter, '/letter/get', endpoint = 'GetLetter')
api.add_resource(GetUnreadLetter, '/letter/unread/get', endpoint = 'GetUnreadLetter')
api.add_resource(DeleteUserLetter, '/letter/deleteall', endpoint = 'DeleteUserLetter')
api.add_resource(DeleteOneLetter, '/letter/deleteone', endpoint = 'DeleteOneLetter')
api.add_resource(Withdrawn, '/letter/withdrawn', endpoint = 'Withdrawn')
api.add_resource(SaveLetter, '/letter/save', endpoint = 'SaveLetter')


if __name__ == '__main__':
    pass
    # dapp = DebuggedApplication(webIndex, evalex = True)
    # server = WSGIServer(('127.0.0.1',8058), dapp, handler_class = WebSocketHandler)
    # server.serve_forever()