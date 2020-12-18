# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo

class VscodeSshScrapyTestPipeline(object):
    def process_item(self, item, spider):
        return item
class MongoDBPipeline:
    print('Pipeline')
    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI')
        db_name = spider.settings.get('MONGODB_DB_NAME')
        db_coll = spider.settings.get('MONGODB_DB_COL')
        db_client = pymongo.MongoClient('mongodb://localhost:27017')
        self.coll = db_client[db_name][db_coll]

    def process_item(self, item, spider):
        self.insert_article(item)
        return item

    def insert_article(self, item):
        item = dict(item)
        print(item)
        self.coll.insert_one(item)

    def close_spider(self, spider):
        pymongo.MongoClient.db_clients.close()