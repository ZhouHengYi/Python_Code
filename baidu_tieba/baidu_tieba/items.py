import scrapy

class JpanItem_Items(scrapy.Item):
    bid = scrapy.Field()
    userid = scrapy.Field()
    username = scrapy.Field()
    userhead = scrapy.Field()
    userhome = scrapy.Field()
    contentid = scrapy.Field()
    content = scrapy.Field()
    turl = scrapy.Field()
    furl = scrapy.Field()
    publisherDate = scrapy.Field()

class JpanList_Items(scrapy.Item):
    bid = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    furl = scrapy.Field()
    publisherDate = scrapy.Field()
