import urllib2,urllib,json,re
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import string
sys.stdout=open('output.txt','w')
from scrapy import log

from baidu_tieba.items import JpanItem_Items
from baidu_tieba.spiders.config import Jpan_config


from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from baidu_tieba.mysql import Connection
from baidu_tieba.DQueue import RedisQueue
from pyquery import PyQuery as pq

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors


import time
import PyV8

def db():
    return Connection(host="192.168.0.8", database="BaiDu_Jpan", user="root", password="newegg@123")


class JpanItemSpider(CrawlSpider):
    name = "baidu.jpan.item"
    allowed_domains = ["tieba.baidu.com"]
    start_urls = ["http://tieba.baidu.com/f?kw=%E6%97%A5%E6%9C%AC%E7%95%99%E5%AD%A6&ie=utf-8&pn=0",]
    headers = Jpan_config().get_Request_Headers()

    def parse(self, response):
        q = RedisQueue('test')
        self.bid = q.get()
        purl = 'http://tieba.baidu.com/p/'+self.bid
        #purl = 'http://tieba.baidu.com/p/3598243313'
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
                values.append((ins["bid"],ins["userid"],ins["username"],ins["userhead"],ins["userhome"],ins["contentid"],ins["content"],ins["turl"],ins["furl"]))
                #inserts += "("+ins["bid"]+","+ins["userid"]+",'"+ins["username"]+"','"+ins["userhead"]+"','"+ins["userhome"]+"','"+ins["contentid"]+"','"+ins["content"]+"','"+ins["turl"]+"','"+ins["furl"]+"'),"
            #inserts = [inserts];
            print values
    
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
                sqli = """insert into jpanitem(bid,userid,username,userhead,userhome,contentid,content,turl,furl,indate) values ('%s', '%s', '%s','%s', '%s', '%s','%s', '%s', '%s', now())"""
                #cur.executemany(sqli,[(3598243313,161821646,'12344','http://tb.himg.baidu.com/sys/portrait/item/ce33e68e92e9aaa8e4ba8ce58fb7a509','/home/main?un=%E6%8E%92%E9%AA%A8%E4%BA%8C%E5%8F%B7&ie=utf-8&fr=pb&ie=utf-8',64703958769,'123','http://tieba.baidu.com/p/3598243313','tieba.baidu.com/f?kw=%E6%97%A5%E6%9C%AC%E7%95%99%E5%AD%A6&ie=utf-8'),])
                #cur.executemany(sqli,values)
                cur.executemany("""insert into jpanitem(bid,userid,username,userhead,userhome,contentid,content,turl,furl,indate) values (%s, %s, %s,%s, %s, %s,%s, %s, %s, now()) """, values)
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
                return request
            else:
                return self.nextItem()
    
    def nextItem(self):
        q = RedisQueue('test')
        self.bid = q.get()
        purl = 'http://tieba.baidu.com/p/'+self.bid
        request = scrapy.Request(purl, callback=self.tlist)
        return request