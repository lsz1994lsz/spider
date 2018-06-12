# -*- coding: UTF-8 -*-
import re
import datetime
import time
import sys
from custom_log_v2 import CustomLog
# reload(sys)
# sys.setdefaultencoding('gbk')
from time import mktime
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import BitcoinMarketsItem
from lxml import etree
from ..settings import *
import scrapy
from scrapy import log
from scrapy import Selector, Request
from scrapy.contrib.spiders import CrawlSpider

class Spider(CrawlSpider):
    # CustomLog(CUSTOM_LOG_LEVEL)
    name = 'bitcoin_markets'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
        "content-type:text/html; charset=utf-8"
    }
    def start_requests(self):
        start_url_request_list = []
        self.name_list = ['bitcoin','ethereum','ripple','bitcoin-cash','eos','cardano','litecoin','stellar','tron','neo']
        self.run_time = 0
        self.a = []
        while self.run_time < 10:
            url = 'https://coinmarketcap.com/currencies/' + self.name_list[self.run_time] +'/#markets'
            self.run_time +=1
            # url = 'https://www.walian.cn/news/1104.html'
            start_request = Request(url, callback=self.parse,headers=self.headers,dont_filter=True)
            start_url_request_list.append(start_request)
        return start_url_request_list

    def parse(self, response):
        body = response.body.decode(response.encoding)
        body = re.sub(r'<br />|\n|\$|,','',body)
        # body = str(response.body).decode(response.encoding,'ignore')
        text = etree.HTML(body)
        market = text.xpath('//*[@id="markets-table"]/tbody/tr/td[2]/a/text()')
        unit = text.xpath('//*[@id="markets-table"]/tbody/tr/td[3]/a/text()')
        volume_24h = text.xpath('//*[@id="markets-table"]/tbody/tr/td[4]/span/text()')
        price = text.xpath('//*[@id="markets-table"]/tbody/tr/td[5]/span/text()')
        valume_rate = text.xpath('//*[@id="markets-table"]/tbody/tr/td[6]/span/text()')

        print response.url
        currency_id = re.findall(r'https://coinmarketcap.com/currencies/(.*)/',response.url)[0]
        for i in range(0,len(unit)):
            if unit[i][-4:] in ['/USD','/CNY']:
                tradetime = int(round(time.time() * 1000))
                # print currency_id,market[i],price[i],tradetime,volume_24h[i],valume_rate[i],unit[i]

# 获取所有market
#                 self.a.append(market[i])
#         self.run_time -= 1
#         if self.run_time == 0:
#             ids = set(self.a)
#             for i in ids:
#                 print i
# #             print ids
#             print len(ids)
#             print 1

                self.data = self.parase_str_list(currency_id,market[i],price[i],tradetime,volume_24h[i],valume_rate[i],unit[i])
                yield self.data

    def parase_str_list(self,currency_id,market,price,tradetime,volume_24h,valume_rate,unit):
        data = BitcoinMarketsItem()
        market_list = ['Livecoin',
        'Stellar Decentralized Exchange',
        'GDAX',
        'Ripple China',
        'Ore.Bz',
        'Neraex',
        'Bitstamp',
        'BitFlip',
        'BitKonan',
        'YoBit',
        'COSS',
        'xBTCe',
        'TOPBTC',
        'LakeBTC',
        'Omicrex',
        'RippleFox',
        'OkCoin Intl.',
        'Lykke Exchange',
        'Waves Decentralized Exchange',
        'Simex',
        'Coinsuper',
        'Exmo',
        'Fatbtc',
        'Exrates',
        'BitMEX',
        'Gatehub',
        'Mr. Exchange',
        'Abucoins',
        'Octaex',
        'C-CEX',
        'DSX',
        'Coinroom',
        'Bittylicious',
        'Bitfinex',
        'Kraken',
        'CoinsBank',
        'Bitstamp (Ripple Gateway)',
        'OKCoin.cn',
        'BTCC',
        'Sistemkoin',
        'WEX',
        'Bitsane',
        'Bitinka',
        'OEX',
        'BTC-Alpha',
        'Coinut',
        'BitBay',
        'Gemini',
        'Gatecoin',
        'SouthXchange',
        'Bitlish',
        'Coinhub',
        'CRXzone',
        'Quoine',
        'CEX.IO',
        'itBit',
        'Ethfinex'
        ]
        if market in market_list:
            data['market_id'] = market_list.index(market) + 1
            data['currency_id'] = currency_id
            data['price'] = float(price)
            data['tradetime'] = tradetime
            data['volume_24h'] = int(volume_24h)
            data['valume_rate'] = valume_rate
            if unit[-4:] == '/USD':
                data['unit'] = 1
            else:
                data['unit'] = 2
            print data['currency_id'],data['market_id'],data['price'],data['tradetime'],data['volume_24h'],data['valume_rate'],data['unit']
            print '-------------------------'
            return data