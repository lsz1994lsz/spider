# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MarketFlowItem(scrapy.Item):
    # define the fields for your item here like:
    quota_amount = scrapy.Field()
    unused_quota_amount = scrapy.Field()
    market_type = scrapy.Field()
    timestamp = scrapy.Field()
    balance = scrapy.Field()
    publish_time = scrapy.Field()
    publish_date = scrapy.Field()   
    publish_timestamp = scrapy.Field()
    inflow = scrapy.Field()
