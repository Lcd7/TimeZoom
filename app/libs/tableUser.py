from app.libs import DB
from app.models import User
import datetime
from logger import log

def get_user(func):
    def wrapper(*arg, **kwargs):
        user = User()
        rows, err = func(*arg, **kwargs)
        if not err and rows:
            user.seqid = rows[0][0]
            user.phone_number = rows[0][1]
            user.password = rows[0][2]
            user.nickname = rows[0][3]
            user.token = rows[0][4]
            return user
        return None
    return wrapper

@get_user
def get_user_by(phone_number = '', email = '', token = ''):
    '''
    查询用户信息
    '''
    if phone_number:
        strSql = 'select * from [User] where phone_number=?'
        return DB.ExecSqlQuery(strSql, phone_number)
    elif email:
        strSql = 'select * from [User] where email=?'
        return DB.ExecSqlQuery(strSql, email)
    elif token:
        strSql = 'select * from [User] where token=?'
        return DB.ExecSqlQuery(strSql, token)
    else:
        pass

def update_user(update_dct):
    '''
    更新用户数据
    *kwargs: 更新字段字典
    return: 成功or失败
    '''
    _tempStr = ''
    for key, value in update_dct.items():
        _tempStr += f'{key}="{value}"'

    strSql = f'update [User] where {_tempStr}'
    return DB.ExecSqlNoQuery(strSql)

def insert_user(phone_number, email, password, nickname):
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


if __name__ == "__main__":
    pass