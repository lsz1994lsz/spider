# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import scrapy
from scrapy import log
from db_peewee import *


class JinsePipeline(object):
    def __init__(self):
        self.list = []
        self.db = test_db
        self.db.connect()

    def process_item(self, li, spider):
        self.__save_mysql(li)

    def __save_mysql(self, li):
        record_timestamp = int(time.time())
        cur = self.db.cursor()
        sql = "select count(id) from jinse where title = %s;"
        cur.execute(sql, (li['title']))
        result = cur.fetchone()

        if result[0] != 0:
            pass
        else:
            with self.db.atomic():
                # jinse.insert_many(self.list).execute()
                jinse.insert(title = li['title'] ,text = li['text'], record_timestamp = record_timestamp).execute()

        cur.close()
        # 关闭数据库连接

    def close_spider(self, spider,):
        self.db.close()