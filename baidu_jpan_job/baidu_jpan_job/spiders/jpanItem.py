import scrapy
import urllib2,urllib,json,re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import string
sys.stdout=open('output2.txt','w')
from scrapy import log


from baidu_jpan_job.items import JpanItem_Items
from baidu_jpan_job.items import JpanList_Items
from baidu_jpan_job.spiders.config import Jpan_config


from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from baidu_jpan_job.mysql import Connection
from baidu_jpan_job.DQueue import RedisQueue
from pyquery import PyQuery as pq

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors


import time
import PyV8

def db():
    return Connection(host="192.168.0.8", database="BaiDu_Jpan", user="root", password="newegg@123")


class JpanItemSpider(object):
    name = "baidu.jpan.item"
    headers = Jpan_config().get_Request_Headers()

    def request(self,bid):
        self.bid = bid
        purl = 'http://tieba.baidu.com/p/'+bid
        request = scrapy.Request(purl,
                             callback=self.tlist)
        #return items
        return request

    def tlist(self,response):
        bid = self.bid
        items = []
        p = pq(response.body)
        #print response.body
        sites_even = p("div.l_post")
        h = pq(response.body)
        
        furl = h("[furl*='tieba']").attr("furl")
        bid = h("[rel*='canonical']").attr("href")
        
        if(bid == None):
            return self.nextItem()
        else:
            bid = bid.replace("http://tieba.baidu.com/p/",'')
            for site in sites_even:
                item = JpanItem_Items()
                item["bid"] = bid
                item["userid"] = pq(site).find(".d_name").attr("data-field")
                item["userid"] = item["userid"].replace("{\"user_id\":",'').replace("}",'')
                item["userhead"] = pq(site).find(".p_author_face img").attr("src")
                item["username"] = pq(site).find(".p_author_face img").attr("username")
                item["userhome"] = pq(site).find(".p_author_face").attr("href")
                item["contentid"] = pq(site).find("[id*='post_content_']").attr("id")
                item["contentid"] = item["contentid"].replace('post_content_','')
                item["content"] = pq(site).find("[id*='post_content_']").html()
                item["turl"] = response.url
                item["furl"] = furl
                items.append(item)
                #item["publisherDate"] = pq(site).find(".p_tail span").eq(1).html()
                #print item["publisherDate"]
    
            values = []
            for ins in items:
                #values.append((ins["bid"],ins["userid"],ins["username"],ins["userhead"],ins["userhome"],ins["contentid"],ins["content"],ins["turl"],ins["furl"]))
                #inserts += "("+ins["bid"]+","+ins["userid"]+",'"+ins["username"]+"','"+ins["userhead"]+"','"+ins["userhome"]+"','"+ins["contentid"]+"','"+ins["content"]+"','"+ins["turl"]+"','"+ins["furl"]+"'),"
                #inserts = [inserts];
                #print values
                try:
                    conn  = MySQLdb.connect(
                        host = '192.168.0.8',
                        db = 'baidu_jpan',
                        user = 'root',
                        passwd = 'newegg@123',
                        cursorclass = MySQLdb.cursors.DictCursor,
                        charset = 'utf8',
                        use_unicode = True,
                    )
                    cur = conn.cursor()
                    #sqli = """insert into jpanitem(bid,userid,username,userhead,userhome,contentid,content,turl,furl,indate) values ('%s', '%s', '%s','%s', '%s', '%s','%s', '%s', '%s', now())"""
                    

                    #cur.executemany("""insert into jpanitem(bid,userid,username,userhead,userhome,contentid,content,turl,furl,indate) values (%s, %s, %s,%s, %s, %s,%s, %s, %s, now()) """, values)
                    sql = "SELECT * FROM jpanitem WHERE contentid = " + ins['contentid']
                    cur.execute(sql)
                    rows = cur.fetchall()
                    log.msg(sql)
                    log.msg(rows)
                    if rows ==  None:
                        cur.execute('insert into jpanitem(bid,userid,username,userhead,userhome,contentid,content,turl,furl,indate) values (%s, %s, %s,%s, %s, %s,%s, %s, %s, now())', (ins["bid"],ins["userid"],ins["username"],ins["userhead"],ins["userhome"],ins["contentid"],ins["content"],ins["turl"],ins["furl"]))
                        log.msg('New Insert contentid:' + item['contentid'])
                    else:
                        log.msg('contentid:' + ins['contentid'] + ' is exists')
                    cur.close()
                    conn.commit()
                    conn.close()
                except Exception, e:
                    #print Exception,":",e
                    errorMsg = Exception,":",e
                    log.msg(errorMsg,level=log.DEBUG)

                next = p('.pb_list_pager a').filter(lambda i: pq(this).text() == u'\u4e0b\u4e00\u9875').attr('href')
                if next <> None:
                    request = scrapy.Request('http://tieba.baidu.com' + next,
                                     callback=self.tlist)            
                    #return request
                #else:
                    #return