import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


class Jpan_config(object):
    def get_Request_Headers(self):
        headers = {
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.81",
        "Connection": "keep-alive",
        "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36",
        "Referer": "http://tieba.baidu.com/",
        "Cookie" : "BAIDUID=196F1B10BCBA7DC3FA8B9B21DDB0C856:FG=1; BIDUPSID=9FB0464A296F82CA31AFC9BAD53C3757; BDRCVFR[TXZ8BX1B2fs]=mk3SLVN4HKm; TIEBA_USERTYPE=856a30f6db8a544e4f061c84; TIEBAUID=c9d8190770e5388957236bf3; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; H_PS_PSSID=1420_13074_13381_12868_13323_12691_13410_10562_12723_13439_13657_13288_13601_11520_13085_8498_13156; BDUSS=EkzZmZobm9qTnRZQWNNN3BMblFyTFpoTWlqUzdwMXEtelVyMXM2NXp4ckxoMkZWQVFBQUFBJCQAAAAAAAAAAAEAAACE6VAUeWN6aG91aHlpAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMv6OVXL-jlVV"
        }

        rules = (
            Rule(LinkExtractor(allow='tieba\.baidu\.com/f?kw=%E6%97%A5%E6%9C%AC%E7%95%99%E5%AD%A6'),follow=True,
            ),
            Rule(LinkExtractor(allow='tieba\.baidu\.com/p/'),
                'parse_Jpan_Item',
            ),
        )

        return headers