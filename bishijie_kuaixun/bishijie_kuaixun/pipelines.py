# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import scrapy
from scrapy import log
from db_peewee import *

class BishijieKuaixunPipeline(object):
    def __init__(self):
        self.list = []
        self.db = test_db
        self.db.connect()

    def process_item(self, li, spider):
        self.__save_mysql(li)

    def __save_mysql(self, li):
        record_timestamp = int(time.time())
        cur = self.db.cursor()
        sql = "select count(id) from bishijie_kuaixun where title = %s;"
        cur.execute(sql, (li['title']))
        result = cur.fetchone()

        if result[0] != 0:
            pass
        else:
            with self.db.atomic():
                # walian.insert_many(self.list).execute()
                bishijie_kuaixun.insert(title=li['title'], text=str(li['text']).replace(r'<br />',''), record_timestamp=record_timestamp).execute()

        cur.close()
        # 关闭数据库连接

    def close_spider(self, spider, ):
        self.db.close()