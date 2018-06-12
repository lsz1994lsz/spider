# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time

from database_connection_handle import DatabaseConnectionHandle


class ShortPositionsPipeline(object):

    def __init__(self):
        databaseConnectionHandle = DatabaseConnectionHandle()
        self.conn = databaseConnectionHandle.get_spider_connection()

    def process_item(self, item, spider):

        trade_date = item['trade_date']
        if item['trade_date'] != '':
            if self.__is_existed_in_db(item):
                pass
                #print str(item) +  " has existed in DB"
            else:
                self.save_to_mysql(item)
        return item

    def save_to_mysql(self, item):
        cur = self.conn.cursor()

        trade_date = item['trade_date']
        trade_date_timestamp = time.mktime(time.strptime(trade_date, '%d/%m/%Y'))

        stock_code = self.__fix_stock_code(item['stock_code'])
        short_positions_shares = item['short_positions_shares']
        short_positions_amount = item['short_positions_amount']
        record_timestamp = time.time()

        sql = "insert into short_position( `stock_code` , `trade_date_timestamp` , `short_positions_shares` , `short_positions_amount` , `record_timestamp` ) values(%s,%s,%s,%s,%s)"

        result = cur.execute(
            sql,
            (stock_code,
             trade_date_timestamp,
             short_positions_shares,
             short_positions_amount,
             record_timestamp))

        self.conn.commit()

    def __fix_stock_code(self, simple_stock_code):

        length = len(simple_stock_code)

        if length == 5:
            return simple_stock_code

        fix_time = 5 - length

        stock_code = simple_stock_code
        while fix_time > 0:
            stock_code = "0" + stock_code

            fix_time -= 1

        return stock_code

    def __close_spider(self):
        self.conn.close()

    def __is_existed_in_db(self, item):

        cur = self.conn.cursor()

        trade_date = item['trade_date']
        trade_date_timestamp = time.mktime(time.strptime(trade_date, '%d/%m/%Y'))

        stock_code = self.__fix_stock_code(item['stock_code'])

        sql = "select count(1) from short_position where stock_code = %s and trade_date_timestamp = %s "

        count = cur.execute(sql, (stock_code, trade_date_timestamp))

        result = cur.fetchone()

        if result[0] != 0:
            return True
        else:
            return False
