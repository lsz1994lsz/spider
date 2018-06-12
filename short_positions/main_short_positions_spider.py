import os
from scrapy import cmdline
import sys

sys.path.append(os.path.abspath('../public'))
cmdline.execute("scrapy crawl short_positions".split())