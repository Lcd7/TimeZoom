from app import creat_app
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from geventwebsocket.websocket import WebSocket
from werkzeug.debug import DebuggedApplication
app = creat_app()

if __name__ == "__main__":
    # app.run('0.0.0.0', 8058, debug = True)

    # WSGIServer服务
    debug_app = DebuggedApplication(app, evalex = True)
    server = WSGIServer(('127.0.0.1',8058), debug_app, handler_class = WebSocketHandler)
    server.serve_forever()