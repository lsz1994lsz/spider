# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import MySQLdb
import traceback
import logging
import time


class MarketFlowPipeline(object):
    logger = logging.getLogger()

    def process_item(self, item, spider):
	# self.dbpool = adbapi.ConnectionPool('MySQLdb', db='moive_get',user='lin', passwd='linhongbin', cursorclass=MySQLdb.cursors.DictCursor,charset='utf8', use_unicode=True)
	host = '114.215.177.242'
	port = '3306'
	dbName = 'spiderdb'
	user = 'spiderdb'
	password = 'Cqmyg321'
	charset = 'utf8'
	conn = MySQLdb.connect(host=host,user=user,passwd=password,db=dbName,port=int(port),charset=charset)
	# host = '218.244.138.88'
	# port = '13456'
	# dbName = 'spiderdb'
	# user = 'spiderdb'
	# password = 'Cqmyg321'
	# charset = 'utf8'
	# conn = MySQLdb.connect(host=host,user=user,passwd=password,db=dbName,port=int(port),charset=charset)



	try:
	    cur = conn.cursor()
	    flag = self.isExist(cur , item)
	    if not flag:

		#计算发布时的时间戳
		publish_detail_time = item['publish_date']+ ' ' + item['publish_time'] 
		publish_timestamp = time.mktime(time.strptime(publish_detail_time,'%d/%m/%Y %H:%M'))
		
		item['publish_timestamp'] = publish_timestamp
		
                sql = "insert into spider_market_flow_2(QUOTA_AMOUNT, INFLOW , MARKET_TYPE , TIMESTAMP , BALANCE , PUBLISH_TIME , PUBLISH_DATE , PUBLISH_TIMESTAMP) value (%s,%s,%s,%s,%s,%s,%s ,%s)"
                result = cur.execute(sql,( item['quota_amount'],item['inflow'], item['market_type'], item['timestamp'], item['balance'] , item['publish_time'] , item['publish_date'] , item['publish_timestamp']))
                conn.commit()
	    else:
		self.logger.info('data has been exist! market_type:' + str(item['market_type']) + ","  + item['publish_time'] )


	except Exception,e:
	    traceback.print_exc()
	    #print Exception,":",e
	    self.logger.info( str(Exception),":",e  )
	
	cur.close()
	conn.close()
        return item






    def isExist(self,cur , item):
	
	sql = "select id from spider_market_flow_2 where PUBLISH_TIME = %s and MARKET_TYPE = %s and PUBLISH_DATE = %s"  

        cur.execute(sql,( item['publish_time'] , item['market_type'] , item['publish_date'] ))

	print sql %( item['publish_time'] , item['market_type'] ,  item['publish_date'] )

	result = cur.fetchall()
	
	
	if len(result) <= 0:
	    print 'result:false'
	    return False
	else:
	    print 'result:true'
	    return True
