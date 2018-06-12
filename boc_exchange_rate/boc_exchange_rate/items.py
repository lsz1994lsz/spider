# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BocExchangeRateItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #代码，1000=USD 美元 ，1100=HKD 港元，1160=JPY 日元，1210=MOP 澳门元，1220=MYR 马来西亚林吉特，1320=SGD 新加坡元，1420=CNY 人民币，1430=TWD 台湾元，3000=EUR 欧元，3030=GBP 英镑，5010=CAD 加拿大元，6010=AUD 澳大利亚元
    code = scrapy.Field()

    #英文简称
    en_name = scrapy.Field()

    #中文名
    cn_name = scrapy.Field()

    #对比人民币汇率（1当前货币比上1人民币汇率）
    exchange_rate = scrapy.Field()

    #插入时间(精度天，单位秒
    record_timestamp = scrapy.Field()
    pass
