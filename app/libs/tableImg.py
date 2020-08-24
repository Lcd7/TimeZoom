from app.libs import DB
from app.models.img import Img
from logger import log

def get_avatar_img(func):
    '''
    返回图片对象
    '''
    def wrapper(*args, **kwargs):
        img = Img()
        rows, err = func(*args, **kwargs)
        if not err:
            if rows:
                img.seqid = rows[-1][0]
                img.imgName = rows[-1][1]
                img.headPic = rows[-1][2]
                img.picValue = rows[-1][3]
                img.imgType = rows[-1][4]
                img.imgUser = rows[-1][5]
                img.imgComment = rows[-1][6]
                return img
            else:
                return None
        else:
            log.error(err)
        return None
    return wrapper

def get_all_img(func):
    def wrapper(*args, **kwargs):
        imgDict = {}
        rows, err = func(*args, **kwargs)
        if not err and rows:
            for row in rows:
                _tmpDict = {}
                _tmpDict['seqid'] = row[0]
                _tmpDict['imgName'] = row[1]
                _tmpDict['headPic'] = row[2]
                _tmpDict['picValue'] = row[3]
                _tmpDict['imgType'] = row[4]
                _tmpDict['imgUser'] = row[5]
                _tmpDict['imgComment'] = row[6]
                imgDict[row[0]] = _tmpDict
            return imgDict
        else:
            log.error(err)
        return None
    return wrapper


class TableImg:

    @get_all_img
    def get_img_by(self, imgName = '', headPic = '', picValue = '', imgType = '', imgUser = '', imgComment = ''):
        '''
        获取多个图片
        返回 字典数据
        '''
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
            strSql = 'select * from Img where imgUser=? and imgType=1'
            return DB.ExecSqlQuery(strSql, imgUser)
        elif imgComment:
            strSql = 'select * from Img where imgComment=?'
            return DB.ExecSqlQuery(strSql, imgComment)
        else:
            pass

    @get_avatar_img
    def get_avatar(self, userid):
        '''
        获取头像
        userid: 用户id
        return 图片对象 or false
        '''
        strSql = 'select * from Img where imgType=2 and imgUser=? order by seqid'
        return DB.ExecSqlQuery(strSql, userid)
    
    def insert_img(self, imgName, headPic, imgUser, imgComment = 0, imgType = 1):
        '''
        上传图片
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
        
    def delete_img(self, imgUser, imgComment = 0, imgType = 1):
        '''
        删除图片
        imgName: 图片名
        headPic: 图片地址
        imgUser: 图片所属用户
        imgComment: 图片所属动态
        imgType: 1动态 2头像 0系统图片
        return True or False
        ''' 
        # 动态图片
        if imgType == 1:
            strSql = 'delete Img where imgComment=?'
            return DB.ExecSqlNoQuery(strSql, imgComment)
        # 头像图片
        elif imgType == 2:
            strSql = 'delete Img where imgUser=? and imgType=?'
            return DB.ExecSqlNoQuery(strSql, imgUser, imgType)