# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

import MySQLdb
from database_connection_handle import DatabaseConnectionHandle


class IndexDailyBulletinPipeline(object):
    def __init__(self):
        databaseConnectionHandle = DatabaseConnectionHandle()
        self.conn = databaseConnectionHandle.get_spider_connection()
        # self.conn = MySQLdb.connect(host='218.244.138.88', port=13456, user='spiderdb', passwd='Cqmyg321',
        #                             db='spiderdb', charset='utf8')

    def process_item(self, item, spider):
        self.item = item
        print item
        print self.item

        non_existent_mysql = self.__is_mysql(item)
        if non_existent_mysql:
            self.__save_to_mysql(item)
        return item

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

        trade_date = item['trade_date']
        index_ = str(item['index'])

        sql = "select count(id) from index_daily_bulletin where trade_date = %s and index_ = %s"
        print sql,trade_date,index_
        cur.execute(sql, (trade_date,index_))

        result = cur.fetchone()
        a = result[0]
        if result[0] != 0:
            return True
        else:
            return False
            # 保存mysql

    def __save_to_mysql(self, item):
        self.cur = self.conn.cursor()

        table_type = item['table_type']
        trade_date = item['trade_date']
        time_array =time.strptime(item['trade_date'], "%Y%m%d")
        trade_date_timestamp = int(time.mktime(time_array))
        index_ = str(item['index'])
        index_currency = item['index_currency']
        daily_high = item['daily_high']
        daily_low = item['daily_low']
        index_close = item['index_close']
        point_change = item['point_change']
        percent_change = item['percent_change']
        dividend_yield = item['dividend_yield']
        pe_ratio = item['pe_ratio']
        record_timestamp = int(time.time())

        if table_type == 2:
            index_turnover = item['index_turnover']
            market_turnover = item['market_turnover']
            index_currency_to_hkd = item['index_currency_to_hkd']
            sql = "insert into index_daily_bulletin( `TABLE_TYPE`, `TRADE_DATE`,`INDEX_`,`INDEX_CURRENCY` , `DAILY_HIGH` , `DAILY_LOW`, `INDEX_CLOSE` , `POINT_CHANGE` , `PERCENT_CHANGE`, `DIVIDEND_YIELD`, `PE_RATIO` ,`INDEX_TURNOVER` , `MARKET_TURNOVER` ,`INDEX_CURRENCY_TO_HKD`,`TRADE_DATE_TIMESTAMP`,`RECORD_TIMESTAMP`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            result = self.cur.execute(sql, (
                table_type, trade_date,index_ ,index_currency,daily_high, daily_low, index_close, point_change,percent_change, dividend_yield, pe_ratio ,index_turnover, market_turnover, index_currency_to_hkd,trade_date_timestamp,record_timestamp))
            self.conn.commit()
            self.cur.close()

        if table_type == 1:
            sql = "insert into index_daily_bulletin( `TABLE_TYPE`, `TRADE_DATE`,`INDEX_`,`INDEX_CURRENCY` , `DAILY_HIGH` , `DAILY_LOW`, `INDEX_CLOSE` , `POINT_CHANGE` , `PERCENT_CHANGE`, `DIVIDEND_YIELD`, `PE_RATIO` ,`TRADE_DATE_TIMESTAMP`,`RECORD_TIMESTAMP` ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            result = self.cur.execute(sql, (
                table_type, trade_date, index_, index_currency, daily_high, daily_low, index_close, point_change,
                percent_change, dividend_yield, pe_ratio,
                trade_date_timestamp, record_timestamp))
            self.conn.commit()
            self.cur.close()


        # 关闭数据库连接

    def close_spider(self, spider,):
        #self.__csv_writer()
        self.conn.close()