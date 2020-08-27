from flask import  Flask ,request,render_template
from  geventwebsocket.websocket import WebSocket,WebSocketError
from  geventwebsocket.handler import WebSocketHandler
from  gevent.pywsgi import WSGIServer

import json

app = Flask(__name__)

@app.route('/index/')
def index():
    return render_template('one2one.html')

user_socket_list = []
user_socket_dict={}

@app.route('/ws/<username>')
def ws(username):
    user_socket=request.environ.get("wsgi.websocket")
    if not user_socket:
        return "请以WEBSOCKET方式连接"

    user_socket_dict[username]=user_socket
    print(user_socket_dict)

    while True:
        try:
            user_msg = user_socket.receive()
            user_msg=json.loads(user_msg)
            to_user_socket = user_socket_dict.get(user_msg.get("to_user"))
            send_msg={
                "send_msg":user_msg.get("send_msg"),
                "send_user":username
            }
            to_user_socket.send(json.dumps(send_msg))
        except WebSocketError as e:
            user_socket_dict.pop(username)
            print(user_socket_dict)
            print(e)


if __name__ == '__main__':

    http_serve=WSGIServer(("127.0.0.1", 8058),app,handler_class=WebSocketHandler)
    http_serve.serve_forever()