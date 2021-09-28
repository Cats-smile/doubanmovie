# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs


import pymongo


class DoubanMoviePipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        scrapy_db = self.client['doubanmovie']  # 创建数据库
        self.coll = scrapy_db['movie']  # 创建数据库中的表格

    def process_item(self, item, spider):
        self.coll.insert_one(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
