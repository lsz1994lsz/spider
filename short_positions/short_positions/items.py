# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShortPositionItem(scrapy.Item):
    trade_date = scrapy.Field()
    stock_code = scrapy.Field()
    short_positions_shares = scrapy.Field()
    short_positions_amount = scrapy.Field()

    pass
