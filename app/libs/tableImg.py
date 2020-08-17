from app.libs import DB
from app.models.img import Imgs
import datetime
from logger import log

def get_img(func):
    def wrapper(*args, **kwargs):
        img = Imgs()
        rows, err = func(*args, **kwargs)
        if not err and rows:
            img.seqid = rows[0][0]
            img.img_name = rows[0][1]
            img.head_pic = rows[0][2]
            img.pic_value = rows[0][3]
            img.img_type = rows[0][4]
            img.img_user = rows[0][5]
            img.img_comment = rows[0][6]
            return img
        return None
    return wrapper

class tableImg:

    @get_img
    @classmethod
    def get_img_by(cls, img_name = '', head_pic = '', pic_value = '', img_type = '', img_user = '', img_comment = ''):
        if img_name:
            strSql = 'select * from Imgs where img_name=?'
            return DB.ExecSqlQuery(strSql, img_name)
        elif head_pic:
            strSql = 'select * from Imgs where head_pic=?'
            return DB.ExecSqlQuery(strSql, head_pic)
        elif pic_value:
            strSql = 'select * from Imgs where pic_value=?'
            return DB.ExecSqlQuery(strSql, pic_value)
        elif img_type:
            strSql = 'select * from Imgs where img_type=?'
            return DB.ExecSqlQuery(strSql, img_type)
        elif img_user:
            strSql = 'select * from Imgs where img_user=?'
            return DB.ExecSqlQuery(strSql, img_user)
        elif img_comment:
            strSql = 'select * from Imgs where img_comment=?'
            return DB.ExecSqlQuery(strSql, img_comment)
        else:
            pass

    @classmethod
    def insert_img(cls, img_name, head_pic, img_user, img_comment):
        '''
        img_name: 图片名
        head_pic: 图片地址
        img_user: 图片所属用户
        img_comment: 图片所属动态
        '''
        img_type = 1
