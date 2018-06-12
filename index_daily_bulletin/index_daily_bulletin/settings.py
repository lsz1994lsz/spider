# -*- coding: utf-8 -*-

# Scrapy settings for index_daily_bulletin project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'index_daily_bulletin'

SPIDER_MODULES = ['index_daily_bulletin.spiders']
NEWSPIDER_MODULE = 'index_daily_bulletin.spiders'
# ===============================
TELNETCONSOLE_PORT = 12345
WEBSERVICE_PORT = 54325
# ==============日志相关=================
# 自定义的日志，默认为ERROR，可用级别为：CRITICAL，ERROR，WARNING，INFO，DEBUG
CUSTOM_LOG_LEVEL = ['ERROR','INFO']
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'shareholding (+http://www.yourdomain.com)'
# ================piplines=======================
ITEM_PIPELINES = {
    'index_daily_bulletin.pipelines.IndexDailyBulletinPipeline': 600,
}
# ==================模拟真实===========================
#取消默认的useragent,使用新的useragent
# DOWNLOADER_MIDDLEWARES = {
#         'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,#关闭默认下载器
#         'agency_middlewares.JavaScriptMiddleware': 500,  # 键为中间件类的路径，值为中间件的顺序
# }
# 启用代理
ENABLE_PROXY = False
GET_PROXY_URL = "http://www.xdaili.cn/ipagent/greatRecharge/getGreatIp?spiderId=fa88b90f2a194d7cbd76b89795a2ee66&orderno=YZ2017815605yJ6Xxz&returnType=1&count=1"
# ==============oss相关==========================
SPIDER_MIDDLEWARES = {
    'oss_middlewares.OSSMiddleWares':150,
    'error_email.EmailSender': 500,
}
OSS_ACCESS_KEY_ID = 'iTXgd33xkJwEQ41U'
OSS_ACCESS_KEY_SECRET = 'fJ6oiBlMeRAEy8vuFzCIGhhNt1q9rx'
OSS_ENDPOINT = 'oss-cn-beijing.aliyuncs.com'
OSS_BUCKET = 'glh-spider'
# 网页编码
WEB_PAGE_ENCODING = 'utf16'
# =================邮件相关==========================
MAIL_HOST = "smtp.exmail.qq.com"  # 发送邮件的smtp服务器
MAIL_USER = "lsz@guruhk.com"  # 发件人的用户名/邮箱账号/收件人邮箱账号
MAIL_PASS  = "CmTpG4vH5UtWZYgA"  # 授权码

# ===============其他============================
# 下载延迟
DOWNLOAD_DELAY = 1
#请求失败重试
RETRY_ENABLED = True
#item条数显示刷新频率
LOGSTATS_INTERVAL = 120
# 下载超时
DOWNLOAD_TIMEOUT = 300

ROBOTSTXT_OBEY = False
# 对网站网站多少并发线程,启用CONCURRENT_REQUESTS_PER_IP此项不生效
# CONCURRENT_REQUESTS_PER_DOMAIN = 5
#对IP多少并发线程
CONCURRENT_REQUESTS_PER_IP = 1

HTTPERROR_ALLOWED_CODES = [404]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'index_daily_bulletin (+http://www.yourdomain.com)'
# 重定向
REDIRECT_ENABLED = False