from app.libs import DB
from app.models.admin import Admin
from logger import log
import datetime
from functools import wraps

def admindata(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        bodyDict = {}
        rows, err = func(*args, **kwargs)
        if not err and rows:
            bodyDict['seqid'] = rows[0][0]
            bodyDict['userName'] = rows[0][1]
            bodyDict['password'] = rows[0][2]
            bodyDict['superadmin'] = rows[0][3]
            bodyDict['ban'] = rows[0][5]
            return bodyDict
        if err:
            log.error(err)
            return None
        else:
            return None
    return wrapper

class TableAdmin:
    
    def get_admin(self, seqid = None, userName = None):
        if seqid:
            strSql = f'select * from T_admin where seqid={seqid}'
        elif userName:
            strSql = f'select * from T_admin where userName={userName}'
        return DB.ExecSqlQuery(strSql)

    def update_token(self, seqid, token):
        strSql = f'update T_admin set token={token} where seqid ={seqid}'
        return DB.ExecSqlNoQuery(strSql)

    def add_admin(self, userName = None, password = None, superadmin = None):
        strSql = 'insert into T_admin (userName,password,superadmin) values(?,?,?)'
        return DB.ExecSqlNoQuery(strSql, userName, password, superadmin)

    def change_passw(self, seqid, newpassw):
        strSql = f'update T_admin set password={newpassw} where seqid={seqid}'
        return DB.ExecSqlNoQuery(strSql)

    def ban_admin(self, seqid, ban = 1):
        strSql = f'update T_admin set ban={ban} where seqid={seqid}'
        return DB.ExecSqlNoQuery(strSql)

    def ban_user(self, seqid, ban):
        strSql = f'update [User] set ban={ban} where seqid={seqid}'
        return DB.ExecSqlNoQuery(strSql)

    def ban_art(self, seqid, ban):
        strSql = f'update Articles set ban={ban} where seqid={seqid}'
        return DB.ExecSqlNoQuery(strSql)