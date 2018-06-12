# -*- coding: utf-8 -*-

# Scrapy settings for market_flow project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
# ==============日志相关=================
# 自定义的日志，默认为ERROR，可用级别为：CRITICAL，ERROR，WARNING，INFO，DEBUG
from market_flow.custom_log import CustomLog

CustomLog.log(['ERROR','WARNING','INFO'])
# 全局日志开关
# LOG_ENABLED = True
# 日志编码
# LOG_ENCODING = 'utf-8'
# 定义日志级别
LOG_LEVEL = 'INFO'
# LOG_LEVEL = 'WARNING'
# LOG_LEVEL = 'ERROR'
# 定义日志路径
# LOG_FILE =
# 记录Scrapy中的标准输出
# LOG_STDOUT = False
BOT_NAME = 'market_flow'

SPIDER_MODULES = ['market_flow.spiders']
NEWSPIDER_MODULE = 'market_flow.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'market_flow (+http://www.yourdomain.com)'

# LOG_FILE='logs/spider.log'
# LOG_FORMAT= '%(levelname)s %(asctime)s [%(name)s:%(module)s:%(funcName)s:%(lineno)s] [%(exc_info)s] %(message)s'


ITEM_PIPELINES = {
    'market_flow.pipelines.MarketFlowPipeline': 200
}
# =================邮件相关==========================
MAIL_HOST = "smtp.exmail.qq.com"  # 发送邮件的smtp服务器
MAIL_USER = "lsz@guruhk.com"  # 发件人的用户名/邮箱账号/收件人邮箱账号
MAIL_PASS  = "CmTpG4vH5UtWZYgA"  # 授权码


SPIDER_MIDDLEWARES = {
    'market_flow.error_email.EmailSender': 500,
}

