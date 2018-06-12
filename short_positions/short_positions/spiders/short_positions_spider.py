# -*- coding: utf-8 -*-
import StringIO
import datetime
import time
import sys

from custom_log_v2 import CustomLog

from ..settings import *

reload(sys)
sys.setdefaultencoding('utf8')
from time import mktime


from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import  Request

from short_positions.items import ShortPositionItem


class ShortDataSpider(CrawlSpider):
	CustomLog(CUSTOM_LOG_LEVEL)
	name = "short_positions"


	def start_requests(self):
		start_url_request_list = []
		i = 0
		while i <= RUN_TIME:

			url = "http://www.sfc.hk/web/TC/pdf/spr/#{date_}/Short_Position_Reporting_Aggregated_Data_#{date}.csv"

			trade_date_timestamp = datetime.datetime.now() - datetime.timedelta(days=i)
			year = trade_date_timestamp.strftime("%Y")

			month = trade_date_timestamp.strftime("%m")
			day = trade_date_timestamp.strftime("%d")

			date_str = year + month + day
			
			date_str_long = year + '/' + month + '/' + day

			url = url.replace("#{date}",date_str)
			url = url.replace("#{date_}",date_str_long)

			start_request = Request(url, callback=self.parse , meta={'trade_date_timestamp': trade_date_timestamp})
			start_url_request_list.append(start_request)
			i += 1


		return start_url_request_list
		

		


	def parse(self,response):

		body = response.body

		trade_date_timestamp = response.meta['trade_date_timestamp']

		parase_content = body.replace("Date,Stock Code,Stock Name,Aggregated Reportable Short Positions (Shares),Aggregated Reportable Short Positions (HK$)","")

		buf = StringIO.StringIO(parase_content)

		line = buf.readline()

		flag = True
		i = 0


		while 1:

			short_position = self.parse_line(line)

			yield short_position
			i += 1

			'''short_data = self.parse_line(line)

			if short_data != None:

				stock_code = short_data['stock_code']

				short_data['trade_date_timestamp'] = trade_date_timestamp

				if len(stock_code) < 4:
					yield short_data
				else:
					if stock_code[:1] != '%' and stock_code[:1] != '7':
						yield short_data'''

			line = buf.readline()
			if not line:
				break


	def parse_line(self,line):

		str_list = line.split(",")

		short_postions = self.parase_str_list(str_list)

		return short_postions


	def parase_str_list(self,str_list):

		short_postions = ShortPositionItem()
		point = 0
		for text in str_list:

			if point == 0:
				short_postions['trade_date'] = text.replace("\n","").replace("\r","")

			if point == 1:
				short_postions['stock_code'] = text.replace("\n","").replace("\r","")

			if point == 3:
				short_postions['short_positions_shares'] = text.replace("\n","").replace("\r","")

			if point == 4:
				short_postions['short_positions_amount'] = text.replace("\n","").replace("\r","")

			point += 1

		return short_postions



	def __get_trade_date_timestamp(self,date_str):

		year = date_str[:2]
		month = date_str[2:4]
		day = date_str[4:6]

		year = str(20) + year 

		trade_date = year + "-" + month + "-" + day

		trade_date = datetime.datetime.strptime(trade_date, "%Y-%m-%d")

		trade_date = trade_date - datetime.timedelta(days=0)

		trade_date_timestamp = time.mktime(trade_date.timetuple())

		return trade_date_timestamp
