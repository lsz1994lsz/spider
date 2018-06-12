from scrapy import cmdline
import time
time.sleep(13)
cmdline.execute("scrapy crawl sz_spider".split())  #2