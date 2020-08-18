from app.libs import DB
from app.models.user import User
import datetime
from logger import log

def get_friend_list(func):
    def wrapper(*args, **kwargs):
        friendsList = []
        rows, err = func(*args, **kwargs)
        if not err and rows:
            for row in rows:
                friendsList.append(row[0])
            return friendsList
        log.error(err)
        return None
    return wrapper

def get_user(func):
    def wrapper(*args, **kwargs):
        user = User()
        rows, err = func(*args, **kwargs)
        if not err and rows:
            user.seqid = rows[0][0]
            user.phone_number = rows[0][1]
            user.email = rows[0][2]
            user.password = rows[0][3]
            user.nickname = rows[0][4]
            user.sex = rows[0][5]
            user.relationships = rows[0][6]
            user.register_time = rows[0][7]
            user.token = rows[0][8]
            return user
        return None
    return wrapper

class tableUser:

    @get_user
    @classmethod
    def get_user_by(cls, seqid = '', phone_number = '', email = '', token = '', nickname = ''):
        '''
        查询用户信息
        return: 用户对象
        '''
        if seqid:
            strSql = 'select * from [User] where seqid=?'
            return DB.ExecSqlQuery(strSql, seqid)
        elif phone_number:
            strSql = 'select * from [User] where phone_number=?'
            return DB.ExecSqlQuery(strSql, phone_number)
        elif email:
            strSql = 'select * from [User] where email=?'
            return DB.ExecSqlQuery(strSql, email)
        elif token:
            strSql = 'select * from [User] where token=?'
            return DB.ExecSqlQuery(strSql, token)
        elif nickname:
            strSql = 'select * from [User] where nickname=?'
            return DB.ExecSqlQuery(strSql, nickname)
        else:
            pass
    
    @classmethod
    def update_user(cls, seqid, updateDict):
        '''
        更新用户数据
        seqid: 用户id
        update_dct: 更新字段字典
        return: 成功or失败
        '''
        _tempStr = ''
        for key, value in updateDict.items():
            _tempStr += f'{key}="{value}"'

        strSql = f'update [User] set {_tempStr} where seqid = {int(_tempStr)}'
        return DB.ExecSqlNoQuery(strSql)

    @classmethod
    def insert_user(cls, phone_number, email, password, nickname):
        '''
        插入新用户
        phone_number: 电话
        email: 邮箱
        password: 密码
        nickname: 昵称
        return: 成功or失败
        '''
        strSql = 'insert into [User] (phone_number,email,password,nickname,register_time) values (?,?,?,?,?)'
        return DB.ExecSqlNoQuery(
            strSql,
            phone_number,
            email,
            password,
            nickname,
            str(datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f'))[:-3]
        )

    @get_friend_list
    @classmethod
    def get_friends(cls, seqid):
        '''
        获取所有好友
        seqid: 用户seqid
        return 好友字典
        '''
        strSql = f'select * from [RelationUsers] where userid in ({seqid})'
        return DB.ExecSqlQuery(strSql)

    @classmethod
    def add_friend(cls, userSeqid, friendSeqid):
        '''
        添加好友
        '''
        strSql = 'insert into RelationUsers (userid,friendid) values (?,?)'
        return DB.ExecSqlNoQuery(strSql, userSeqid, friendSeqid)

if __name__ == "__main__":
    pass