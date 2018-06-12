# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShareholdingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 股票代码
    stock_code = scrapy.Field()

    # 股票名
    stock_name = scrapy.Field()

    # 持股数量(股)
    positions_amount = scrapy.Field()

    # 股份百分比
    percent = scrapy.Field()

    # 日期
    shareholding_date = scrapy.Field()
    pass
