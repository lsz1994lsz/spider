# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HistoricalDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 币种id 例如（bitcoin）
    currency_id = scrapy.Field()

    # 日期时间戳（毫秒）
    publish_timestamp = scrapy.Field()

    # 开盘价
    open_price = scrapy.Field()

    # 最高价
    high_price = scrapy.Field()

    # 最低价
    low_price = scrapy.Field()

    # 收盘价
    close_price = scrapy.Field()

    #成交量
    turnover_volume = scrapy.Field()

    # 市值
    marke_value = scrapy.Field()

    # 配对单位（USD、CNY）
    unit = scrapy.Field()

    # 入库时间戳（毫秒）
    update_time = scrapy.Field()

