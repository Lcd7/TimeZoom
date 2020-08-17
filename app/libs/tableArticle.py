from app.libs import DB
from app.models.article import Article
import datetime

def get_art(func):
    def wrapper(*args, **kwargs):
        art = Article()
        rows, err = func(*args, **kwargs)
        if not err and rows:
            art.seqid = rows[0][0]
            art.text = rows[0][1]
            art.is_public = rows[0][2]
            art.likes = rows[0][3]
            art.relation_user_id = rows[0][4]
            return art
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
        return None
    return wrapper

class tableArticle:

    @classmethod
    def insert_art(cls, text, userid, is_public = False):
        '''
        新建动态
        return seqid
        '''
        strSql = 'insert into Article (text,is_public,likes,relation_user_id) values (?,?,?,?)'
        ret, seqid = DB.ExecInsertGetLastId(strSql, text, is_public, 0, userid)
        if ret:
            return seqid

    @get_art_list
    @classmethod
    def get_all_art(cls, art_num):
        '''
        获取所有动态
        return 动态字典
        '''
        strSql = f'select TOP ({art_num}) * from Article order by do_time DESC'
        return DB.ExecSqlQuery(strSql)

    @get_art_list
    @classmethod
    def search_art(cls, relation_user_id):
        '''
        搜索动态
        return 动态字典
        '''
        strSql = 'selcet * from Article where relation_user_id=? order by do_time DESC'
        return DB.ExecSqlQuery(strSql, relation_user_id)

    @classmethod
    def delete_art(cls, seqid):
        '''
        删除动态
        '''
        strSql = f'delete Article where seqid = {seqid}'
        return DB.ExecSqlNoQuery(strSql)