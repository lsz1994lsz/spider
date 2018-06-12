# -*- coding: utf-8 -*-
import re
import StringIO
import datetime
import time
import sys

import scrapy
from scrapy import log
reload(sys)
sys.setdefaultencoding('utf8')
from time import mktime
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from short_data.items import ShortDataItem
from ..settings import *
from custom_log_v2 import CustomLog


class ShortDataSpider(CrawlSpider):
    CustomLog(CUSTOM_LOG_LEVEL)
    name = "short_data"

    time1 = time.time()
    j = 0
    #URL
    def start_requests(self):
        start_url_request_list = []

        i = 0
        while i < RUN_TIME:
        # url = "https://www.hkex.com.hk/chi/stat/smstat/dayquot/d170716c.htm#short_selling"
            url = "https://www.hkex.com.hk/chi/stat/smstat/dayquot/d#{date}c.htm#short_selling"
            trade_date_timestamp = datetime.datetime.now() - datetime.timedelta(days=i)
            year = trade_date_timestamp.strftime("%Y")
            year = year[-2:]
            month = trade_date_timestamp.strftime("%m")
            day = trade_date_timestamp.strftime("%d")
            date_str = year + month + day
            url = url.replace("#{date}", date_str)

            start_request = Request(url, callback=self.parse)
            start_url_request_list.append(start_request)
            i += 1

        return start_url_request_list


    #主体
    def parse(self, response):
        # scrapy.log.msg('INFO', level=log.INFO)
        # scrapy.log.msg('ERROR', level=log.ERROR)
        # scrapy.log.msg('WARNING', level=log.WARNING)
        # scrapy.log.msg('CRITICAL', level=log.CRITICAL)
        # scrapy.log.msg('DEBUG', level=log.DEBUG)

        body = (response.body).decode(WEB_PAGE_ENCODING,'ignore')
        url = response.url

        date_str = re.findall("\d+", url)[0]

        trade_date_timestamp = self.__get_trade_date_timestamp(date_str)

        start_index = body.find('<a name = "short_selling">')

        parase_content = body[start_index:]
        buf = StringIO.StringIO(parase_content)

        # 去掉无用的数据
        i = 0
        while i <= 5:
            buf.readline()
            i += 1

        line = buf.readline()

        flag = True

        while flag:
            short_data = self.parse_line(line)

            if short_data != None:

                stock_code = short_data['stock_code']

                short_data['trade_date_timestamp'] = trade_date_timestamp

                if len(stock_code) < 4:
                    yield short_data
                else:
                    if stock_code[:1] != '%' and stock_code[:1] != '7':
                        yield short_data

            line = buf.readline()
            flag = self.__runnable(line)

    # 判断空行
    def __runnable(self, line):
        # if line != "\r\n" or line != "\n\r" or line != "" or line != '\r' or line != '\r':
        #	return True
        if len(line) != 2:
            if len(line) != 0:
                return True

        return False


#抽取
    def parse_line(self, line):

        str_list_filted = []
        text = re.findall(ur"[^%]\s\d+\s|\d+,\d+[,\d]*", line)

        for use in text:
            use = use.replace(',','').replace("\n", "").replace("\r", "").replace(" ", "")
            str_list_filted.append(use)

        short_data = ShortDataItem()

        list_filted_len = len(str_list_filted)

        if list_filted_len == 5:
            short_data = self.parase_str_list(str_list_filted)

            return short_data

    #字典
    def parase_str_list(self, str_list):

        short_data = ShortDataItem()
        point = 1
        for text in str_list:
            if point == 1:
                short_data['stock_code'] = text

            if point == 2:
                short_data['short_volume_shares'] = text

            if point == 3:
                short_data['short_turnover_amount'] = text

            if point == 4:
                short_data['turnover_volume_shares'] = text

            if point == 5:
                short_data['turnover_amount'] = text
            point += 1

        return short_data

    #更改日期格式
    def __get_trade_date_timestamp(self, date_str):

        year = date_str[:2]
        month = date_str[2:4]
        day = date_str[4:6]

        year = str(20) + year

        trade_date = year + "-" + month + "-" + day

        trade_date = datetime.datetime.strptime(trade_date, "%Y-%m-%d")

        trade_date_timestamp = time.mktime(trade_date.timetuple())


        return trade_date_timestamp


