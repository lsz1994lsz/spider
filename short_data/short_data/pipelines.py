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
from spiders.short_data_spider import ShortDataSpider


class ShortDataPipeline(object):
    def __init__(self):

        handler = DatabaseConnectionHandle()

        self.r = handler.get_cache_redis_connectin()

        self.conn = handler.get_spider_connection()

    def process_item(self, item, spider):

        non_existent_redis = self.__is_redis(item)
        # stock_code = self.__get_stock_code(item['stock_code'])
        # if stock_code == u'06899':
        #     # ShortDataSpider.j +=1
        #     # if ShortDataSpider.j == 4:
        #     time1 = ShortDataSpider.time1
        #     time2 = time.time()
        #     time3 = time2 - time1
        #     print time3
        #     print 'aaa'

        if non_existent_redis:
            non_existent_mysql = self.__is_mysql(item)
            if non_existent_mysql:
                self.__save_to_mysql(item)
                self.__save_to_redis(item)
            else:

                self.__save_to_redis(item)

        return item




    # 判断redis是否存在该数据
    def __is_redis(self, item):

        cache = self.__get_cache_from_redis(item)

        if cache == None:
            #print "no has existed in redis"
            return True
        else:
            #print "has existed in redis"
            return False

    # 取redis的key对应的值
    def __get_cache_from_redis(self, item):

        key = self.__get_redis_key(item)
        cache = self.r.get(key)
        return cache

    # 生成redis的key
    def __get_redis_key(self, item):

        stock_code = self.__get_stock_code(item['stock_code'])

        trade_date_timestamp = item['trade_date_timestamp']

        dateArray = datetime.datetime.utcfromtimestamp(trade_date_timestamp)
        trade_date_str = dateArray.strftime("%Y-%m-%d")

        key = "str:" + "short_data:" + "hk" + stock_code + ":" + trade_date_str

        return key


    # 保存到redis
    def __save_to_redis(self, item):

        key = self.__get_redis_key(item)

        self.r.set(key, str(item))


    # mysql是否存在该数据
    def __is_mysql(self, item):

        is_existed_in_db = self.__is_existed_in_db(item)
        if is_existed_in_db:
            #print "has existed in mysql"
            return False
        else:
            #print "no has existed in mysql"
            return True

    # mysql是否存在该数据
    def __is_existed_in_db(self, item):
        cur = self.conn.cursor()
        stock_type = "hk"
        trade_date_timestamp = int(item['trade_date_timestamp'])
        stock_code = self.__get_stock_code(item['stock_code'])

        sql = "select count(id) from spider_short_data where stock_code = %s and stock_type = %s and trade_date_timestamp = %s "

        cur.execute(sql, (stock_code, stock_type, trade_date_timestamp))

        result = cur.fetchone()

        if result[0] != 0:
            return True
        else:
            return False

    # 保存到mysql
    def __save_to_mysql(self, item):

        cur = self.conn.cursor()

        stock_type = "hk"

        record_timestamp = time.time()

        trade_date_timestamp = item['trade_date_timestamp']
        short_volume_shares = int(item['short_volume_shares'].replace(",", ""))
        short_turnover_amount = int(item['short_turnover_amount'].replace(",", ""))
        turnover_amount = int(item['turnover_amount'].replace(",", ""))
        turnover_volume_shares = int(item['turnover_volume_shares'].replace(",", ""))

        sql = "insert into spider_short_data(`STOCK_TYPE` , `STOCK_CODE`, `SHORT_VOLUME_SHARES`, `SHORT_TURNOVER_AMOUNT` , `TURNOVER_AMOUNT` , `TURNOVER_VOLUME_SHARES` ,`RECORD_TIMESTAMP` , `TRADE_DATE_TIMESTAMP`  ) values(%s,%s,%s,%s,%s,%s,%s,%s)"

        stock_code = item['stock_code']
        # if stock_code == u'6899':
        #     # ShortDataSpider.j +=1
        #     #
        #     # if ShortDataSpider.j == 4:
        #     time1 = ShortDataSpider.time1
        #     time2 = time.time()
        #     time3 = time2 - time1
        #     print time3
        #     print 'aaa'

        stock_code = self.__get_stock_code(stock_code)

        result = cur.execute(sql, (
            stock_type, stock_code, short_volume_shares, short_turnover_amount, turnover_amount,
            turnover_volume_shares,
            record_timestamp, trade_date_timestamp))

        self.conn.commit()


    #股票代码
    def __get_stock_code(self, stock_code):
        if len(stock_code) < 5:
            length = len(stock_code)
            lack = 5 - length
            i = 0
            while i < lack:
                i += 1
                stock_code = "0" + stock_code
        return stock_code


    # 关闭数据库连接
    def close_spider(self, spider):
            self.conn.close()




