# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# 定义数据封装item
class DoubanmovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    order = scrapy.Field()
    content = scrapy.Field()
    contentnum = scrapy.Field()
    year = scrapy.Field()
    country = scrapy.Field()
    score = scrapy.Field()
    vary = scrapy.Field()

    pass
