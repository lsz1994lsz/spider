# -*- coding: utf-8 -*-

import datetime
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import scrapy
from scrapy import log
from db_peewee import *


class Ipv4Pipeline(object):
    def __init__(self):
        self.list = []
        self.db = test_db
        self.db.connect()
        # databaseConnectionHandle = DatabaseConnectionHandle()
        # self.conn = databaseConnectionHandle.get_spider_connection()


    def process_item(self, li,spider):
        self.__save_or_update_mysql(li)


    def __save_or_update_mysql(self, li):
        self.dict5 = {}
        self.dict5['apnic'] = li['apnic']
        self.dict5['en'] = li['en']
        self.dict5['ipv4'] = li['ipv4']
        self.dict5['ip'] = li['ip']
        self.dict5['num'] = li['num']
        self.dict5['public_timestamp'] = li['public_timestamp']
        self.dict5['record_timestamp']= int(time.time())
        self.list.append(self.dict5)


        if len(self.list) == li['len']:
            cur = self.db.cursor()
            # sql1 = "select count(id) from ipv4_copy where record_timestamp regexp '^%s';"
            today_timestamp = int(time.mktime(datetime.date.today().timetuple()))
            sql = "select count(id) from ipv4 where record_timestamp>%s;"
            cur.execute(sql, (today_timestamp))
            result = cur.fetchone()

            if result[0] != 0:
                # sql = "UPDATE ipv4 set `apnic`=%s,`en`=%s,`ipv4`=%s ,`ip`=%s ,`num`=%s ,`public_timestamp`=%s , `record_timestamp`=%s  where public_timestamp = %s and en = %s"
                # result = self.cur.execute(sql,(apnic,en,ipv4,ip,num,public_timestamp,`record_timestamp`))
                pass
            else:
                with self.db.atomic():
                    ipv4.insert_many(self.list).execute()
            yesterday_timestamp = int(time.mktime((datetime.date.today() - datetime.timedelta(days=1)).timetuple()))
            del_num = ipv4.delete().where(ipv4.record_timestamp < yesterday_timestamp).execute()
            scrapy.log.msg(str(del_num), level=log.WARNING)

            cur.close()
        # 关闭数据库连接

    def close_spider(self, spider,):
        self.db.close()