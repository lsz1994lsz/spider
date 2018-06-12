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
from ..items import JinseItem
from lxml import etree
from ..settings import *
import scrapy
from scrapy import log
from scrapy import Selector, Request
from scrapy.contrib.spiders import CrawlSpider

class Spider(CrawlSpider):
    # CustomLog(CUSTOM_LOG_LEVEL)
    name = 'jinse'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    }
    def start_requests(self):
        start_url_request_list = []
        url = 'https://www.jinse.com/xinwen'
        # url = 'https://www.jinse.com/bitcoin/182883.html'
        start_request = Request(url, callback=self.parse,headers=self.headers)
        start_url_request_list.append(start_request)
        return start_url_request_list

    def parse(self, response):
        start_url_request_list = []
        news_text = []
        body = str((response.body).decode(WEB_PAGE_ENCODING,'ignore')).encode('utf8')
        text = etree.HTML(body)
        urls = text.xpath('//*[@id="app"]//ul/h3/a/@href')
        for i in urls:
            start_request = Request(i, callback=self.parse, headers=self.headers)
            start_url_request_list.append(start_request)
        title_xpath = text.xpath('//*[@id="app"]/div[1]/div/div[1]/div/div[1]/h2/text()')
        page = text.xpath('//*[@id="app"]/div[1]/div/div[1]/div/p[not(@style="text-align: center;")]/text()')
        # print title_xpath[0]
        for i in range(0,len(title_xpath)):
            for z in page:
                news_text.append(z)
            news_text1 = "".join(news_text)
            self.data = self.parase_str_list(title_xpath[i],news_text1)
            return self.data
        # for i in page:
        #     print i
        print response.url

        return start_url_request_list


    #
    # yield self.data
    #
    def parase_str_list(self, title,text):
        data = JinseItem()
        print title
        data['title'] = title
        data['text'] = text
        return data
        # print body