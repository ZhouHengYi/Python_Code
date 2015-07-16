# -*- coding: utf-8 -*-  \
import logging
import logging.handlers  

class Log_Utility(object):
    def __init__(self,msg):
        LOG_FILE = 'tst.log'

        handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # 实例化handler
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

        formatter = logging.Formatter(fmt)   # 实例化formatter
        handler.setFormatter(formatter)      # 为handler添加formatter

        logger = logging.getLogger('tst')    # 获取名为tst的logger
        logger.addHandler(handler)           # 为logger添加handler
        logger.setLevel(logging.DEBUG)
        print str(msg).decode('utf8')
        logger.info(msg)