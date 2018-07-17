# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
import platform



class TestscrapyPipeline(object):
    def process_item(self, item, spider):
        basic_file='E:/scrapy_data/'
        if platform.system()=='Linux':
            # basic_file='/media/liang/Data/scrapy_data/'
            basic_file='/media/liang/办公/Data/datascrapy/'
        if type(item)==type({}):
            if not os.path.exists(basic_file+spider.name):
                os.makedirs(basic_file+spider.name)

            with open(basic_file+spider.name+'/'+item['owner'],'w+') as fl:
                json.dump(item,fl)
