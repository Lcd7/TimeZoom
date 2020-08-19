from app.libs import DB
from app.models.tcomment import TComment
from logger import log
import datetime

def all_comments_body(func):
    def wrapper(*args):
        bodyDict = {}
        rows, err = func(*args)
        if not err and rows:
            for row in rows:
                _tmpDict = {}
                _tmpDict['seqid'] = row[0]
                _tmpDict['text'] = row[1]
                _tmpDict['isPublic'] = row[2]
                _tmpDict['relationArticlesId'] = row[3]
                bodyDict['row[0]'] = _tmpDict
            return bodyDict
        log.error(err)
        return None
    return wrapper

def comment_body(func):
    def wrapper(*args):
        bodyDict = {}
        rows, err = func(*args)
        if not err and rows:
            bodyDict['seqid'] = rows[0][0]
            bodyDict['text'] = rows[0][1]
            bodyDict['isPublic'] = rows[0][2]
            bodyDict['relationArticlesId'] = rows[0][3]
            return bodyDict
        log.error(err)
        return None
    return wrapper


class TableComment:

    @classmethod
    def add_comment(cls, text, isPublic, relationArtId):
        '''
        新增评论
        text: 评论正文
        isPublic: 是否公开
        relationArtId: 关联的动态id
        return true or false
        '''
        doTime = str(datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f'))[:-3]
        strSql = 'insert into T_Comment (text,isPublic,relationArticlesId,doTime) values (?,?,?,?)'
        return DB.ExecSqlNoQuery(strSql, text, isPublic, relationArtId, doTime)

    @classmethod
    def delete_comment(cls, seqid):
        '''
        删除评论
        seqid: 评论seqid
        return true or false
        '''
        strSql = 'delete T_Comment where seqid=?'
        return DB.ExecSqlNoQuery(strSql, seqid)

    @comment_body
    @classmethod
    def get_comment(cls, seqid):
        '''
        获取单个评论
        seqid: 评论seqid
        return: 评论数据 字典
        '''
        strSql = 'select * from T_Comment where seqid=?'
        return DB.ExecSqlQuery(strSql, seqid)

    @all_comments_body
    @classmethod
    def get_all_comments(cls, relationArtId):
        '''
        获取动态所有的评论
        relationArtId: 评论关联的动态seqid
        return: 所有评论数据 字典
        '''
        strSql = 'select * from T_Comment where relationArticlesId=? order by doTime DESC'
        return DB.ExecSqlQuery(strSql, relationArtId)