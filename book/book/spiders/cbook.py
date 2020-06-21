# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class CbookSpider(scrapy.Spider):
    name = 'cbook'
    allowed_domains = ['www.barnesandnoble.com/']
    start_urls = ['https://www.barnesandnoble.com/w/a-sky-beyond-the-storm-sabaa-tahir/1136569449?ean=9780448494531']

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'}

    def start_requests(self):
        yield Request(
            self.start_urls[0],
            callback=self.parse,
            headers=self.headers

        )
    def parse(self, response):
        print(response.text)
