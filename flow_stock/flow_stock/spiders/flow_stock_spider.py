# -*- coding: utf-8 -*-
import re

from scrapy.http import FormRequest
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector

from flow_stock.items import FlowStockItem

class StockFlowSpider(CrawlSpider):


	name = "flow_stock"

	base_params={
		'ACTIONID': '7' ,
		'AJAX':'AJAX-TRUE' ,
		'CATALOGID': 'SGT_GGTBDQD'
	}

	def start_requests(self):

		params = self.base_params

		#params['tab1PAGENO'] = '1'

		return [FormRequest("http://www.szse.cn/szseWeb/FrontController.szse",formdata=params,callback=self.parse)]



	def parse(self,response):

		sel = Selector(response)
		trade_date = ""
		span_list = sel.xpath("//span[@class='cls-subtitle']")
		if len(span_list) != 0:
			span = span_list[0]
			trade_date = span.xpath('text()').extract()

			
		response.meta['trade_date'] = trade_date


		self.parse_stock_code(response)

		page_td_list = sel.xpath("//td[@width='128px']")

		if len(page_td_list) != 0:
			page_str_list = page_td_list[0].xpath("text()").extract()

			page_str = page_str_list[0]
			
			page_str = page_str[-5:]

			page = re.findall("\d+",page_str)[0]

			page = int(page)

			i = 1
			while i <= page:

				params = self.base_params

				params['tab1PAGENO'] = str(i)
				
				yield FormRequest("http://www.szse.cn/szseWeb/FrontController.szse",meta={"trade_date":trade_date},formdata=params,callback=self.parse_stock_code)

				i += 1
		 
		





	def parse_stock_code(self,response):

		trade_date = response.meta['trade_date']
		sel = Selector(response)

		table_list = sel.xpath("//table[@id='REPORTID_tab1']")

		table = table_list[0]

		tr_list = table.xpath("tr")

		for tr in tr_list:
			td_list = tr.xpath('td')
			if len(td_list) == 3:
				td = td_list[0]

				stock_code = td.xpath('text()').extract()

				item = FlowStockItem()
				item['stock_code'] = stock_code[0]
				#item['trade_date'] = trade_date[0]

				yield item


