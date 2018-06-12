# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import scrapy
from scrapy import log
from db_peewee import *


class BitcoinMarketsPipeline(object):
    def __init__(self):
        self.list = []
        self.db = test_db
        self.db.connect()

    def process_item(self, li, spider):
        self.__save_mysql(li)

    def __save_mysql(self, li):
        record_timestamp = int(round(time.time() * 1000))
        cur = self.db.cursor()
        # sql = "select count(id) from t_bourse_quote where title = %s;"
        # cur.execute(sql, 'a')
        # result = cur.fetchone()
        #
        # if result[0] != 0:
        #     pass
        # else:
        with self.db.atomic():
            # print 1
            # walian.insert_many(self.list).execute()
            t_bourse_quote.insert(currency_id=li['currency_id'], market_id=li['market_id'],
                                    price=li['price'], tradetime=li['tradetime'],
                                    volume_24h=li['volume_24h'], valume_rate=li['valume_rate'],
                                    unit=li['unit'], record_timestamp=record_timestamp
                                    ).execute()
        cur.close()
        # 关闭数据库连接

    def close_spider(self, spider, ):
        self.db.close()