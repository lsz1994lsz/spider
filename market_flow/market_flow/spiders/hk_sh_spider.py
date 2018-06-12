# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re
import scrapy
from scrapy import log
import time

from market_flow.items import MarketFlowItem 
from market_flow.util import Util

class HKSHSpider(scrapy.Spider):
    name = "hk_sh_spider"
    
    start_urls = [ 
	"http://www.sse.com.cn/js/common/hgtedxx/dailyinfo.js"
    ]


    def parse(self,response):

	body = response.body

	quota_amount = Util.getMidContent('daily_amt:"' , '",day_unused:' , body)
	
	
	balance = Util.getMidContent( 'day_unused:"' , '",mktstatus_first:' , body) 

	timestamp = str(time.time())
	index = timestamp.index('.')
	timestamp = timestamp[:index]

	#balance = int(quota_amount) - int( unused_quota_amount)
	
	publish_time_str = Util.getMidContent('create_time:"' , '"};' , body)
	
	space = publish_time_str.find(' ')
	publish_time = publish_time_str[space+1: ]

	publish_date_str = publish_time_str[:space]
	year = publish_date_str[:4]
	month = publish_date_str[5:7]
	day = publish_date_str[8:]
	publish_date = day + '/' + month + '/' + year

	item = MarketFlowItem()

	inflow = int(quota_amount) - int( balance)

	item['quota_amount'] = quota_amount
	item['balance'] = balance
	#item['unused_quota_amount'] = unused_quota_amount
	item['timestamp'] = timestamp
	item['market_type'] = 3
	item['publish_time'] = publish_time
	item['publish_date'] = publish_date
	item['inflow'] = inflow
	print publish_time + '||' + balance + '||' + str(inflow) + '||' + quota_amount + '||' + timestamp + '||' + publish_date
	scrapy.log.msg(str(3) + '     ' + quota_amount + '—' + balance + '—' + str(inflow) + '      ||' + publish_date + '-' + publish_time + ' ||' + timestamp, level=log.WARNING)
	yield item	
