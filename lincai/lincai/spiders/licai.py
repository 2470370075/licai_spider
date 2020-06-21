# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy import FormRequest
from numpy import *
import re


def get_cookies(cookies_string):
    cookies_string = '; ' + cookies_string + ';'
    keys = re.findall('; (.*?)=', cookies_string)
    values = re.findall('=(.*?);', cookies_string)
    cookies = dict(zip(keys, values))
    return cookies


dic = {"stockIds": [101000000006472], "granularity": "y10", "metricTypes": ["mcw"], "leftMetricNames": ["pe_ttm"],
       "rightMetricNames": ["cp"]}
import json

dic2 = json.dumps(dic)


class LicaiSpider(scrapy.Spider):
    name = 'licai'
    allowed_domains = ['lixinger.com']
    start_urls = ['https://www.lixinger.com/analytics/company/sz/002230/2230/detail/fundamental/profit?start-date=2010-05-08&end-date=2020-05-08&granularity=q&data-label-display=show_annual&left-expression-caculate-type=t&right-expression-caculate-type=t_y2y']
    cookies = 'jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1ZWIyMjcyMWI0Yzg0ZTc1NDYxNTVmZmEiLCJpYXQiOjE1ODg3MzM3ODksImV4cCI6MTU4OTk0MzM4OX0.ycGDJuGvl8PvFOf6v12ppWA8Wi111SY2YIIuX2eHTck'
    cookies2 = 'jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1ZWIyMjcyMWI0Yzg0ZTc1NDYxNTVmZmEiLCJpYXQiOjE1ODg3MzQ4NDEsImV4cCI6MTU4OTk0NDQ0MX0.v1zLOH-ZLYhcVmUwfMujmqwhdRKnnljQSTSzklcVRP8'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}

    def start_requests(self):
        yield Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=get_cookies(self.cookies)
        )

    def parse(self, response):
        print(response.status)
        print(response.text)


    #     chart_url = 'https://www.lixinger.com/api/analyt/stock-collection/price-metrics/get-price-metrics-chart-info'
    #     yield Request(chart_url,
    #                   method="POST",
    #                   body=json.dumps(dic),
    #                   cookies=get_cookies(self.cookies),
    #                   headers={'Content-Type': 'application/json'},
    #                   callback=self.chart_parse)
    #
    # def chart_parse(self, response):
    #     data = json.loads(response.text)
    #     cur_pe_ttm = data["priceMetricsList"][0]['pe_ttm']['mcw']
    #     q8v = data["priceMetricsList"][0]['pos']['pe_ttm']['mcw']["q8v"]
    #     q5v = data["priceMetricsList"][0]['pos']['pe_ttm']['mcw']["q5v"]
    #     q2v = data["priceMetricsList"][0]['pos']['pe_ttm']['mcw']["q2v"]
    #     pe_ttm = [i['pe_ttm']['mcw'] for i in data["priceMetricsList"]]
    #     avg_value = round(mean(pe_ttm),2)
    #     max_value = max(pe_ttm)
    #     min_value = min(pe_ttm)
    #
    #     with open('1.txt','a',encoding='utf-8') as f:
    #         f.write('当前值：{}\n'.format(str(cur_pe_ttm)))
    #         f.write('80分位点：{}\n'.format(q8v))
    #         f.write('50分位点：{}\n'.format(q5v))
    #         f.write('20分位点：{}\n'.format(q2v))
    #         f.write('最大值：{}\n'.format(max_value))
    #         f.write('最小值：{}\n'.format(min_value))
    #         f.write('平均值：{}\n'.format(avg_value))






