# -*- coding: UTF-8 -*-
import re
import datetime
import time
import sys
from custom_log_v2 import CustomLog
# reload(sys)
# sys.setdefaultencoding('gbk')
from time import mktime
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import BishijieKuaixunItem
from lxml import etree
from ..settings import *
import scrapy
from scrapy import log
from scrapy import Selector, Request
from scrapy.contrib.spiders import CrawlSpider

class Spider(CrawlSpider):
    # CustomLog(CUSTOM_LOG_LEVEL)
    name = 'bishijie_kuaixun'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
        "content-type:text/html; charset=utf-8"
    }
    def start_requests(self):
        start_url_request_list = []
        run_time = 0
        # while run_time < 20:
        url = 'http://www.bishijie.com/kuaixun'
            # run_time +=1
            # url = 'https://www.walian.cn/news/1104.html'
        start_request = Request(url, callback=self.parse,headers=self.headers,dont_filter=True)
        start_url_request_list.append(start_request)
        return start_url_request_list

    def parse(self, response):
        body = response.body.decode(response.encoding)
        body = re.sub('<br />','',body)
        # body = str(response.body).decode(response.encoding,'ignore')
        text = etree.HTML(body)
        kx_title = text.xpath('//ul/li[1]/a/h2/text()')
        # kx_body = re.findall('</h2><div>(.*?)</div>',body)

        kx_body = text.xpath('//ul/li[1]/a/div/text()')

        print len(kx_title),len(kx_body)
        if len(kx_title) == len(kx_body) == 100:
            for i in range(0,len(kx_title)):
                print kx_title[i]
                print kx_body[i]#title_xpath[i]
                print '================================='
                self.data = self.parase_str_list(str(kx_title[i]).replace('\n',''),kx_body[i])
                yield self.data

    def parase_str_list(self, title,text):
        data = BishijieKuaixunItem()
        print title
        data['title'] = title
        data['text'] = text
        return data
