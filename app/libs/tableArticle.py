from app.libs import DB
from app.models.article import Article
import datetime
from functools import wraps
from logger import log

def get_art_dict(func):
    '''
    返回 动态的字典数据
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        rows, err = func(*args, **kwargs)
        if not err and rows:
            artDict = {}
            artDict['seqid'] = rows[0][0]
            artDict['text'] = rows[0][1]
            artDict['isPublic'] = rows[0][2]
            artDict['likes'] = rows[0][3]
            artDict['relationUserId'] = rows[0][4]
            artDict['comments'] = rows[0][5]
            artDict['doTime'] = rows[0][6]
            artDict['ban'] = rows[0][7]
            return artDict
        if not err and not rows:
            return '暂无动态'
        log.error(err)
        return None
    return wrapper

def get_arts_dict(func):
    '''
    返回 动态的字典数据
    '''
    @wraps(func)
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
                _tmpDict['comments'] = row[5]
                _tmpDict['doTime'] = row[6]
                _tmpDict['ban'] = row[7]
                artDict[row[0]] = _tmpDict
            return artDict
        if not err and not rows:
            return '暂无动态'
        log.error(err)
        return None
    return wrapper

def get_likes_list(func):
    '''
    返回 动态的seqid列表
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        likesList = []
        rows, err = func(*args, **kwargs)
        if not err and rows:
            for row in rows:
                likesList.append(row[0])
            return likesList
        if not err and not rows:
            return None
        log.error(err)
        return None
    return wrapper

strSqlItem = 'Article.seqid,Article.text,Article.isPublic,Article.likes,Article.relationUserId,Article.comments,Article.doTime,Img.headPic from Article full outer join Img on Article.seqid=Img.imgArticle'

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
        strSql = f"insert into Article (text,isPublic,relationUserId,doTime) values ('{text}',{isPublic},{userid},'{doTime}')"
        ret, seqid = DB.ExecInsertGetLastId(strSql)
        if ret:
            return seqid
        else:
            return ret

    @get_arts_dict
    def get_all_art(self, artNum):
        '''
        获取所有用户所有动态
        artNum: 获取的动态数量
        return 多个动态字典
        '''
        strSql = f'select TOP ({artNum}) {strSqlItem} where Article.isPublic=1 order by Article.doTime DESC'
        return DB.ExecSqlQuery(strSql)

    @get_art_dict
    def get_user_one_art(self, artSeqid, isPublic = 1):
        '''
        获取单个动态
        artSeqid: 动态id
        isPublic: 是否公开 0不公开, 1公开, 2所有
        return 单个动态字典
        '''
        if isPublic == 2:
            strSql = f'select {strSqlItem} where Article.seqid=?'
        elif isPublic == 1:
            strSql = f'select {strSqlItem} where Article.seqid=? and Article.isPublic=1'
        elif isPublic == 0:
            strSql = f'select {strSqlItem} where Article.seqid=? and Article.isPublic=0'

        return DB.ExecSqlQuery(strSql, artSeqid)

    @get_arts_dict
    def get_user_all_arts(self, relationUserId, isPublic = 1):
        '''
        搜索某个用户所有动态
        relationUserId: 动态所属用户的id
        isPublic: 是否公开 0不公开, 1公开, 2所有
        return 多个动态字典
        '''
        if isPublic == 2:
            strSql = f'select {strSqlItem} where relationUserId=? order by Article.doTime DESC'
        elif isPublic == 1:
            strSql = f'select {strSqlItem} where relationUserId=? and Article.isPublic=1 order by Article.doTime DESC'
        elif isPublic == 0:
            strSql = f'select {strSqlItem} where relationUserId=? and Article.isPublic=0 order by Article.doTime DESC'
        return DB.ExecSqlQuery(strSql, int(relationUserId))

    def update_article(self, artid, likes = None, isPublic = None, comments = None):
        '''
        更新动态数据
        设置公开状态、 更新点赞数和评论数。
        artid: 动态id
        isPublic: 动态状态 true or false
        likes: 点赞 1 or -1
        comments: 评论 1 or -1
        '''
        if isPublic:
            strSql = 'update Article set isPublic=? where seqid=?'
            return DB.ExecSqlNoQuery(strSql, isPublic, artid)

        elif likes:
            resDict = self.get_user_one_art(artid, 2)
            if isinstance(resDict, dict):
                likes = resDict.get('likes') + int(likes)
                strSql = 'update Article set likes=? where seqid=?'
                return DB.ExecSqlNoQuery(strSql, likes, artid)

        elif comments:
            resDict = self.get_user_one_art(artid, 2)
            if isinstance(resDict, dict):
                comments = resDict.get('comments') + int(comments)
                strSql = 'update Article set comments=? where seqid=?'
                return DB.ExecSqlNoQuery(strSql, comments, artid)

    def delete_art(self, seqid):
        '''
        删除动态
        seqid: 动态id
        return: ture or false
        '''
        strSql = 'delete Article where seqid=?'
        return DB.ExecSqlNoQuery(strSql, int(seqid))

    @get_likes_list
    def select_likes(self, seqid = None, artid = None):
        '''
        查询点赞记录
        seqid:  用户seqid
        srtid:  动态seqid
        return: id列表
        '''
        # 查询某个用户的某条动态点赞记录
        if seqid and artid:
            strSql = 'select seqid from RelationLikes where userid=? and artid=?'
            return DB.ExecSqlQuery(strSql, seqid, int(artid))

        # 查询某个用户所有点赞记录
        elif seqid and not artid:
            strSql = 'select artid from RelationLikes where userid=?'
            return DB.ExecSqlQuery(strSql, int(seqid))

        # 查询某个动态点赞的所有用户
        elif not seqid and artid:
            strSql = 'select userid from RelationLikes where artid=?'
            return DB.ExecSqlQuery(strSql, int(artid))
        else:
            pass

    def like_art(self, seqid, artid):
        '''
        点赞动态
        seqid:  用户seqid
        artid:  动态seqid
        '''
        strSql = 'insert into RelationLikes (userid,artid) values (?,?)'
        if DB.ExecSqlNoQuery(strSql, seqid, int(artid)):
            if not self.update_article(artid, likes = 1):
                return None
            else:
                return True
        return None

    def reset_like_art(self, seqid, artid):
        '''
        取消点赞
        seqid:  用户seqid
        artid:  动态seqid
        '''
        strSql = 'delete RelationLikes where userid=? and artid=?'
        if DB.ExecSqlNoQuery(strSql, seqid, int(artid)):
            if not self.update_article(artid, likes = -1):
                return None
            else:
                return True
        return None