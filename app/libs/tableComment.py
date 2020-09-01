from app.libs import DB
from app.models.tcomment import TComment
from logger import log
import datetime

def all_comments_body(func):
    '''
    返回多个评论的字典数据
    '''
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
                _tmpDict['relationComment'] = row[4]
                _tmpDict['doTime'] = row[5]
                bodyDict[row[0]] = _tmpDict
            return bodyDict
        log.error(err)
        return None
    return wrapper

def comment_body(func):
    '''
    返回单个评论的字典数据
    '''
    def wrapper(*args):
        bodyDict = {}
        rows, err = func(*args)
        if not err and rows:
            bodyDict['seqid'] = rows[0][0]
            bodyDict['text'] = rows[0][1]
            bodyDict['isPublic'] = rows[0][2]
            bodyDict['relationArticlesId'] = rows[0][3]
            bodyDict['relationComment'] = rows[0][4]
            bodyDict['doTime'] = rows[0][5]
            return bodyDict
        log.error(err)
        return None
    return wrapper


class TableComment:

    def add_comment(self, text, isPublic, relationArtId, commentSeqid = None):
        '''
        新增评论
        text: 评论正文
        isPublic: 是否公开
        relationArtId: 关联的动态id
        commentSeqid: 回复评论的id
        return true or false
        '''
        doTime = str(datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f'))[:-3]
        if commentSeqid:
            strSql = 'insert into T_Comment (text,isPublic,relationArticlesId,relationComment,doTime) values (?,?,?,?,?)'
            return DB.ExecSqlNoQuery(strSql, text, isPublic, relationArtId, commentSeqid, doTime)
        else:
            strSql = 'insert into T_Comment (text,isPublic,relationArticlesId,doTime) values (?,?,?,?)'
            return DB.ExecSqlNoQuery(strSql, text, isPublic, relationArtId, doTime)

    def delete_comment(self, seqid):
        '''
        删除评论
        seqid: 评论seqid
        return true or false
        '''
        strSql = 'delete T_Comment where seqid=?'
        return DB.ExecSqlNoQuery(strSql, seqid)

    @comment_body
    def get_comment(self, seqid):
        '''
        获取单个评论
        seqid: 评论seqid
        return: 评论数据 字典
        '''
        strSql = 'select * from T_Comment where seqid=?'
        return DB.ExecSqlQuery(strSql, seqid)

    @all_comments_body
    def get_all_comments(self, relationArtId):
        '''
        获取动态所有的评论
        relationArtId: 评论关联的动态seqid
        return: 所有评论数据 字典
        '''
        strSql = 'select * from T_Comment where relationArticlesId=? order by doTime DESC'
        return DB.ExecSqlQuery(strSql, relationArtId)