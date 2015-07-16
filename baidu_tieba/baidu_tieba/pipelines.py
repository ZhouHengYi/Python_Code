# -*- coding: utf-8 -*-
# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline
import time
import MySQLdb
import MySQLdb.cursors
import socket
import select
import sys
import os
import errno
#连接数据库
class MySQLStorePipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host = '192.168.0.8',
            db = 'baidu_jpan',
            user = 'root',
            passwd = 'newegg@123',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True
        )
    #pipeline默认调用
    def process_item(self, item, spider):
        try:
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            return item
        except:
            print "mysql程序异常"

    #将每行写入数据库中
    def _conditional_insert(self, tx, item):
        if item.get('title'):
            for i in range(len(item['title'])):
                tx.execute('insert into jpanlist(title,link,furl,indate) values (%s, %s, %s, now())', (item['title'][i], item['link'][i], item['furl'][i]))

    #pipeline默认调用
    def process_item_item(self, item, spider):
        try:
            query = self.dbpool.runInteraction(self._conditional_insert_item, item)
            return item
        except:
            print "mysql程序异常"

    #将每行写入数据库中
    def _conditional_insert_item(self, tx, item):
        if item.get('title'):
            for i in range(len(item['title'])):
                tx.execute("insert into jpanitem(bid,userid,username,userhead,userhome,contentid,content,turl,furl,indate) values (%s, %s, '%s','%s', '%s', %s,'%s', '%s', '%s', now())", (item['title'][i], item['link'][i], item['furl'][i]))