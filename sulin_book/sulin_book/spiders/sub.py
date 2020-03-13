# -*- coding: utf-8 -*-
import scrapy


class SubSpider(scrapy.Spider):
    name = 'sub'
    allowed_domains = ['suning.com']
    start_urls = ['http://suning.com/']

    def parse(self, response):
        pass
