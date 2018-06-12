# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BitcoinMarketsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 币种id 例如（bitcoin）
    currency_id = scrapy.Field()

    #市场id
    market_id = scrapy.Field()

    # 现价
    price = scrapy.Field()

    # 交易时间戳（毫秒）
    tradetime = scrapy.Field()

    # 24小时成交量
    volume_24h = scrapy.Field()

    # 交易量百分比（已转百分数的小数）
    valume_rate = scrapy.Field()

    # 配对单位（1代表美元、2代表人民币）
    unit = scrapy.Field()

    # 入库时间戳（毫秒）
    record_timestamp = scrapy.Field()

    #'可流通市值'（暂未使用）
    market_cap_by_available_supply = scrapy.Field()
    pass
