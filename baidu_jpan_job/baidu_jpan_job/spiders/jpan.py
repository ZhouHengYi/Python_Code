import urllib2,urllib,json,re
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import string
sys.stdout=open('output.txt','w')
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

class JpanSpider(CrawlSpider):

    name = "baidu.jpan.job"
    allowed_domains = ["tieba.baidu.com"]
    start_urls = ["http://tieba.baidu.com/f?kw=%E6%97%A5%E6%9C%AC%E7%95%99%E5%AD%A6&ie=utf-8&pn=0",]
    headers = Jpan_config().get_Request_Headers()

    def parse(self, response):
        items = []
        sel = Selector(response)
        sites_even = sel.css('a.j_th_tit')
        furl = sel.xpath("/html/head/meta[2][@furl]")
        for site in sites_even:
            item = JpanList_Items()
            item['title'] = site.xpath('text()').extract()
            item["link"] = site.xpath('@href').extract()
            item["furl"] = furl.x('@furl').extract()
            item['bid'] = item["link"][0].replace("/p/",'')
            items.append(item)
            print item['bid']

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
            sql = "SELECT * FROM jpanlist WHERE bid = " + item['bid']
            cur.execute(sql)
            rows = cur.fetchall()
            print sql
            log.msg(sql)
            print rows
            log.msg(rows)
            if rows ==  None:
                cur.execute('insert into jpanlist(title,link,furl,indate) values (%s, %s, %s, now())', (item['title'][i], item['link'][i], item['furl'][i]))

                print 'New Insert bid:' + item['bid']
                log.msg('New Insert bid:' + item['bid'])
            else:
                print 'bid:' + item['bid'] + ' is exists'
                log.msg('bid:' + item['bid'] + ' is exists')
            #JpanItemSpider().request(item['bid'])
            #return JpanItemSpider().request(item['bid'])
        print items
        for item in items:
             yield  scrapy.Request(item["link"],
                             callback=self.tlist)

    def tlist(self,response):
        items = []
        p = pq(response.body)
        #print response.body
        sites_even = p("div.l_post")
        h = pq(response.body)

        furl = h("[furl*='tieba']").attr("furl")
        bid = h("[rel*='canonical']").attr("href")
        print 'bid : ' + bid
        if(bid == None):
            return;
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

            for ins in items:
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
                    sql = "SELECT * FROM jpanitem WHERE contentid = " + ins['contentid']
                    print sql
                    cur.execute(sql)
                    rows = cur.fetchall()

                    print sql
                    log.msg(sql)
                    print rows
                    log.msg(rows)
                    if rows ==  None:
                        cur.execute('insert into jpanitem(bid,userid,username,userhead,userhome,contentid,content,turl,furl,indate) values (%s, %s, %s,%s, %s, %s,%s, %s, %s, now())', (ins["bid"],ins["userid"],ins["username"],ins["userhead"],ins["userhome"],ins["contentid"],ins["content"],ins["turl"],ins["furl"]))
                        print 'New Insert contentid:' + ins['contentid']
                        log.msg('New Insert contentid:' + ins['contentid'])
                    else:
                        print 'contentid:' + ins['contentid'] + ' is exists'
                        log.msg('contentid:' + ins['contentid'] + ' is exists')
                    cur.close()
                    conn.commit()
                    conn.close()
                except Exception, e:
                    #print Exception,":",e
                    errorMsg = Exception,":",e
                    print errorMsg + ' : ' + log.DEBUG
                    log.msg(errorMsg,level=log.DEBUG)

                next = p('.pb_list_pager a').filter(lambda i: pq(this).text() == u'\u4e0b\u4e00\u9875').attr('href')
                if next <> None:
                    yield scrapy.Request('http://tieba.baidu.com' + next,
                                     callback=self.tlist)
                continue