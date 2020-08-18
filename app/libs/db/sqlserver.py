# -*- coding: utf-8 -*-
import pyodbc
from logger import log
import threading
import sys
from app.config import DevelopmentConfig

class SqlServer:
    __conn = None
    __cursor = None
    __lock = threading.Lock()

    def __init__(self,connstring):
        try:
            self.__conn = pyodbc.connect(connstring)
            self.__cursor = self.__conn.cursor()
        except Exception as ex:
            log.error(ex)

    def ExecSqlQuery(self, strSql, *args):
        '''
        数据库查询
        strSql: 查询语句
        *args: 查询条件
        return: 查询结果列表, 异常
        '''
        rows = None
        err = None
        self.__lock.acquire()
        try:
            self.__cursor.execute(strSql, *args)
            rows = self.__cursor.fetchall()
        except Exception as e:
            log.error(e)
            err = e

        self.__lock.release()
        return rows, err

    def ExecSqlNoQuery(self, strSql, *args):
        '''
        数据库增删改操作
        strSql: 操作语句
        *args: 操作条件
        return: 成功or失败
        '''
        ret = False
        self.__lock.acquire()
        try:
            self.__cursor.execute(strSql, *args)
            self.__conn.commit()
            ret = True
        except Exception as e:
            log.error(e)

        self.__lock.release()
        return ret

    def ExecInsertGetLastId(self, strSql, *args):
        ret = False
        seqId = None
        self.__lock.acquire()
        try:
            self.__cursor.execute(strSql,*args)
            self.__conn.commit()
            self.__cursor.execute("select @@identity")
            row = self.__cursor.fetchone()
            if row:
                ret = True
                seqId = row[0]
        except Exception as ex:
            log.error('数据库执行插入异常{}'.format(ex))
        self.__lock.release()
        return ret, seqId

DB = SqlServer(DevelopmentConfig.DATABASE_URI)

if __name__ == "__main__":
    pass

