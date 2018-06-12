# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import scrapy
from scrapy import log
from db_peewee import *

class HistoricalDataPipeline(object):
    def __init__(self):
        self.list = []
        self.db = test_db
        self.db.connect()

    def process_item(self, li, spider):
        self.__save_mysql(li)

    def __save_mysql(self, li):
        record_timestamp = int(round(time.time() * 1000))
        cur = self.db.cursor()
        sql = "select count(id) from t_coinmarketcap_daily_quote where `publish_timestamp`= %s and `currency_id`=%s;"
        cur.execute(sql, (li['publish_timestamp'],li['currency_id']))
        result = cur.fetchone()

        if result[0] != 0:
            pass
        else:
            with self.db.atomic():
                # print 1
                # walian.insert_many(self.list).execute()
                t_coinmarketcap_daily_quote.insert(
                    currency_id = li['currency_id'], publish_timestamp = li['publish_timestamp'], open_price = li['open_price'],
                    high_price = li['high_price'],low_price = li['low_price'], close_price = li['close_price'],
                    turnover_volume = li['turnover_volume'], marke_value = li['marke_value'], unit=li['unit'],
                    update_time=record_timestamp
                    ).execute()
        cur.close()
        # 关闭数据库连接

    def close_spider(self, spider, ):
        self.db.close()
