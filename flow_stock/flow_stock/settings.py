# -*- coding: utf-8 -*-

# Scrapy settings for flow_stock project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'flow_stock'

SPIDER_MODULES = ['flow_stock.spiders']
NEWSPIDER_MODULE = 'flow_stock.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'flow_stock (+http://www.yourdomain.com)'



ITEM_PIPELINES = {
    'flow_stock.pipelines.FlowStockPipeline': 300,
}