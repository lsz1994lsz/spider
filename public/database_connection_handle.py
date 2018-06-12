# -*- coding: utf-8 -*-

import json
import redis
import MySQLdb

class DatabaseConnectionHandle:


	def __init__(self):

		f = open("../public/online_db.json")
		config_json = json.load(f)

		self.redis_config = config_json['redis']
		self.mysql_config = config_json['mysql']


	def get_cache_redis_connectin(self):
		r = redis.Redis(host=self.redis_config["host"],port=self.redis_config['port'],db=self.redis_config['db'],password=self.redis_config['password'])
		return r



	def get_spider_connection(self):
		conn = MySQLdb.connect(
			host = self.mysql_config['host'],
			port = self.mysql_config['port'],
			user = self.mysql_config['user'],
			passwd = self.mysql_config['passwd'],
			db = self.mysql_config['db'],
		)

		return conn