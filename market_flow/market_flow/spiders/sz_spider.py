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


class SZSpider(scrapy.Spider):
    name = "sz_spider"

    start_urls = {
	"http://sc.hkex.com.hk/TuniS/www.hkex.com.hk/chi/csm/script/data_NBSZ_QuotaUsage_chi.js"
    }




    def parse(self,response):
	
	body = response.body

 	print body
	balanceStr = Util.getMidContent('RMB' , ' Mil' , body)
	balance = balanceStr.strip().lstrip().replace(',','')
	quota_amount = 13000
	inflow = quota_amount - int(balance)
	timestamp = str(time.time())

	index = timestamp.index('.')
	timestamp = timestamp[:index]
	
	publish_time = Util.getMidContent('余额 \(于 ' , '\)", "RMB' , body)
	publish_date_Str = Util.getMidContent('每日额度", "' , '", {}],' , body)	
	publis_date = publish_date_Str[0:10]
	
	item = MarketFlowItem()

	item['quota_amount'] = quota_amount 
	item['balance'] = balance
	#item['unused_quota_amount'] = unused_quota_amount
	item['timestamp'] = timestamp
	item['market_type'] = 2
	item['publish_time'] = publish_time
	item['publish_date'] = publish_date_Str[0:10]
	item['inflow'] = inflow
	print publish_time + '||' + balance + '||' + str(inflow) + '||' + str(quota_amount) + '||' + timestamp + '||' + publish_date_Str[0:10]
	scrapy.log.msg(str(2)+ '     ' + str(quota_amount) + '—' + balance + '—' + str(inflow) + '     ||' + publish_date_Str[0:10] + '-' + publish_time + '||' + timestamp , level=log.WARNING)
	yield item
