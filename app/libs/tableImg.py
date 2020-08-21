from app.libs import DB
from app.models.img import Img
from logger import log

def get_img(func):
    def wrapper(*args, **kwargs):
        img = Img()
        rows, err = func(*args, **kwargs)
        if not err and rows:
            img.seqid = rows[0][0]
            img.imgName = rows[0][1]
            img.headPic = rows[0][2]
            img.picValue = rows[0][3]
            img.imgType = rows[0][4]
            img.imgUser = rows[0][5]
            img.imgComment = rows[0][6]
            return img
        return None
    return wrapper

class TableImg:

    @get_img
    def get_img_by(self, imgName = '', headPic = '', picValue = '', imgType = '', imgUser = '', imgComment = ''):
        if imgName:
            strSql = 'select * from Img where imgName=?'
            return DB.ExecSqlQuery(strSql, imgName)
        elif headPic:
            strSql = 'select * from Img where headPic=?'
            return DB.ExecSqlQuery(strSql, headPic)
        elif picValue:
            strSql = 'select * from Img where picValue=?'
            return DB.ExecSqlQuery(strSql, picValue)
        elif imgType:
            strSql = 'select * from Img where imgType=?'
            return DB.ExecSqlQuery(strSql, imgType)
        elif imgUser:
            strSql = 'select * from Img where imgUser=?'
            return DB.ExecSqlQuery(strSql, imgUser)
        elif imgComment:
            strSql = 'select * from Img where imgComment=?'
            return DB.ExecSqlQuery(strSql, imgComment)
        else:
            pass

    def insert_img(self, imgName, headPic, imgUser, imgComment = 0, imgType = 1):
        '''
        imgName: 图片名
        headPic: 图片地址
        imgUser: 图片所属用户
        imgComment: 图片所属动态
        imgType: 1动态 2头像 0系统图片
        return True or False
        ''' 
        # 动态图片
        if imgType == 1:
            strSql = 'insert into Img (imgName,headPic,imgType,imgUser,imgComment) values (?,?,?,?,?)'
            return DB.ExecSqlNoQuery(strSql, imgName, headPic, imgType, imgUser, imgComment)
        # 头像图片
        elif imgType == 2:
            strSql = 'insert into Img (imgName,headPic,imgType,imgUser) values (?,?,?,?)'
            return DB.ExecSqlNoQuery(strSql, imgName, headPic, imgType, imgUser)