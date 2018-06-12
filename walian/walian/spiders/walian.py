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
from ..items import WalianItem
from lxml import etree
from ..settings import *
import scrapy
from scrapy import log
from scrapy import Selector, Request
from scrapy.contrib.spiders import CrawlSpider

class Spider(CrawlSpider):
    # CustomLog(CUSTOM_LOG_LEVEL)
    name = 'walian'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    }
    def start_requests(self):
        start_url_request_list = []
        url = 'https://www.walian.cn/'
        # url = 'https://www.walian.cn/news/1104.html'
        start_request = Request(url, callback=self.parse,headers=self.headers)
        start_url_request_list.append(start_request)
        return start_url_request_list

    def parse(self, response):
        start_url_request_list = []
        news_text = []
        body = str((response.body).decode(WEB_PAGE_ENCODING,'ignore')).encode('utf8')
        text = etree.HTML(body)
        # print body
        urls = text.xpath('//div [@class="el-tabs__content"]/div[1]/div [@class="articlelist"]/div/a [@class="c-block-tout__media"]/@href')

        for i in urls:
            url = 'https://www.walian.cn' + i
            start_request = Request(url, callback=self.parse, headers=self.headers)
            start_url_request_list.append(start_request)
        title_xpath = text.xpath('//*[@id="news"]/div/div/div[1]/div[1]/div/div[2]/text()')
        page = text.xpath('//*[@id="news"]/div/div/div[1]/div[1]/div/div[4]//p//text()')

        for i in range(0,len(title_xpath)):
            for z in page:
                news_text.append(z)
            news_text1 = "".join(news_text)
            print news_text1
            self.data = self.parase_str_list(str(title_xpath[i]).replace('\n',''),news_text1)
            return self.data

        print response.url

        return start_url_request_list


    #
    # yield self.data
    #
    def parase_str_list(self, title,text):
        data = WalianItem()
        print title
        data['title'] = title
        data['text'] = text
        return data
        # print body