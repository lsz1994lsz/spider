# -*- coding: utf-8 -*-
import logging
from peewee import MySQLDatabase, Model, CharField, DateField, BooleanField, IntegerField,FloatField

# logger = logging.getLogger('peewee')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

test_db = MySQLDatabase('spiderdb',host='218.244.138.88', user='spiderdb', passwd='Cqmyg321', charset='utf8', port=13456)
online_db = MySQLDatabase('spiderdb',host = '114.215.177.242', user='spiderdb', passwd='Cqmyg321', charset='utf8', port = 3306)



class BaseModel(Model):
    class Meta:
        database = test_db

class ipv4(BaseModel):
    apnic = CharField(verbose_name='apnic', max_length=10, null=True, index=True,default=None)
    en = CharField(verbose_name='en', max_length=20, null=True, default=None)
    ipv4 = CharField(verbose_name='ipv4', max_length=50, null=True, unique=True,default=None)
    ip = CharField(verbose_name='ip', null=True, default=None)
    num = IntegerField(verbose_name='num', null=True, default=None)
    public_timestamp = IntegerField(verbose_name='public_timestamp', null=True,default=None)
    record_timestamp = IntegerField(verbose_name='record_timestamp', null=True,default=None)

class boc_exchange_rate(BaseModel):
    code = IntegerField(verbose_name='code',  null=True, index=True,default=None)
    en_name = CharField(verbose_name='en_name', max_length=255, null=True, default=None)
    cn_name = CharField(verbose_name='cn_name', max_length=255, null=True, default=None)
    exchange_rate = FloatField(verbose_name='exchange_rate', null=True, default=None)
    record_timestamp = IntegerField(verbose_name='record_timestamp', null=True,default=None)