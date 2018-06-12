# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request, FormRequest

from market_flow.items import MarketFlowItem
from market_flow.util import Util
import scrapy
from scrapy import log

class HKSZSpideri(CrawlSpider):
    name = 'hk_sz_spider'



    def start_requests(self):
        #return [Request("https://www.szse.cn/szseWeb/FrontController.szse" , callback = self.post_login)]  #添加了meta
	return 	[FormRequest("http://www.szse.cn/szseWeb/FrontController.szse",formdata={'ACTIONID': 'sgtSsedQuery'},callback=self.parse)]

    def parse(self,response):
	body = response.body

	year = body[:4]
	month = body[5:7]
	day = body[8:10]

	publish_date = day + '/' + month + '/' + year

	space = body.index(' ')
	#第一个||的位置
	first_symbol = body.index('||')
	publish_time = body[space+1:first_symbol]	

	
	quota_amount_plus_str = body[first_symbol+2:]
	#第二个||所在的位置
	second_symbol = quota_amount_plus_str.index('||') + first_symbol + 2
	quota_amount_str = body[first_symbol+2:second_symbol]
	quota_amount_float = float(quota_amount_str)
	quota_amount = int(quota_amount_float * 100)

	balance_plus_str = body[second_symbol+2:]
	
	third_symbol = balance_plus_str.index('||') + second_symbol + 2
	#balance_str = body[second_symbol+2:third_symbol]
	#balance = round(float(balance_str))


	unused_quota_amount_str = body[third_symbol+2 : ]
	balance = round(float(unused_quota_amount_str))

	item = MarketFlowItem()

	timestamp = str(time.time())
	index = timestamp.index('.')
	timestamp = timestamp[:index]

	inflow = quota_amount - balance 

	item['quota_amount'] = quota_amount
	item['balance'] = balance
	#item['unused_quota_amount'] = unused_quota_amount
	item['timestamp'] = timestamp
	item['market_type'] = 4
	item['publish_time'] = publish_time
	item['publish_date'] = publish_date
	item['inflow'] = inflow
	print publish_time + '||' + str(balance) + '||' + str(inflow)+ '||' + str(quota_amount) + '||' + timestamp + '||' + publish_date

	scrapy.log.msg(str(4)+ '     ' + str(quota_amount) + '—' + str(balance) + '—' + str(inflow) + '   ||' + publish_date + '-' + publish_time + '||' + timestamp, level=log.WARNING)
	yield item 

	


