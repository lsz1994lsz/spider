# coding:utf-8
import _strptime
import re
import datetime
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from time import mktime
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from hk_stock_buy_back.items import HkStockBuyBackItem
from lxml import etree
from ..settings import *
from custom_log_v2 import CustomLog

class Spider(CrawlSpider):
    CustomLog(CUSTOM_LOG_LEVEL)
    name = 'hk_stock_buy_back'

    def start_requests(self):
        start_url_request_list = []

        i = 0

        while i < RUN_TIME:
            i += 1
            url = "http://hk.eastmoney.com/buyback_%d.html" % i
            start_request = Request(url, callback=self.parse)
            start_url_request_list.append(start_request)


        return start_url_request_list

    def parse(self, response):
        body = (response.body).decode(WEB_PAGE_ENCODING,'ignore')
        html = etree.HTML(body)
        code = html.xpath('//*[@id="main"]/div[1]/div[2]/div[2]/ul')

        if code != None:
            i = 0
            while i < 50:
                info = code[i].xpath('string(.)').replace("万", "00").replace("\r", "")
                content = info.replace(' ', '')
                data = re.split('\\n', content)
                i += 1
                #windows
                # if len(data) == 11:
                #     buy_back_data = self.parase_str_list(data)
                #     yield buy_back_data

                # linux
                if len(data) == 10:
                    buy_back_data = self.parase_str_list(data)
                    yield buy_back_data



    def parase_str_list(self, data):
        # windows
        # buy_back_data = HkStockBuyBackItem()
        # if data[2] != None:
        #     buy_back_data['stock_code'] = data[2]
        #
        # if data[4] != None:
        #     data[4] = re.sub('\.', '', data[4])
        #     buy_back_data['buy_back_amount'] = data[4]
        #
        # if data[5] != None:
        #     buy_back_data['highest_buy_back_price'] = data[5]
        #
        # if data[6] != None:
        #     buy_back_data['minimum_buy_back_price'] = data[6]
        #
        # if data[7] != None:
        #     buy_back_data['average_buy_back_price'] = data[7]
        #
        # if data[8] != None:
        #     data[8] = re.sub('\.', '', data[8])
        #     buy_back_data['buy_back_total'] = data[8]
        #
        # if data[9] != None:
        #     trade_date = datetime.datetime.strptime(data[9], "%Y-%m-%d")
        #     trade_date_timestamp = time.mktime(trade_date.timetuple())
        #     buy_back_data['trade_date_timestamp'] = trade_date_timestamp

        # linux
        buy_back_data = HkStockBuyBackItem()
        if data[1] != None:
            buy_back_data['stock_code'] = data[1]

        if data[3] != None:
            data[3] = re.sub('\.', '', data[3])
            buy_back_data['buy_back_amount'] = data[3]

        if data[4] != None:
            buy_back_data['highest_buy_back_price'] = data[4]

        if data[5] != None:
            buy_back_data['minimum_buy_back_price'] = data[5]

        if data[6] != None:
            buy_back_data['average_buy_back_price'] = data[6]

        if data[7] != None:
            data[7] = re.sub('\.', '', data[7])
            buy_back_data['buy_back_total'] = data[7]

        if data[8] != None:
            trade_date = datetime.datetime.strptime(data[8], "%Y-%m-%d")
            trade_date_timestamp = time.mktime(trade_date.timetuple())
            buy_back_data['trade_date_timestamp'] = trade_date_timestamp


        return buy_back_data