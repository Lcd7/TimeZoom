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



def test_AES_encrypt():
    from Crypto.Cipher import AES
    import base64

    class Aescrypt():
        '''
        密钥（key）, 密斯偏移量（iv） CBC模式加密
        '''
        BLOCK_SIZE = 16  # Bytes

        def __init__(self, key, model, iv):
            self.key = key
            self.model = model
            self.iv = iv

        def pad(self, data):
            data = data + (self.BLOCK_SIZE - len(data) % self.BLOCK_SIZE) * \
                    chr(self.BLOCK_SIZE - len(data) % self.BLOCK_SIZE)
            return data
        
        def unpad(self, data):
            return data[:-ord(data[len(data) - 1:])]

        def AES_Encrypt(self, data):
            # 字符串补位
            data = self.pad(data)
            
            if self.model == AES.MODE_CBC:
                cipher = AES.new(self.key.encode('utf8'), self.model, self.iv.encode('utf8'))
            elif self.model == AES.MODE_ECB:
                cipher = AES.new(self.key.encode('utf8'), self.model)

            encryptedbytes = cipher.encrypt(data.encode('utf8'))

            # 加密后得到的是bytes类型的数据，使用Base64进行编码,返回byte字符串
            encodestrs = base64.b64encode(encryptedbytes)

            # 对byte字符串按utf-8进行解码
            enctext = encodestrs.decode('utf8')
            print(enctext)
            return enctext


        def AES_Decrypt(self, data):
            data = data.encode('utf8')
            encodebytes = base64.decodebytes(data)

            # 将加密数据转换位bytes类型数据
            if self.model == AES.MODE_CBC:
                cipher = AES.new(self.key.encode('utf8'), self.model, self.iv.encode('utf8'))
            elif self.model == AES.MODE_ECB:
                cipher = AES.new(self.key.encode('utf8'), self.model)

            text_decrypted = cipher.decrypt(encodebytes)

            # 去补位
            text_decrypted = self.unpad(text_decrypted)
            text_decrypted = text_decrypted.decode('utf8')
            print(text_decrypted)
            return text_decrypted

    data = "holy"
    iv = '0102030405060708'
    key = 'lcd12345fp123456'
    aescryptor = Aescrypt(key, AES.MODE_CBC, iv) # CBC模式
    # aescryptor = Aescrypt(key, AES.MODE_ECB, "") # ECB模式
    
    enctext = aescryptor.AES_Encrypt(data)
    aescryptor.AES_Decrypt(enctext)


if __name__ == "__main__":
    import time
    print(str(int(time.time())))

    