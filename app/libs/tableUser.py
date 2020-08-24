from app.libs import DB
from app.models.user import User
import datetime
from logger import log

def get_friend_list(func):
    '''
    返回用户seqid列表
    '''
    def wrapper(*args, **kwargs):
        friendsList = []
        rows, err = func(*args, **kwargs)
        if not err and rows:
            for row in rows:
                friendsList.append(row[0])
            return friendsList
        if not rows:
            return friendsList
        log.error(err)
        return None
    return wrapper

def get_user(func):
    '''
    返回单个用户对象
    '''
    def wrapper(*args, **kwargs):
        user = User()
        rows, err = func(*args, **kwargs)
        if not err and rows:
            user.seqid = rows[0][0]
            user.phoneNumber = rows[0][1]
            user.email = rows[0][2]
            user.password = rows[0][3]
            user.nickname = rows[0][4]
            user.sex = rows[0][5]
            user.registerTime = rows[0][6]
            user.token = rows[0][7]
            user.timenow = rows[0][8]
            return user
        return None
    return wrapper

class TableUser:

    @get_user
    def get_user_by(self, seqid = '', phoneNumber = '', email = '', token = '', nickname = ''):
        '''
        查询用户信息
        return: 用户对象
        '''
        if seqid:
            strSql = 'select * from [User] where seqid=?'
            return DB.ExecSqlQuery(strSql, seqid)
        elif phoneNumber:
            strSql = 'select * from [User] where phoneNumber=?'
            return DB.ExecSqlQuery(strSql, phoneNumber)
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
    
    def update_user(self, seqid, updateDict):
        '''
        更新用户数据
        seqid: 用户id
        update_dct: 更新字段字典
        return: 成功or失败
        '''
        _tempStr = ''
        for key, value in updateDict.items():
            _tempStr += f"{key}='{value}',"
        _tempStr = _tempStr[:-1]

        strSql = f"update [User] set {_tempStr} where seqid = {int(seqid)}"
        return DB.ExecSqlNoQuery(strSql)

    def insert_user(self, phoneNumber, email, password, nickname, sex):
        '''
        插入新用户
        phoneNumber: 电话
        email: 邮箱
        password: 密码
        nickname: 昵称
        return: 成功or失败
        '''
        strSql = 'insert into [User] (phoneNumber,email,password,nickname,sex,registerTime) values (?,?,?,?,?,?)'
        return DB.ExecSqlNoQuery(
            strSql,
            phoneNumber,
            email,
            password,
            nickname,
            sex,
            str(datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f'))[:-3]
        )

    @get_friend_list
    def get_friends(self, userid):
        '''
        获取所有好友
        userid: 用户seqid
        return 好友seqid列表
        '''
        strSql = f'select * from RelationUsers where userid in ({userid})'
        return DB.ExecSqlQuery(strSql)

    def get_friend(self, userid, friendid):
        '''
        查询好友
        userid: 用户seqid
        return true or false
        '''
        strSql = 'select * from RelationUsers where userid=? and friendid=?'
        rows, _ = DB.ExecSqlQuery(strSql, userid, friendid)
        if rows:
            return True
        else:
            return False

    def add_friend(self, userSeqid, friendSeqid):
        '''
        添加好友
        '''
        strSql = f'insert into RelationUsers (userid,friendid,isReceive) values ({userSeqid},{friendSeqid},1),({friendSeqid},{userSeqid},0)'
        return DB.ExecSqlNoQuery(strSql)

    def delete_friend(self, userSeqid, friendSeqid):
        '''
        删除好友
        '''
        strSql = 'delete RelationUsers where userid=? and friendid=?'
        return DB.ExecSqlNoQuery(strSql, userSeqid, friendSeqid)

    def answer_friend(self, userSeqid, friendSeqid, answer):
        '''
        回应好友请求
        '''
        if answer:
            strSql = 'update RelationUsers set isReceive=1 where userid=? and friendid=?'
            return DB.ExecSqlNoQuery(strSql, userSeqid, friendSeqid)
        else:
            return self.delete_friend(userSeqid, friendSeqid)
            
