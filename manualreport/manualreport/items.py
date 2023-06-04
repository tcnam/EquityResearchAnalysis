# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ManualreportItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class EnterpriseItem(scrapy.Item):
    soTT=scrapy.Field()
    maCK=scrapy.Field()
    tenCTY=scrapy.Field()
    nganh=scrapy.Field()
    san=scrapy.Field()
    klGD=scrapy.Field()
    link=scrapy.Field()

class DemoItem(scrapy.Item):
    number_of_pages=scrapy.Field()