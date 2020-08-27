import json
from app.web import webIndex, check_token
from flask import request, jsonify, g, current_app, render_template, abort
from flask_restful import Api, Resource
from logger import log
# from app.libs.tableLetter

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
                user_dict.pop(mySeqid)
                log.error(e)


api.add_resource(Chat, '/user/chat', endpoint = 'Chat')

@webIndex.route('/webchat')
def webchat():
    return render_template('web_chat.html')

if __name__ == '__main__':
    pass
    # dapp = DebuggedApplication(webIndex, evalex = True)
    # server = WSGIServer(('127.0.0.1',8058), dapp, handler_class = WebSocketHandler)
    # server.serve_forever()