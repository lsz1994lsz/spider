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

class SHSpider(scrapy.Spider):
    name = "sh_spider"
    start_urls = [
        "http://www.hkex.com.hk/chi/csm/script/data_NBSH_QuotaUsage_chi.js"
    ]


    def parse(self,response):

        body = response.body
	
	print body
	'''patternStr = '.*, "RMB([^ ]+) Mil.*' 
        p = re.compile(patternStr,re.DOTALL)
	m = p.match(body)
        #m = re.match(p,body)'''

	balanceStr = Util.getMidContent(', "RMB' , ' Mil' , body)
	balance = balanceStr.strip().lstrip().replace(',','')
	
	quota_amount = 13000
	inflow = quota_amount - int(balance) 

	timestamp = str(time.time())
	index = timestamp.index('.')
	timestamp = timestamp[:index]
	publish_time = self.getMidContent('餘額 \(於 ' , '\)' , body)	
	publish_date_str = self.getMidContent('每日額度", "' , '", {}],' , body)	
	publish_date = publish_date_str[0:10]

	item = MarketFlowItem()

	item['quota_amount'] = quota_amount 
	item['balance'] = balance
	#item['unused_quota_amount'] = unused_quota_amount
	item['inflow'] = inflow
	item['timestamp'] = timestamp
	item['market_type'] = 1
	item['publish_time'] = publish_time
	item['publish_date'] = publish_date
	print publish_time + '||' + balance + '||' + str(inflow) + '||' + str(quota_amount) + '||' + timestamp + '||' + publish_date

	scrapy.log.msg(str(1)+ '     ' + str(quota_amount) + '—' + balance + '—' + str(inflow) + '     ||' + publish_date + '-' + publish_time + '||' + timestamp, level=log.WARNING)
	yield item
	
  
		

        '''if m:
	    item = MarketFlowItem()
	    balanceStr = m.group(1)
	    balance = balanceStr.strip().lstrip().replace(',','')   
	    quota_amount = 13000
	    unused_quota_amount = quota_amount 

	    timestamp = str(time.time())
	    index = timestamp.index('.')
	    timestamp = timestamp[:index]

	    item['quota_amount'] = quota_amount 
	    item['balance'] = balance
	    item['unused_quota_amount'] = unused_quota_amount
	    item['timestamp'] = timestamp
	    item['market_type'] = 1
	    item['publish_time'] = '12:01'
	    
	    yield item
	'''     
	    
       
	


    def getMidContent(self,startStr , endStr , text):
	patternStr = '.*"%s(.*)%s.*' % (startStr,endStr)
	print 'patternStr :' + patternStr
        p = re.compile(patternStr,re.DOTALL)
	m = p.match(text)

	if m:
	    return m.group(1)
	else:
	    return None







	



