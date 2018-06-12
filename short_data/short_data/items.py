# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShortDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    stock_code = scrapy.Field()

    #卖空成交量股数
    short_volume_shares = scrapy.Field()

    #卖空成交金额
    short_turnover_amount = scrapy.Field()

    #成交量股数
    turnover_volume_shares = scrapy.Field()

    #成交量金额
    turnover_amount = scrapy.Field()

    #交易日时间戳
    trade_date_timestamp = scrapy.Field()

    pass

