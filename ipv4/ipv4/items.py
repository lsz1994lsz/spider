# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Ipv4Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #第一列
    apnic = scrapy.Field()

    #第二列
    en = scrapy.Field()

    #第三列
    ipv4 = scrapy.Field()

    #第四列
    ip = scrapy.Field()

    #第五列
    num = scrapy.Field()

    # 公布时间戳
    public_timestamp = scrapy.Field()

    # 入库时间戳
    record_timestamp = scrapy.Field()

    #数据长度
    len = scrapy.Field()
    pass

