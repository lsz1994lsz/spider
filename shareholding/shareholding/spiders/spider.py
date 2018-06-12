# coding:utf-8
import re
import datetime
import time
import sys

from custom_log_v2 import CustomLog

reload(sys)
sys.setdefaultencoding('utf8')
from time import mktime
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from shareholding.items import ShareholdingItem
from lxml import etree
from ..settings import *


class Spider(CrawlSpider):
    CustomLog(CUSTOM_LOG_LEVEL)
    name = 'shareholding'

    def start_requests(self):
        start_url_request_list = []

        url = "http://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=hk"
        start_request = Request(url, callback=self.parse)
        start_url_request_list.append(start_request)

        return start_url_request_list

    def parse(self, response):
        body = (response.body).decode(WEB_PAGE_ENCODING,'ignore')
        html = etree.HTML(body)
        code = html.xpath('//table//tr[starts-with(@class,"row")]')
        dates = html.xpath('//*[@id="pnlResult"]/div[1]/text()')

        if not dates == []:

            publish_dates = re.findall('(\d+/\d+/\d+)', dates[0])


            for each in code:
                data = each.xpath('td/text() ')

                positions_record_data = self.parase_str_list(data,publish_dates)
                yield positions_record_data



    def parase_str_list(self, data,publish_dates):
        positions_record_data = ShareholdingItem()
        if data[0] != None:
            positions_record_data['stock_code'] = re.sub('[( ),(\\r),(\\n)]', '',data[0])

        if data[1] != None:
            positions_record_data['stock_name'] = re.sub('[( ),(\\r),(\\n)]', '',data[1])

        if data[2] != None:
            positions_record_data['positions_amount'] = re.sub('[( ),(\\r),(\\n)]', '',data[2])

        if data[3] != None:
            positions_record_data['percent'] = re.sub('[( ),(\\r),(\\n)]', '',data[3])

        if publish_dates[0] != None:
            positions_record_data['shareholding_date'] =  re.sub('/', '-',publish_dates[0])
            print positions_record_data['shareholding_date']


        return positions_record_data