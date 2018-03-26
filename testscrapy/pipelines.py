# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json




class TestscrapyPipeline(object):
    def process_item(self, item, spider):
        basic_file='E:/scrapy_data/'
        if type(item)==type({}):

            with open(basic_file+spider.name+'/'+item['owner'],'w+') as fl:
                json.dump(item,fl)
