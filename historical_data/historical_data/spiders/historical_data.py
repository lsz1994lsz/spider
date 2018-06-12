# -*- coding: UTF-8 -*-
import sys
reload(sys)
# sys.setdefaultencoding('uft8')
from custom_log_v2 import CustomLog
import re
import datetime
import time
from time import mktime
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import HistoricalDataItem
from lxml import etree
from ..settings import *
import scrapy
from scrapy import log
from scrapy import Selector, Request
from scrapy.contrib.spiders import CrawlSpider

class Spider(CrawlSpider):
    # CustomLog(CUSTOM_LOG_LEVEL)
    name = 'historical_data'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
        "content-type:text/html; charset=utf-8"
    }
    def start_requests(self):
        start_url_request_list = []
        self.name_list = ['bitcoin','ethereum','ripple','bitcoin-cash','eos','cardano','litecoin','stellar','tron','neo']
        self.run_time = 0
        self.a = []
        while self.run_time < len(self.name_list):
            url = 'https://coinmarketcap.com/zh/currencies/' + self.name_list[self.run_time] +'/historical-data/?start=20180510&end=20281229'
            self.run_time +=1
            start_request = Request(url, callback=self.parse,headers=self.headers,dont_filter=True)
            start_url_request_list.append(start_request)
        return start_url_request_list

    def parse(self, response):
        body1 = str(response.body).decode(response.encoding,'ignore')
        body = re.sub(r',', '', body1)
        currency_id = re.findall(r'https://coinmarketcap.com/zh/currencies/(.*)/historical-data',response.url)[0]
        text = etree.HTML(body)
        timestamp = text.xpath('//*[@id="historical-data"]/div/div[3]/table/tbody/tr/td[1]/text()')
        open_price = text.xpath('//*[@id="historical-data"]/div/div[3]/table/tbody/tr/td[2]/text()')
        high_price = text.xpath('//*[@id="historical-data"]/div/div[3]/table/tbody/tr/td[3]/text()')
        low_price = text.xpath('//*[@id="historical-data"]/div/div[3]/table/tbody/tr/td[4]/text()')
        close_price = text.xpath('//*[@id="historical-data"]/div/div[3]/table/tbody/tr/td[5]/text()')
        turnover_volume = text.xpath('//*[@id="historical-data"]/div/div[3]/table/tbody/tr/td[6]/text()')
        marke_value = text.xpath('//*[@id="historical-data"]/div/div[3]/table/tbody/tr/td[7]/text()')
        unit = 'USD'

        print response.url
        for i in range(len(timestamp)):
            self.data = self.parase_str_list(currency_id,timestamp[i],open_price[i],high_price[i],low_price[i],close_price[i],turnover_volume[i],marke_value[i],unit)
            yield self.data

    def parase_str_list(self,currency_id,timestamp,open_price,high_price,low_price,close_price,turnover_volume,marke_value,unit):
        data = HistoricalDataItem()
        timestamp1 = re.sub(u'\u5e74|\u6708|\u65e5','-',timestamp)
        time1 = time.strptime(timestamp1, '%Y-%m-%d-')
        publish_timestamp = int(time.mktime(time1))
        data['currency_id'] = currency_id
        data['publish_timestamp'] = int(publish_timestamp)
        data['open_price'] = float(open_price)
        data['high_price'] = float(high_price)
        data['low_price'] = float(low_price)
        data['close_price'] = float(close_price)
        if turnover_volume == '-':
            data['turnover_volume'] = None
            print 'aaaaaaaaaaaaaa'
        else:
            data['turnover_volume'] = int(turnover_volume)
        if marke_value == '-':
            print 'bbbbbbbbbbbbbb'
            data['marke_value'] = None
        else:
            data['marke_value'] = int(marke_value)
        data['unit'] = unit
        # print data['currency_id'],data['publish_timestamp'],data['open_price'],data['high_price'],data['low_price'],\
        #         data['close_price'],data['turnover_volume'],data['marke_value'],data['unit']
        return data