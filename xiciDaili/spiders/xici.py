# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
from scrapy.selector import Selector

from xiciDaili.items import XiciDailiItem


class proxySpider(scrapy.Spider):
    name = "xici"

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # 在这个位置请求下 清空数据库中代理数据相关操作

    allowed_domains = ["xicidaili.com", ]

    # 提取前边十条页面的数据
    def start_requests(self):
        start_url = 'http://www.xicidaili.com/nn/'
        for i in range(1, 11):
            request = scrapy.Request(url=start_url + str(i), callback=self.parse)
            request.meta['page'] = i
            yield request

    def parse(self, response):
        sel = Selector(response)
        page = response.meta['page']
        ip_list = sel.xpath('//*[@id="body"]/table/tr')
        items = []
        i = 0
        for ip in ip_list:
            if i == 0:
                i = i + 1
                pass
            else:
                pre_item = XiciDailiItem()
                pre_item['NUM'] = i
                pre_item['PAGE'] = page
                pre_item["IP"] = ip.xpath('string(td[2])').extract_first()
                port = ip.xpath('string(td[3])').extract_first()
                pre_item["PORT"] = port
                location = ip.xpath('string(td[4])').extract_first().strip()
                pre_item["POSITION"] = location
                proxy_type = ip.xpath('string(td[5])').extract_first()
                pre_item["TYPE"] = proxy_type
                speed = ip.xpath('td[8]/div/@title').re('\d{0,2}\.\d{0,}')
                pre_item["SPEED"] = float(speed[0])
                check_time = ip.xpath('string(td[10])').extract_first()
                pre_item["LAST_CHECK_TIME"] = check_time
                items.append(pre_item)
                i = i + 1
        return items
