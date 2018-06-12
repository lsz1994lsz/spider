# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IndexDailyBulletinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 交易日
    trade_date = scrapy.Field()

    # 指数
    index = scrapy.Field()

    # 指数货币
    index_currency = scrapy.Field()

    # 全日最高
    daily_high = scrapy.Field()

    # 全日最低
    daily_low = scrapy.Field()

    # 指数收市
    index_close = scrapy.Field()

    # 点数变动
    point_change = scrapy.Field()

    # 百分比变动
    percent_change = scrapy.Field()

    # 周息率
    dividend_yield = scrapy.Field()

    # 市盈率
    pe_ratio = scrapy.Field()

    # 指数成交额（佰万元）
    index_turnover = scrapy.Field()

    # 市场成交额（佰万元）
    market_turnover = scrapy.Field()

    # 指数货币兑换港元汇率
    index_currency_to_hkd = scrapy.Field()

    #表类型
    table_type = scrapy.Field()

    pass
