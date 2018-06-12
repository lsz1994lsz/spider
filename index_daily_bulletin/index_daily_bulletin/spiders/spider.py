# coding:utf-8
import re
import datetime
import time
import sys

from custom_log_v2 import CustomLog

reload(sys)
sys.setdefaultencoding('utf8')
from time import mktime
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from index_daily_bulletin.items import IndexDailyBulletinItem
from lxml import etree
from ..settings import *

import scrapy
from scrapy import log
from scrapy import Selector, Request
from scrapy.contrib.spiders import CrawlSpider

class Spider(CrawlSpider):
    CustomLog(CUSTOM_LOG_LEVEL)
    name = 'index_daily_bulletin'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    }
    def start_requests(self):
        start_url_request_list = []


        i = 0
        while i < 5:

            date_timestamp = (datetime.datetime.now() - datetime.timedelta(days=i))
            date = str(date_timestamp.day) + date_timestamp.strftime('%b%y')
            url_hscei = 'http://www.hsi.com.hk/HSI-Net/static/revamp/contents/en/indexes/report/hscei/idx_' + str(date) + '.csv'
            start_request = Request(url_hscei, callback=self.parse,headers=self.headers)
            start_url_request_list.append(start_request)
            url_hsi = 'http://sc.hangseng.com/gb/www.hsi.com.hk/HSI-Net/static/revamp/contents/en/indexes/report/hsi/idx_' + str(date) + '.csv'
            start_request2 = Request(url_hsi, callback=self.parse,headers=self.headers)
            start_url_request_list.append(start_request2)
            i += 1

        return start_url_request_list

    def parse(self, response):
        body = str((response.body).decode(WEB_PAGE_ENCODING,'ignore')).encode('utf8')
        body_line = body.splitlines(True)
        print len(body_line)
        print response.status
        if response.status != 404:
            if len(body_line) > 0:
                for i in body_line:
                    data = i.replace('"', '').replace('\r\n','').split('\t')
                    if body_line.index(i) > 1:
                        if len(body_line) == 3:
                            table_type = 1
                            print data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9]
                            positions_record_data = self.parase_str_list(data,table_type)
                            yield positions_record_data
                        #
                        if len(body_line) == 8:
                            table_type = 2
                            print data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[
                                10], data[11], data[12]
                            positions_record_data = self.parase_str_list(data,table_type)
                            yield positions_record_data
            else:
                scrapy.log.msg("没有数据" , level=log.ERROR)



    def parase_str_list(self, data,table_type):
        positions_record_data = IndexDailyBulletinItem()
        positions_record_data['table_type'] = table_type
        positions_record_data['trade_date'] = data[0]
        positions_record_data['index'] = data[1]
        positions_record_data['index_currency'] = data[2]
        positions_record_data['daily_high'] = data[3]
        positions_record_data['daily_low'] = data[4]
        positions_record_data['index_close'] = data[5]
        positions_record_data['point_change'] = data[6]
        positions_record_data['percent_change'] = data[7]
        positions_record_data['dividend_yield'] = data[8]
        positions_record_data['pe_ratio'] = data[9]

        if table_type == 2:
            positions_record_data['index_turnover'] = data[10]
            print data[11]
            print float(108244)
            positions_record_data['market_turnover'] = data[11]
            positions_record_data['index_currency_to_hkd'] = data[12]

        return positions_record_data