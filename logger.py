# -*- coding: utf-8 -*-  
import logging, os
import coloredlogs
from logging.handlers import TimedRotatingFileHandler


coloredlogs.DEFAULT_FIELD_STYLES = {'asctime': {'color': 'green'}, 
                                    'filename': {'color': 'magenta', 'bold': True},
                                    'levelname': {'color': 'yellow', 'bold': True}, 
                                    'request_id': {'color': 'green', 'bold': True},
                                    'name': {'color': 'blue'}, 
                                    'programname': {'color': 'cyan'},
                                    'threadName': {'color': 'yellow'},
                                    'lineno': {'color': 'cyan'}}


coloredlogs.DEFAULT_LEVEL_STYLES = {'info': {'color': 'cyan', 'bold': True}, 
                                    'notice': {'color': 'magenta', 'bold': True},
                                    'critical': {'color': 'red', 'bold': True}, 
                                    'error': {'color': 'red', 'bold': True},
                                    'debug': {'color': 'blue', 'bold': True}, 
                                    'warning': {'color': 'yellow', 'bold': True}}


def getlogger():

    # 使用一个名字为mylogger的logger
    logger = logging.getLogger()
    # 设置logger的level为DEBUG
    logger.setLevel(logging.INFO)
    # 创建一个输出日志到控制台的StreamHandler

    streamHandler = logging.StreamHandler()

    fmt = '[%(asctime)s]:[%(filename)s]:[line:%(lineno)d]:%(levelname)s: %(message)s'
    formatter = logging.Formatter(fmt)
    streamHandler.setFormatter(formatter)


    #把log输出到当前目录下交usk.log的文件
    filename = '%s/app.log' % ('./log')

    fileHandler = TimedRotatingFileHandler(filename, when = 'D', interval = 1, backupCount = 7, encoding = 'utf-8')
    fileHandler.setLevel(logging.INFO)
    fileHandler.setFormatter(streamHandler)

    logger.addHandler(streamHandler)#把日志打印到控制台
    logger.addHandler(fileHandler) #把日志打印到文件

    coloredlogs.install(fmt = fmt, level = logging.INFO, logger = logger)

    return logger

log = getlogger()

if __name__ == "__main__":
    pass

