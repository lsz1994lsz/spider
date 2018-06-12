from time import sleep

from scrapy import cmdline
import sys
import os

sys.path.append(os.path.abspath('../public'))

cmdline.execute("scrapy crawl bishijie_kuaixun".split())
