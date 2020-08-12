def test_marshal_with():
    '''
    格式化输出
    '''
    from flask import Flask,Blueprint
    from flask_restful import Resource, Api,reqparse,marshal_with,fields
    # from flask_docs import ApiDoc

    app = Flask(__name__)
    app.config['API_DOC_MEMBER'] = ['blue']


    # ApiDoc(app, title='Sample App Restful', version='0.1.4')

    blue=Blueprint('blue',__name__)
    tt={
        'test':   fields.String,
        'vv':    fields.String
    }
    @blue.route("/test",methods=['POST'])
    def post():
        """Submission of data
            Args:
                pass

            Returns:
                pas
        """
        parse=reqparse.RequestParser()
        parse.add_argument("test",type=str)
        parse.add_argument("test1",type=str)
        pp=parse.parse_args()
        print(pp)
        return {'test1': pp['test1']}
    @blue.route("/tt",methods=["GET"])
    @marshal_with(tt)
    def get():
        """
            @@@
            #### args
            | args | nullable | type | remark |
            |--------|--------|--------|--------|
            |    id    |    false    |    int   |    todo id    |
            #### return
            - ##### json
            > {...}
            @@@
        """
        return {'todos': 'get todolist',"tt":"tt","vv":"vv"}


    app.register_blueprint(blue,url_prefix='/blue')

    app.run(port=5000, debug=True)

def GouZi():
    '''
    flask4个钩子函数的使用

    1.before_first_request
    在处理第一个请求前执行

    2.before_request
    在每次请求前执行；如果在某修饰的函数中返回了一个相应，视图函数将不再被调用。

    3.after_request
    在每次请求后执行（如果没有抛出错误）；接收一个参数：视图函数做出的相应，在此函数中可以对响应值在返回之前做最后一步修改处理，需要将参数中的相应在此参数中进行返回。

    4.teardown_request
    在每次请求后执行；接收一个参数：错误信息，如果有相关错误抛出，需要设置flask的配置DEBUG=False，teardown_request才会接收到异常对象。

    '''
    # from settings.dev import DevConfig
    from flask import Flask
    app = Flask(__name__)
    # 项目配置
    # app.config.from_object(DevConfig)

    @app.before_first_request
    def before_first_request():
        print("----before_first_request----")
        print("系统初始化的时候,执行这个钩子方法")
        print("会在接收到第一个客户端请求时,执行这里的代码")

    @app.before_request
    def before_request():
        print("----before_request----")
        print("每一次接收到客户端请求时,执行这个钩子方法")
        print("一般可以用来判断权限,或者转换路由参数或者预处理客户端请求的数据")
        print('注意:该函数不需要任何参数，如果其返回了一个非空的值，则其将会作为当前视图的返回值,看下面的例子')

    @app.after_request
    def after_request(response):
        print("----after_request----")
        print("在处理请求以后,执行这个钩子方法")
        print("一般可以用于记录会员/管理员的操作历史,浏览历史,清理收尾的工作")
        response.headers["Content-Type"] = "application/json"
        # 必须返回response参数
        return response


    @app.teardown_request
    def teardown_request(exc):
        print("----teardown_request----")
        print("在每一次请求以后,执行这个钩子方法,如果有异常错误,则会传递错误异常对象到当前方法的参数中")
        print(exc)

    @app.route("/")
    def index():
        print("----视图函数----")
        print("视图函数被运行了")
        return "视图函数被运行了<br>"

    if __name__ == '__main__':
        app.run(host="0.0.0.0", port=80)

def blueprint_test():
    from flask import Flask
    app = Flask(__name__)

    from flask import Blueprint
    blue_index = Blueprint("index", __name__)
    
    from flask_restful import Api, Resource, reqparse
    api = Api(blue_index)


    def before_main(func):
        def wrapper(*args, **kwargs):
            print('before_main')
            return func(*args, **kwargs)
        return wrapper


    @blue_index.before_request
    def before():
        print("before")


    @blue_index.route('/')
    def yyy():
        print('111')
        return '111'

    class main(Resource):
        @before_main
        def get(self):
            print('hello')
            return 'hello'


    api.add_resource(main, '/main/', endpoint = 'main')
    app.register_blueprint(blue_index)
    app.run('0.0.0.0', 8058, debug = True)


from flask import Blueprint
blue_index = Blueprint("index", __name__, url_prefix = '/index')

if __name__ == '__main__':
    blueprint_test()
    