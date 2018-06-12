# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import json
import datetime
import MySQLdb
from database_connection_handle import DatabaseConnectionHandle
from spiders.spider import Spider

class HkStockBuyBackPipeline(object):
    def __init__(self):

        handler = DatabaseConnectionHandle()



        self.conn = handler.get_spider_connection()

    def process_item(self, item, spider):


        non_existent_mysql = self.__is_mysql(item)
        if non_existent_mysql:
            self.__save_to_mysql(item)


        return item

        # mysql是否存在该数据

    def __is_mysql(self, item):

        is_existed_in_db = self.__is_existed_in_db(item)
        if is_existed_in_db:
            print "has existed in mysql"
            return False
        else:
            print "no has existed in mysql"
            return True

            # mysql是否存在该数据

    def __is_existed_in_db(self, item):
        cur = self.conn.cursor()

        trade_date_timestamp = int(item['trade_date_timestamp'])
        stock_code = int(item['stock_code'])

        sql = "select count(id) from hk_buy_back_data where stock_code = %s  and trade_date_timestamp = %s "

        cur.execute(sql, (stock_code, trade_date_timestamp))

        result = cur.fetchone()
        a = result[0]
        if result[0] != 0:
            return True
        else:
            return False

            # 保存mysql

    def __save_to_mysql(self, item):
        self.cur = self.conn.cursor()

        stock_code = item['stock_code']

        buy_back_amount = int(item['buy_back_amount'])
        highest_buy_back_price = float(item['highest_buy_back_price'])
        minimum_buy_back_price = float(item['minimum_buy_back_price'])
        average_buy_back_price = float(item['average_buy_back_price'])
        buy_back_total = int(item['buy_back_total'])

        trade_date_timestamp = item['trade_date_timestamp']
        record_timestamp = time.time()

        sql = "insert into hk_buy_back_data( `STOCK_CODE`, `BUY_BACK_AMOUNT`, `HIGHEST_BUY_BACK_PRICE` , `MINIMUM_BUY_BACK_PRICE` , `AVERAGE_BUY_BACK_PRICE` ,`BUY_BACK_TOTAL` , `TRADE_DATE_TIMESTAMP`,`RECORD_TIMESTAMP` ) values(%s,%s,%s,%s,%s,%s,%s,%s)"

        result = self.cur.execute(sql, (
            stock_code, buy_back_amount, highest_buy_back_price, minimum_buy_back_price, average_buy_back_price,
            buy_back_total, trade_date_timestamp, record_timestamp))

        self.conn.commit()
        self.cur.close()


        # 关闭数据库连接

    def close_spider(self, spider):
        self.conn.close()