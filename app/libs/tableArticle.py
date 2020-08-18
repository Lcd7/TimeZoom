from app.libs import DB
from app.models.article import Article
import datetime
from logger import log

def get_art(func):
    def wrapper(*args, **kwargs):
        rows, err = func(*args, **kwargs)
        if not err and rows:
            art_dict = {}
            art_dict['seqid'] = rows[0][0]
            art_dict['text'] = rows[0][1]
            art_dict['is_public'] = rows[0][2]
            art_dict['likes'] = rows[0][3]
            art_dict['relation_user_id'] = rows[0][4]
            return art_dict
        log.error(err)
        return None
    return wrapper

def get_art_list(func):
    def wrapper(*args, **kwargs):
        art_dict = {}
        rows, err = func(*args, **kwargs)
        if not err and rows:
            for row in rows:
                _tmp_dict = {}
                _tmp_dict['seqid'] = row[0]
                _tmp_dict['text'] = row[1]
                _tmp_dict['is_public'] = row[2]
                _tmp_dict['likes'] = row[3]
                _tmp_dict['relation_user_id'] = row[4]
                art_dict[row[0]] = _tmp_dict
            return art_dict
        log.error(err)
        return None
    return wrapper

def get_likes_list(func):
    def wrapper(*args, **kwargs):
        likes_list = []
        rows, err = func(*args, **kwargs)
        if not err and rows:
            for row in rows:
                likes_list.append(row[0])
            return likes_list
        return None
    return wrapper

class tableArticle:

    @classmethod
    def insert_art(cls, text, userid, is_public = False):
        '''
        新建动态
        text: 正文
        userid: 用户id
        is_public: 是否公开
        return seqid
        '''
        strSql = 'insert into Article (text,is_public,likes,relation_user_id) values (?,?,?,?)'
        ret, seqid = DB.ExecInsertGetLastId(strSql, text, is_public, 0, userid)
        if ret:
            return seqid
        else:
            return ret

    @get_art_list
    @classmethod
    def get_all_art(cls, artNum):
        '''
        获取所有用户所有动态
        artNum: 获取的动态数量
        return 多个动态字典
        '''
        strSql = f'select TOP ({artNum}) * from Article order by do_time DESC'
        return DB.ExecSqlQuery(strSql)

    @get_art
    @classmethod
    def get_user_one_art(cls, art_seqid):
        '''
        获取单个动态
        art_seqid: 动态id
        return 单个动态字典
        '''
        strSql = 'select * from Article where seqid=?'
        return DB.ExecSqlQuery(strSql, art_seqid)

    @get_art_list
    @classmethod
    def get_user_all_arts(cls, relation_user_id):
        '''
        搜索某个用户所有动态
        relation_user_id: 动态所属用户的id
        return 多个动态字典
        '''
        strSql = 'selcet * from Article where relation_user_id=? order by do_time DESC'
        return DB.ExecSqlQuery(strSql, relation_user_id)

    @classmethod
    def delete_art(cls, seqid):
        '''
        删除动态
        seqid: 动态id
        return: ture or false
        '''
        strSql = 'delete Article where seqid=?'
        return DB.ExecSqlNoQuery(strSql, seqid)

    @get_likes_list
    @classmethod
    def select_likes(cls, seqid = '', artid = ''):
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

    @classmethod
    def like_art(cls, seqid, artid):
        '''
        点赞动态
        seqid:  用户seqid
        srtid:  动态seqid
        '''
        strSql = 'insert into RelationLikes (userid,artid) values (?,?)'
        return DB.ExecSqlNoQuery(strSql, seqid, artid)