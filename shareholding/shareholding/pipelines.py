# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import csv
import os

import time
from database_connection_handle import DatabaseConnectionHandle


class ShareholdingPipeline(object):
    def __init__(self):
        handler = DatabaseConnectionHandle()
        self.stock_code = []
        self.stock_name = []
        self.positions_amount = []
        self.percent = []
        self.csv_switch = False

        # self.r = handler.get_cache_redis_connectin()

        self.conn = handler.get_spider_connection()

    def process_item(self, item, spider):
        self.csv_switch = True
        self.stock_code.append(item['stock_code'])
        self.stock_name.append(item['stock_name'])
        self.positions_amount.append(item['positions_amount'])
        self.percent.append(item['percent'])
        self.item = item
        print item
        print self.item

        non_existent_mysql = self.__is_mysql(item)
        if non_existent_mysql:
            self.__save_to_mysql(item)
        return item

    # def __csv_writer(self,):
    #     # python2可以用file替代open
    #     if self.csv_switch:
    #         filename = "Shareholding Date" + str(self.item['shareholding_date']) + ".csv"
    #
    #         if not os.path.exists(filename):
    #             with open(filename, "ab", ) as csvfile:
    #                 csvfile.write(codecs.BOM_UTF8)
    #                 writer = csv.writer(csvfile, dialect='excel')
    #                 writer.writerow(["股份代號", "股份名稱", "於中央結算系統的持股量", "佔已發行股份百分比"])
    #                 writer.writerows(zip(self.stock_code,self.stock_name,self.positions_amount,self.percent))
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

        shareholding_date = item['shareholding_date']
        stock_code = int(item['stock_code'])

        sql = "select count(id) from shareholding where stock_code = %s  and shareholding_date = %s "

        cur.execute(sql, (stock_code, shareholding_date))

        result = cur.fetchone()
        a = result[0]
        if result[0] != 0:
            return True
        else:
            return False

            # 保存mysql

    def __save_to_mysql(self, item):
        self.cur = self.conn.cursor()

        stock_code = int(item['stock_code'])
        positions_amount = int(item['positions_amount'])
        percent = item['percent']
        shareholding_date = str(item['shareholding_date'])
        record_timestamp = time.time()

        sql = "insert into shareholding( `STOCK_CODE`, `POSITIONS_AMOUNT`, `PERCENT` , `SHAREHOLDING_DATE` , `RECORD_TIMESTAMP`  ) values(%s,%s,%s,%s,%s)"
        result = self.cur.execute(sql, (
            stock_code, positions_amount,percent,shareholding_date, record_timestamp))
        self.conn.commit()
        self.cur.close()


        # 关闭数据库连接

    def close_spider(self, spider,):
        #self.__csv_writer()
        self.conn.close()