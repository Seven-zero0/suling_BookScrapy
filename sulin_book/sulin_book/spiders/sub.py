# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import re


class SubSpider(scrapy.Spider):
    name = 'sub'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/']

    def parse(self, response):
        # 获取首页菜单
        menu_list = response.xpath('//div[@class="menu-list"]//dl')
        for menu in menu_list:
            item = {}
            item['menu_item'] = menu.xpath('./dt/h3/a/text()').extract_first()  # 标题
            item['menu_href'] = menu.xpath('./dt/h3/@href').extract_first()     # 标题url
            dd_list = menu.xpath('./dd/a')  # 获得小标签
            for dd in dd_list:
                item['menu_item'] = dd.xpath('./text()').extract_first()
                item['menu_href'] = dd.xpath('./@href').extract_first()     # 链接

                yield scrapy.Request(
                    url=item['menu_href'],
                    callback=self.parse_book_list,
                    meta={"item": deepcopy(item)}
                )

    def parse_book_list(self, response):
        """ 获取书籍的详情页面 """
        item = response.meta.get('item')
        book_url_list = response.xpath('//ul[@class="clearfix"]/li')
        for book_url in book_url_list:
            item['book_name'] = book_url.xpath("//div[@class='res-img']//a/img/@alt").extract_first()
            item['book_image'] = book_url.xpath("//div[@class='res-img']//a/img/@src2").extract_first()
            item['href'] = book_url.xpath("//div[@class='res-img']//a/@href").extract_first()
            # print(item['book_name'])
            if item['href'] is not None:
                item['href'] = 'http:' + item['href']

                yield scrapy.Request(
                    url=item['href'],
                    callback=self.parse_book_detail,
                    meta={'item': deepcopy(item)}
                )

    def parse_data(self, data):
        return data.replace("\n", "").replace("\r", "").replace("\t", "").replace("</span>", "")

    def parse_book_detail(self, response):
        """ 获取出版社和作者 """
        item = response.meta.get('item')
        item['book_author'] = response.xpath("//ul[@class='bk-publish clearfix']/li[1]/text()").extract_first()
        item['book_author'] = self.parse_data(item['book_author'])
        item['book_press'] = response.xpath("//ul[@class='bk-publish clearfix']/li[2]/text()").extract_first()
        item['book_press'] = self.parse_data(item['book_press'])
        print(item)
