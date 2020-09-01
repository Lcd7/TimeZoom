from app.libs import DB
from app.models.tcomment import TComment
from logger import log
import datetime
from functools import wraps

def get_letter_dict(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        letterDict = {}
        rows, err = func(*args, **kwargs)
        if not err and rows:
            for row in rows:
                _tmpDict = {}
                _tmpDict['seqid'] = row[0]
                _tmpDict['userid'] = row[1]
                _tmpDict['frienid'] = row[2]
                _tmpDict['senderid'] = row[3]
                _tmpDict['receiverid'] = row[4]
                _tmpDict['msgType'] = row[5]
                _tmpDict['text'] = row[6]
                _tmpDict['sendTime'] = row[7]
                _tmpDict['readTime'] = row[8]
                _tmpDict['status'] = row[9]
                letterDict[row[0]] = _tmpDict
            return letterDict
        log.error(err)
        return None
    return wrapper

class TableLetter():
    @get_letter_dict
    def get_letter_by(self, userid = None, friendid = None, status = None):
        '''
        获取聊天记录
        return 消息字典
        '''
        # 获取未读信息
        if status == 0 and friendid:
            strSql = f"select * from Letter where status={status} and userid={userid} and friendid={friendid} order by seqid"
            return DB.ExecSqlQuery(strSql)
        
        # 获取聊天信息
        if userid and friendid:
            strSql = f"select * from Letter where userid={userid} and friendid={friendid} order by seqid"
            return DB.ExecSqlQuery(strSql)

    def delete_letter(self, seqid = None, userid = None, friendid = None):
        '''
        删除聊天记录
        return True or false
        '''
        # 删除用户聊天记录
        if userid and friendid :
            strSql = f"delete Letter where userid={userid} and friendid={friendid}"
            return DB.ExecSqlNoQuery(strSql)

        # 删除一条聊天记录
        if seqid:
            strSql = f"delete Letter where seqid={seqid}"
            return DB.ExecSqlNoQuery(strSql)

    def withdrawn_letter(self, senderid, receiverid, sendTime):
        '''
        撤回聊天记录
        return True or false
        '''
        if senderid and receiverid and sendTime:
            strSql = f"delete Letter where senderid={senderid} and receiverid={receiverid} and sendTime='{sendTime}'"
            return DB.ExecSqlNoQuery(strSql)

    def save_letter(self, userid, friendid, text, status):
        '''
        保存聊天记录
        return True or false
        '''
        msgType = 1
        sendTime = str(datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f'))[:-3]
        strSql = "insert into Letter (userid,friendid,senderid,receiverid,msgType,text,sendTime,status) values ()"
        _res1 = DB.ExecSqlNoQuery(strSql, userid, friendid, userid, friendid, msgType, text, sendTime, 1)
        _res2 = DB.ExecSqlNoQuery(strSql, userid, friendid, friendid, userid, msgType, text, sendTime, status)
        if _res1 and _res1:
            return True
        else:
            return False

    def set_read(self, seqid):
        '''
        设置已读
        seqid: 信息seqid
        return True or false
        '''
        strSql = f"update Letter set status=1 where seqid={seqid}"
        return DB.ExecSqlNoQuery(strSql)
