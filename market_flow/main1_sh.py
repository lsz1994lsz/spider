from scrapy import cmdline
import time
time.sleep(10)
cmdline.execute("scrapy crawl sh_spider".split())   #1