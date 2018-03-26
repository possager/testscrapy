import scrapy
from scrapy.spiders import Spider
from datetime import datetime


class spider2(Spider):
    name = 'spider2'
    start_urls = ['https://www.mala.cn/forum-60-{}.html'.format(str(i)) for i in range(1, 500)]

    def parse(self, response):
        print(response.url)

        dict1 = {
            'url': response.url,
            'content': str(response.body),
            'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'owner': response.url.split('-')[-1].split('.')[0]

        }
        return dict1