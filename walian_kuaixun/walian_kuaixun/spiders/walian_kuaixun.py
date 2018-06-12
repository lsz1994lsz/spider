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
from ..items import WalianKuaixunItem
from lxml import etree
from ..settings import *
import scrapy
from scrapy import log
from scrapy import Selector, Request
from scrapy.contrib.spiders import CrawlSpider

class Spider(CrawlSpider):
    # CustomLog(CUSTOM_LOG_LEVEL)
    name = 'walian_kuaixun'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    }
    def start_requests(self):
        start_url_request_list = []
        run_time = 0
        # while run_time < 20:
        url = 'https://www.walian.cn/live'
            # run_time +=1
            # url = 'https://www.walian.cn/news/1104.html'
        start_request = Request(url, callback=self.parse,headers=self.headers,dont_filter=True)
        start_url_request_list.append(start_request)
        return start_url_request_list

    def parse(self, response):
        start_url_request_list = []
        news_text = []
        body = str((response.body).decode(WEB_PAGE_ENCODING,'ignore')).encode('utf8')
        text = etree.HTML(body)
        # print body
        # urls = text.xpath('//div [@class="el-tabs__content"]/div[1]/div [@class="articlelist"]/div/a [@class="c-block-tout__media"]/@href')
        #
        # for i in urls:
        #     url = 'https://www.walian.cn' + i
        #     start_request = Request(url, callback=self.parse, headers=self.headers)
        #     start_url_request_list.append(start_request)
        title_xpath = text.xpath('//*[@id="pane-tab0"]/ul/li/div/h4/text()')
        page = text.xpath('//*[@id="pane-tab0"]/ul/li/div/div[2]/text()')
        for i in range(0,len(title_xpath)):
            print title_xpath[i]
            print page[i]
            self.data = self.parase_str_list(str(title_xpath[i]).replace('\n',''),page[i])
            yield self.data

    def parase_str_list(self, title,text):
        data = WalianKuaixunItem()
        print title
        data['title'] = title
        data['text'] = text
        return data
