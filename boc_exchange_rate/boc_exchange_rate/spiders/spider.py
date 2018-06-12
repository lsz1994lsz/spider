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
from boc_exchange_rate.items import BocExchangeRateItem
from lxml import etree
from ..settings import *
import scrapy
from scrapy import log
from scrapy import Selector, Request
from scrapy.contrib.spiders import CrawlSpider

class Spider(CrawlSpider):
    CustomLog(CUSTOM_LOG_LEVEL)
    name = 'boc_exchange_rate'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    }
    def start_requests(self):
        start_url_request_list = []
        url = 'http://data.bank.hexun.com/other/cms/foreignexchangejson.ashx?callback=ShowDatalist'
        start_request = Request(url, callback=self.parse,headers=self.headers)
        start_url_request_list.append(start_request)
        return start_url_request_list

    def parse(self, response):
        body = str((response.body).decode(WEB_PAGE_ENCODING,'ignore')).encode('utf8')
        all_tate = re.findall("{bank:'中国银行',currency:'(美元|日元|欧元|英镑|澳大利亚元|加拿大元|瑞士法郎|港币|新台币|韩元|泰国铢|澳门元|林吉特|卢布|南非兰特|新西兰元|菲律宾比索|新加坡元|瑞典克朗|丹麦克朗|挪威克朗)',code:'([A-Z]*)',currencyUnit:'.*?',cenPrice:'(.*?)',",body)
        hk_cny_rate = z = re.findall("{bank:'中国银行',currency:'(港币)',code:'([A-Z]*)',currencyUnit:'.*?',cenPrice:'(.*?)',",body)
        cny_100hk_rate = 1/float(hk_cny_rate[0][2])
        # all_tate2 = list(all_tate)
        # print all_tate2
        for i in all_tate:
            li = list(i)
            if i[0] == '港币':
                cn_name = '人民币'
                en_name = 'CNY'
                exchange_rate = cny_100hk_rate*100
                self.data = self.parase_str_list(cn_name, en_name, exchange_rate)
            else:
                cn_name = li[0]
                en_name = li[1]
                exchange_rate = cny_100hk_rate*float(li[2])
                self.data = self.parase_str_list(cn_name, en_name, exchange_rate)
            yield self.data


    def parase_str_list(self,cn_name,en_name,exchange_rate):
        data = BocExchangeRateItem()
        code = self.code(en_name)
        data['code'] = code
        data['cn_name'] = cn_name
        data['en_name'] = en_name
        data['exchange_rate'] = exchange_rate
        return data

    def code(self, en_name):
        if en_name == 'USD':
            code = 1000
            return code
        if en_name == 'CNY':
            code = 1420
            return code
        if en_name == 'JPY':
            code = 1160
            return code
        if en_name == 'MOP':
            code = 1210
            return code
        if en_name == 'MYR':
            code = 1220
            return code
        if en_name == 'SGD':
            code = 1320
            return code
        if en_name == 'CNY':
            code = 1420
            return code
        if en_name == 'TWD':
            code = 1430
            return code
        if en_name == 'EUR':
            code = 3000
            return code
        if en_name == 'GBP':
            code = 3030
            return code
        if en_name == 'CAD':
            code = 5010
            return code
        if en_name == 'AUD':
            code = 6010
            return code

        if en_name == 'PHP':
            code = 1290
            return code
        if en_name == 'KRW':
            code = 1330
            return code
        if en_name == 'THB':
            code = 1360
            return code
        if en_name == 'DKK':
            code = 3020
            return code
        if en_name == 'NOK':
            code = 3260
            return code
        if en_name == 'SEK':
            code = 3300
            return code
        if en_name == 'CHF':
            code = 3310
            return code
        if en_name == 'NZD':
            code = 6090
            return code
        if en_name == 'ZAR':
            code = 7113
            return code
        if en_name == 'RUB':
            code = 3440
            return code