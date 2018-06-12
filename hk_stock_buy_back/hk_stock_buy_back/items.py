# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HkStockBuyBackItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 股票代码
    stock_code = scrapy.Field()

    # 回购数量(股)

    buy_back_amount = scrapy.Field()

    #最高回购价
    highest_buy_back_price = scrapy.Field()

    # 最低回购价
    minimum_buy_back_price = scrapy.Field()

    # 回购平均价
    average_buy_back_price = scrapy.Field()

    # 回购总额(港元)
    buy_back_total = scrapy.Field()

    # 发布日期
    trade_date_timestamp = scrapy.Field()

    pass
