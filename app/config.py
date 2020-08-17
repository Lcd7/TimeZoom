from app.models import User

class BaseConfig:
    """
    配置基类，公用配置写在这里
    """
    # MODELS字典，存放模型名称：模型
    MODELS = {'User': User}
    # json 返回中文
    JSON_AS_ASCII = False
    # AES密钥
    AES_KEY = 'lcd12345fp123456'
    # AES 偏移向量
    IV = '0102030405060708'



class DevelopmentConfig(BaseConfig):
    """
    开发环境配置类
    """
    DATABASE_URI = r"DRIVER={SQL Server Native Client 11.0};SERVER=192.168.8.16;DATABASE=crawler_test;UID=sa;PWD=root123."
    # 七牛服务器配置
    BUCKET = ''
    AK = ''
    Sk = ''
    

class TestConfig(BaseConfig):
    """
    测试环境配置类
    """
    pass


class ProductionConfig(BaseConfig):
    """
    生产环境配置类
    """
    pass
    
# 配置类字典，根据传递的 key 选择不同的配置类
configs = {
    "development": DevelopmentConfig,
    "test": TestConfig,
    "production": ProductionConfig
}




def tips():
    '''
    config中可以更改的键值对如下 :
    '''
    
    _tips_dict = {
        'DEBUG': False,  # 是否开启Debug模式
        'TESTING': False,  # 是否开启测试模式
        'PROPAGATE_EXCEPTIONS': None,  # 异常传播(是否在控制台打印LOG) 当Debug或者testing开启后,自动为True
        'PRESERVE_CONTEXT_ON_EXCEPTION': None,  # 一两句话说不清楚,一般不用它
        'SECRET_KEY': None,  # 之前遇到过,在启用Session的时候,一定要有它
        'PERMANENT_SESSION_LIFETIME': 31,  # days , Session的生命周期(天)默认31天
        'USE_X_SENDFILE': False,  # 是否弃用 x_sendfile
        'LOGGER_NAME': None,  # 日志记录器的名称
        'LOGGER_HANDLER_POLICY': 'always',
        'SERVER_NAME': None,  # 服务访问域名
        'APPLICATION_ROOT': None,  # 项目的完整路径
        'SESSION_COOKIE_NAME': 'session',  # 在cookies中存放session加密字符串的名字
        'SESSION_COOKIE_DOMAIN': None,  # 在哪个域名下会产生session记录在cookies中
        'SESSION_COOKIE_PATH': None,  # cookies的路径
        'SESSION_COOKIE_HTTPONLY': True,  # 控制 cookie 是否应被设置 httponly 的标志，
        'SESSION_COOKIE_SECURE': False,  # 控制 cookie 是否应被设置安全标志
        'SESSION_REFRESH_EACH_REQUEST': True,  # 这个标志控制永久会话如何刷新
        'MAX_CONTENT_LENGTH': None,  # 如果设置为字节数， Flask 会拒绝内容长度大于此值的请求进入，并返回一个 413 状态码
        'SEND_FILE_MAX_AGE_DEFAULT': 12,  # hours 默认缓存控制的最大期限
        'TRAP_BAD_REQUEST_ERRORS': False,
        # 如果这个值被设置为 True ，Flask不会执行 HTTP 异常的错误处理，而是像对待其它异常一样，
        # 通过异常栈让它冒泡地抛出。这对于需要找出 HTTP 异常源头的可怕调试情形是有用的。
        'TRAP_HTTP_EXCEPTIONS': False,
        # Werkzeug 处理请求中的特定数据的内部数据结构会抛出同样也是“错误的请求”异常的特殊的 key errors 。
        # 同样地，为了保持一致，许多操作可以显式地抛出 BadRequest 异常。
        # 因为在调试中，你希望准确地找出异常的原因，这个设置用于在这些情形下调试。
        # 如果这个值被设置为 True ，你只会得到常规的回溯。
        'EXPLAIN_TEMPLATE_LOADING': False,
        'PREFERRED_URL_SCHEME': 'http',  # 生成URL的时候如果没有可用的 URL 模式话将使用这个值
        'JSON_AS_ASCII': True,
        # 默认情况下 Flask 使用 ascii 编码来序列化对象。如果这个值被设置为 False ，
        # Flask不会将其编码为 ASCII，并且按原样输出，返回它的 unicode 字符串。
        # 比如 jsonfiy 会自动地采用 utf-8 来编码它然后才进行传输。
        'JSON_SORT_KEYS': True,
        #默认情况下 Flask 按照 JSON 对象的键的顺序来序来序列化它。
        # 这样做是为了确保键的顺序不会受到字典的哈希种子的影响，从而返回的值每次都是一致的，不会造成无用的额外 HTTP 缓存。
        # 你可以通过修改这个配置的值来覆盖默认的操作。但这是不被推荐的做法因为这个默认的行为可能会给你在性能的代价上带来改善。
        'JSONIFY_PRETTYPRINT_REGULAR': True,
        'JSONIFY_MIMETYPE': 'application/json',
        'TEMPLATES_AUTO_RELOAD': None,
    }