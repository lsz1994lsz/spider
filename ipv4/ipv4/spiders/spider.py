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
from ipv4.items import Ipv4Item
from lxml import etree
from ..settings import *
import scrapy
from scrapy import log
from scrapy import Selector, Request
from scrapy.contrib.spiders import CrawlSpider

class Spider(CrawlSpider):
    CustomLog(CUSTOM_LOG_LEVEL)
    name = 'ipv4'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    }
    def start_requests(self):
        start_url_request_list = []
        url = 'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
        start_request = Request(url, callback=self.parse,headers=self.headers)
        start_url_request_list.append(start_request)
        return start_url_request_list

    def parse(self, response):
        body = str((response.body).decode(WEB_PAGE_ENCODING,'ignore')).encode('utf8')
        extract = re.findall('(apnic\|CN\|ipv4\|.*\|a.*d)', body)

        le = len(extract)
        if len(extract) > 0:
            for i in extract:
                i = i.split('|')
                if len(i) == 7:
                    self.data = self.parase_str_list(i[0],i[1],i[2],i[3],i[4],i[5],le)
                    yield self.data
        else:
            scrapy.log.msg("没有数据" , level=log.ERROR)

    def parase_str_list(self, apnic, en,ipv4,ip,num,public_date,le):
        data = Ipv4Item()
        #  ip
        data['apnic'] = apnic
        data['en'] = en
        data['ipv4'] = ipv4
        data['ip'] = ip
        data['num'] = num
        public_date_array = time.strptime(str(public_date),'%Y%m%d')
        public_timestamp = int(time.mktime(public_date_array))
        data['public_timestamp'] = public_timestamp
        data['len'] = le
        return data