# -*- coding: utf-8 -*-
import scrapy
import re
from doubanbook.items import DoubanbookItem

class DbbookSpider(scrapy.Spider):
    name = "dbbooktag"
    #allowed_domains = ["https://www.douban.com/doulist/1264675/"]
    tag = "大数据"
    start_urls = (
        'https://book.douban.com/tag/'+tag,
    )
    URL = 'https://book.douban.com/tag/'+tag+'/?start=PAGE&sort=seq&sub_type='
    def parse(self, response):
        #print response.body
        item = DoubanbookItem()
        selector = scrapy.Selector(response)
        books = selector.xpath('//li[@class="subject-item"]/div[@class="info"]')
        for each in books:
            title = each.xpath('h2/a/text()').extract()[0]
            #rate = each.xpath('div[@class="star clearfix"]/span[@class="rating_nums"]/text()').extract()[0]
            rateXpath = each.xpath('div[@class="star clearfix"]/span[@class="rating_nums"]/text()')
            if rateXpath.__len__() == 1:
                rate = each.xpath('div[@class="star clearfix"]/span[@class="rating_nums"]/text()').extract()[0];
            else:
                rate = "";

            author = each.xpath('div[@class="pub"]/text()').extract()[0]
            quantity = each.xpath('div[@class="star clearfix"]/span[@class="pl"]/text()').extract()[0];

            #替换空格和换行
            title = title.replace(' ','').replace('\n','')
            author = author.replace(' ','').replace('\n','')
            quantity = quantity.replace(' ','').replace('\n','')
            quantity = quantity.replace('(','').replace(')','')
            quantity = quantity.replace('少于'.decode('utf-8'),'').replace('人评价'.decode('utf-8'),'')

            item['title'] = title
            item['rate'] = rate
            item['author'] = author
            item['quantity'] = quantity
            item['type'] = DbbookSpider.tag
            # print 'title:' + title
            # print 'rate:' + rate
            # print author
            # print ''
            yield item
            nextPage = selector.xpath('//span[@class="next"]/link/@href').extract()
            if nextPage:
                next = nextPage[0]
                next = "https://book.douban.com" + next;
                print next
                yield scrapy.http.Request(next,callback=self.parse)

