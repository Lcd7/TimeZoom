from app.libs import DB
from app.models.article import Article
import datetime
from logger import log

def get_art(func):
    def wrapper(*args, **kwargs):
        rows, err = func(*args, **kwargs)
        if not err and rows:
            artDict = {}
            artDict['seqid'] = rows[0][0]
            artDict['text'] = rows[0][1]
            artDict['isPublic'] = rows[0][2]
            artDict['likes'] = rows[0][3]
            artDict['relationUserId'] = rows[0][4]
            artDict['commentNum'] = len(rows)
            return artDict
        log.error(err)
        return None
    return wrapper

def get_art_dict(func):
    def wrapper(*args, **kwargs):
        artDict = {}
        rows, err = func(*args, **kwargs)
        if not err and rows:
            for row in rows:
                _tmpDict = {}
                _tmpDict['seqid'] = row[0]
                _tmpDict['text'] = row[1]
                _tmpDict['isPublic'] = row[2]
                _tmpDict['likes'] = row[3]
                _tmpDict['relationUserId'] = row[4]
                artDict[row[0]] = _tmpDict
            return artDict
        log.error(err)
        return None
    return wrapper

def get_likes_list(func):
    def wrapper(*args, **kwargs):
        likesList = []
        rows, err = func(*args, **kwargs)
        if not err and rows:
            for row in rows:
                likesList.append(row[0])
            return likesList
        return None
    return wrapper

class TableArticle:
    
    def insert_art(self, text, userid, isPublic = False):
        '''
        新建动态
        text: 正文
        userid: 用户id
        isPublic: 是否公开
        return seqid
        '''
        doTime = str(datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f'))[:-3]
        strSql = 'insert into Article (text,isPublic,likes,relationUserId,doTime) values (?,?,?,?,?)'
        ret, seqid = DB.ExecInsertGetLastId(strSql, text, isPublic, 0, userid, doTime)
        if ret:
            return seqid
        else:
            return ret

    @get_art_dict
    def get_all_art(self, artNum):
        '''
        获取所有用户所有动态
        artNum: 获取的动态数量
        return 多个动态字典
        '''
        strSql = f'select TOP ({artNum}) * from Article order by doTime DESC'
        return DB.ExecSqlQuery(strSql)

    @get_art
    def get_user_one_art(self, artSeqid):
        '''
        获取单个动态
        artSeqid: 动态id
        return 单个动态字典
        '''
        strSql = 'select * from Article where seqid=?'
        # strSql = 'select * from Article full outer join T_Comment on Article.seqid=T_Comment.relationArticlesId where Article.seqid=?'
        return DB.ExecSqlQuery(strSql, artSeqid)

    @get_art_dict
    def get_user_all_arts(self, relationUserId):
        '''
        搜索某个用户所有动态
        relationUserId: 动态所属用户的id
        return 多个动态字典
        '''
        strSql = 'selcet * from Article where relationUserId=? order by doTime DESC'
        return DB.ExecSqlQuery(strSql, relationUserId)

    def set_public_art(self, artid, artStatus):
        '''
        设置动态是否公开
        artid: 动态id
        artStatus: 动态状态
        '''
        strSql = 'update Article set isPublic=? where seqid=?'
        return DB.ExecSqlNoQuery(strSql, artStatus, artid)

    def delete_art(self, seqid):
        '''
        删除动态
        seqid: 动态id
        return: ture or false
        '''
        strSql = 'delete Article where seqid=?'
        return DB.ExecSqlNoQuery(strSql, seqid)

    @get_likes_list
    def select_likes(self, seqid = '', artid = ''):
        '''
        查询点赞记录
        seqid:  用户seqid
        srtid:  动态seqid
        return: id列表
        '''
        # 查询某个用户的某条动态点赞记录
        if seqid and artid:
            strSql = 'select seqid from RelationLikes where userid=? and artid=?'
            return DB.ExecSqlQuery(strSql, seqid, artid)

        # 查询某个用户所有点赞记录
        elif seqid and not artid:
            strSql = 'select artid from RelationLikes where userid=?'
            return DB.ExecSqlQuery(strSql, seqid)

        # 查询某个动态点赞的所有用户
        elif not seqid and artid:
            strSql = 'select userid from RelationLikes where artid=?'
            return DB.ExecSqlQuery(strSql, artid)
        else:
            pass

    def like_art(self, seqid, artid):
        '''
        点赞动态
        seqid:  用户seqid
        artid:  动态seqid
        '''
        strSql1 = 'insert into RelationLikes (userid,artid) values (?,?)'
        if DB.ExecSqlNoQuery(strSql1, seqid, artid):
            strSql2 = 'select likes from Article where seqid=?'
            rows, err = DB.ExecSqlQuery(strSql2, artid)
            if not err:
                likeNum = int(rows[0][0]) + 1
                strSql3 = 'update Article set likes=? where seqid=?'
                return DB.ExecSqlNoQuery(strSql3, likeNum, artid)
            return None
        return None

    def reset_like_art(self, seqid, artid):
        '''
        取消点赞
        seqid:  用户seqid
        artid:  动态seqid
        '''
        strSql = 'delete RelationLikes where seqid=? and artid=?'
        if DB.ExecSqlNoQuery(strSql, seqid, artid):
            strSql2 = 'select likes from Article where seqid=?'
            rows, err = DB.ExecSqlQuery(strSql2, artid)
            if not err:
                likeNum = int(rows[0][0]) - 1
                strSql3 = 'update Article set likes=? where seqid=?'
                return DB.ExecSqlNoQuery(strSql3, likeNum, artid)
            return None
        return None