import urllib2
import urllib
import json
import re
import scrapy
import sys
import redisco
import string
sys.stdout = open('output.txt', 'w')
from scrapy import log

from baidu_tieba.items import JpanItem_Items
from baidu_tieba.items import JpanList_Items
from baidu_tieba.spiders.config import Jpan_config

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from redisco import models


class JpanSpider(CrawlSpider):
    #redisco.connection_setup(host='localhost', port=6379, db=10)

    name = "baidu.jpan"
    allowed_domains = ["tieba.baidu.com"]
    start_urls = [
        "http://tieba.baidu.com/f?kw=%E6%97%A5%E6%9C%AC%E7%95%99%E5%AD%A6&ie=utf-8&pn=0", ]
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
            item['bid'] = item["link"][0].replace("/p/", '')
            # print item;
            items.append(item)
            print item['bid']
            jRedisco = JRedisco(bid=item['bid'])
            if jRedisco.is_valid():
                jRedisco.save()
                print 'jRedisco.save()'
            else:
                print 'jRedisco.is_valid'
        nextUrl = "http://tieba.baidu.com" + \
            sel.css("a.next::attr(href)").extract()[0]
        print 'Next Page :' + nextUrl
        # self.insert(items)
        request = scrapy.Request(nextUrl,
                                 callback=self.parse)
        # return items
        return request


class JRedisco(models.Model):
    bid = models.Attribute(required=True)
    created_at = models.DateTimeField(auto_now_add=True)
    fave_colors = models.ListField(str)
