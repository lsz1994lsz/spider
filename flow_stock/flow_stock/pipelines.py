# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import time
import datetime
import MySQLdb

class FlowStockPipeline(object):

	'''__add_status = 1
	__update_status = 2
	__delete_status = 3'''

	def __init__(self):


		f = open("config/db.json")

		config_json = json.load(f)

		redis_config = config_json['redis']
		mysql_config = config_json['mysql']

		#self.r = redis.Redis(host=redis_config["host"],port=redis_config['port'],db=redis_config['db'],password=redis_config['password'])

		self.conn = MySQLdb.connect(
			host = mysql_config['host'],
			port = mysql_config['port'],
			user = mysql_config['user'],
			passwd = mysql_config['passwd'],
			db = mysql_config['db']
		)


	def process_item(self, item, spider):

		'''stock_status = self.get_stock_status(item['stock_code'])

		stock = {}
		stock['stock_code'] = item['stock_code']'''

		self.save_to_mysql(item)

		return item



	'''def save_item_to_redis(self,stock):

		flow_stock_redis_key = self.get_redis_key(item)

		self.r.hset(flow_stock_redis_key,'status',status)



	def get_redis_key(self,stock_code):

		key = "flow-stock:cache:" + "hk" + stock_code

		return key


	def get_stock_status(self,stock_code):
		key = self.get_redis_key()
		json_str = self.r.get(key)

		if json_str == "":
			return self.__add_status

		else:
			return self.__update_status'''


	def save_to_mysql(self,item):

		cur = self.conn.cursor()

		stock_type = "hk"
		#trade_date_timestamp = time.mktime(time.strptime(item['trade_date'],'%Y-%m-%d'))
		trade_date_timestamp = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
		trade_date_timestamp = trade_date_timestamp.strftime("%Y-%m-%d")

		#trade_date_timestamp = trade_date_timestamp[:10]

		trade_date_timestamp = time.mktime(time.strptime(trade_date_timestamp,'%Y-%m-%d'))

		print trade_date_timestamp

		sql = "insert into spider_flow_stock(`stock_type` , `stock_code`, `trade_date_timestamp` ) values(%s,%s,%s)" 

		result = cur.execute(sql,( stock_type,item['stock_code'], trade_date_timestamp)) 

		self.conn.commit()


	#关闭操作
	def spider_closed(self, spider):
		self.r.close()
		self.conn.close()

