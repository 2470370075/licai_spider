# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json
import re
import openpyxl
import os
import re
from openpyxl.styles import PatternFill
from openpyxl.styles import Font
from openpyxl.styles import colors



guojiadui = ['汇金',
             '中央汇金资产管理公司',
             '中央汇金投资公司',
             '证金',
             '中国证券金融股份有限公司',
             '中证金融资产管理计划',
             '梧桐树投资平台公司',
             '北京凤山投资公司',
             '北京坤藤投资公司',
             '社保基金',
             '基本养老',
             '全国社会',
             '保障基金理事会']


gupiao_list = []
with open('list.txt', 'r') as f:
    while 1:
        gupiao_name = f.readline().strip()
        if gupiao_name == '':
            break
        gupiao_list.append(gupiao_name)


with open('id.txt', 'r', encoding='gbk') as f:
    id_list = f.read()

try:
    id = re.findall('(.*?)' + gupiao_list[-1], id_list)[0].upper()
except:
    pass

if "SZ" in id:
    szbh = '0'
else:
    szbh = '1'

wb = openpyxl.load_workbook('a.xlsx')
sh = wb['Sheet1']
column = 3
ce = sh.cell(row=1, column=column)


class CdongfangSpider(scrapy.Spider):
    name = 'cdongfang'
    id = id.strip()
    gupiao_name = gupiao_list.pop()
    szid = re.findall('(\d+)', id)[0]
    szbh = szbh
    allowed_domains = ['f10.eastmoney.com', '18.push2.eastmoney.com', 'push2.eastmoney.com', 'f10.eastmoney.com',
                       'f10.eastmoney.com']
    start_urls = ['http://f10.eastmoney.com/f10_v2/OperationsRequired.aspx?code={}'.format(id)]
    column = 4

    def parse(self, response):

        url = 'http://f10.eastmoney.com/NewFinanceAnalysis/MainTargetAjax?type=1&code={}'.format(self.id)
        request = Request(url, callback=self.head_data)
        yield request

    def head_data(self, response):

        sh.cell(row=1, column=self.column).value = self.id
        sh.cell(row=2, column=self.column).value = self.gupiao_name
        sh.cell(row=4, column=self.column - 1).value = '排名'
        sh.cell(row=4, column=self.column).value = '2020'
        sh.cell(row=4, column=self.column + 1).value = '2019'
        sh.cell(row=4, column=self.column + 2).value = '2018'

        data = json.loads(response.text)

        c = 0
        l = []
        for i in data:
            c += 1
            l.append(i)
            if c == 2:
                break

        two_year = []
        for i in l:
            one_year = []
            print(i)
            yyzsrtbzz7 = i['yyzsrtbzz']
            one_year.append(yyzsrtbzz7)
            gsjlrtbzz8 = i['gsjlrtbzz']
            one_year.append(gsjlrtbzz8)

            kfjlrtbzz9 = i['kfjlrtbzz']
            one_year.append(kfjlrtbzz9)

            mll10 = i['mll']
            one_year.append(mll10)

            jll11 = i['jll']
            one_year.append(jll11)

            jqjzcsyl12 = i['jqjzcsyl']
            one_year.append(jqjzcsyl12)

            zcfzl14 = i['zcfzl']
            one_year.append(zcfzl14)

            ldbl16 = i['ldbl']
            one_year.append(ldbl16)

            sdbl17 = i['sdbl']
            one_year.append(sdbl17)
            two_year.append(one_year)

        self.column += 1
        for i in two_year:
            sh.cell(row=8, column=self.column).value = i[0]
            sh.cell(row=9, column=self.column).value = i[1]
            sh.cell(row=10, column=self.column).value = i[2]
            sh.cell(row=11, column=self.column).value = i[3]
            sh.cell(row=12, column=self.column).value = i[4]
            sh.cell(row=13, column=self.column).value = i[5]
            sh.cell(row=15, column=self.column).value = i[6]
            sh.cell(row=17, column=self.column).value = i[7]
            sh.cell(row=18, column=self.column).value = i[8]
            self.column += 1
        wb.save('b.xlsx')

        url = 'https://push2.eastmoney.com/api/qt/stock/get?secid={}.{}&ut=f057cbcbce2a86e2866ab8877db1d059&fields=f57,f58,f43,f169,f170,f168,f47,f48,f86,f46,f44,f60,f45,f168,f164,f50,f171&np=1&fltt=2&invt=2&cb=jQuery1800949845130501221_1589442842631&_=1589442842693'.format(
            self.szbh, self.szid)
        yield Request(url, callback=self.body_data)

    def body_data(self, response):

        hsl18 = re.findall('"f168":(.*?),', response.text)
        cjl20 = re.findall('"f47":(.*?),', response.text)
        cje21 = re.findall('"f48":(.*?),', response.text)
        self.column -= 3

        sh.cell(row=19, column=self.column).value = hsl18[0]
        sh.cell(row=21, column=self.column).value = cje21[0]
        sh.cell(row=22, column=self.column).value = cjl20[0]

        wb.save('b.xlsx')

        url = 'http://f10.eastmoney.com/NewFinanceAnalysis/MainTargetAjax?type=0&code={}'.format(self.id)
        yield Request(url, self.new_head)

    def new_head(self, response):
        data = json.loads(response.text)
        yyzsrtbzz7 = data[0]['yyzsrtbzz']
        gsjlrtbzz8 = data[0]['gsjlrtbzz']
        kfjlrtbzz9 = data[0]['kfjlrtbzz']
        mll10 = data[0]['mll']
        jll11 = data[0]['jll']
        jqjzcsyl12 = data[0]['jqjzcsyl']
        zcfzl14 = data[0]['zcfzl']
        ldbl16 = data[0]['ldbl']
        sdbl17 = data[0]['sdbl']

        sh.cell(row=7, column=self.column).value = yyzsrtbzz7
        sh.cell(row=8, column=self.column).value = gsjlrtbzz8
        sh.cell(row=9, column=self.column).value = kfjlrtbzz9
        sh.cell(row=10, column=self.column).value = mll10
        sh.cell(row=11, column=self.column).value = jll11
        sh.cell(row=12, column=self.column).value = jqjzcsyl12
        sh.cell(row=14, column=self.column).value = zcfzl14
        sh.cell(row=16, column=self.column).value = ldbl16
        sh.cell(row=17, column=self.column).value = sdbl17

        wb.save('b.xlsx')
        url = 'http://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&invt=2&fltt=2&fields=f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f164,f163,f116,f60,f45,f52,f50,f48,f167,f117,f71,f161,f49,f530,f135,f136,f137,f138,f139,f141,f142,f144,f145,f147,f148,f140,f143,f146,f149,f55,f62,f162,f92,f173,f104,f105,f84,f85,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f107,f111,f86,f177,f78,f110,f262,f263,f264,f267,f268,f250,f251,f252,f253,f254,f255,f256,f257,f258,f266,f269,f270,f271,f273,f274,f275,f127,f199,f128,f193,f196,f194,f195,f197,f80,f280,f281,f282,f284,f285,f286,f287&secid={}.{}&cb=jQuery112405506785612361488_1589457232614&_=1589457232640'.format(
            self.szbh, self.szid)

        yield Request(url, self.last_data)

    def last_data(self, response):

        sy4 = re.findall('"f162":(.*?),', response.text)[0]
        sj5 = re.findall('"f167":(.*?),', response.text)[0]

        sh.cell(row=5, column=self.column).value = sy4
        sh.cell(row=6, column=self.column).value = sj5

        url = 'http://f10.eastmoney.com/ShareholderResearch/ShareholderResearchAjax?code={}'.format(self.id)

        yield Request(url, callback=self.gudong_parse)

    def gudong_parse(self, response):
        data = json.loads(response.text)

        c = 0
        sum = 0
        sh.cell(row=23 + c, column=self.column - 1).value = '排名'
        sh.cell(row=23 + c, column=self.column).value = '占总流通股本持股比例'
        sh.cell(row=23 + c, column=self.column + 1).value = '增减股'
        sh.cell(row=23 + c, column=self.column + 2).value = '变动比例'
        sh.cell(row=34 + c, column=self.column - 1).value = '合计'
        for i in data['sdltgd'][0]['sdltgd']:

            sh.cell(row=24 + c, column=self.column - 1).value = i['gdmc']
            for j in guojiadui:
                if j in i['gdmc']:
                    orange_fill = PatternFill(fill_type='solid', fgColor="FFC125")
                    sh.cell(row=24 + c, column=self.column - 1).fill = orange_fill
            if '香港中央结算' in i['gdmc']:
                print(i['gdmc'])
                print()
                grey_fill = PatternFill(fill_type='solid', fgColor="77887B")
                sh.cell(row=24 + c, column=self.column - 1).fill = grey_fill
            sh.cell(row=24 + c, column=self.column).value = i['zltgbcgbl']
            sh.cell(row=24 + c, column=self.column + 1).value = i['zj']
            if '-' in i['zj']:

                ft = Font(color=colors.GREEN)
                sh.cell(row=24 + c, column=self.column + 1).font = ft
                sh.cell(row=24 + c, column=self.column + 2).font = ft



            if '新' in i['zj'] or i['zj'].isdigit():

                ft = Font(color=colors.RED)
                sh.cell(row=24 + c, column=self.column + 1).font = ft


            sh.cell(row=24 + c, column=self.column + 2).value = i['bdbl']
            c += 1

            sum = float(i['zltgbcgbl'][0:-1]) + sum
        sh.cell(row=34, column=self.column).value = sum

        c = 0
        sum = 0
        row = 36
        sh.cell(row=row - 1, column=self.column - 1).value = '排名'
        sh.cell(row=row - 1, column=self.column).value = '占总流通股本持股比例'
        sh.cell(row=row - 1, column=self.column + 1).value = '增减股'
        sh.cell(row=row - 1, column=self.column + 2).value = '变动比例'
        sh.cell(row=row + 10, column=self.column - 1).value = '合计'
        for i in data['sdgd'][0]['sdgd']:

            sh.cell(row=row + c, column=self.column - 1).value = i['gdmc']
            for j in guojiadui:
                if j in i['gdmc']:
                    orange_fill = PatternFill(fill_type='solid', fgColor="FFC125")
                    sh.cell(row=row + c, column=self.column - 1).fill = orange_fill
                if '香港中央结算' in i['gdmc']:
                    orange_fill = PatternFill(fill_type='solid', fgColor="77887B")
                    sh.cell(row=row + c, column=self.column - 1).fill = orange_fill

            if '-' in i['zj']:
                ft = Font(color=colors.GREEN)
                sh.cell(row=row + c, column=self.column + 1).font = ft
                sh.cell(row=row + c, column=self.column + 2).font = ft
            if '新' in i['zj'] or i['zj'].isdigit():
                ft = Font(color=colors.RED)
                sh.cell(row=row + c, column=self.column + 1).font = ft

            sh.cell(row=row + c, column=self.column).value = i['zltgbcgbl']
            sh.cell(row=row + c, column=self.column + 1).value = i['zj']
            sh.cell(row=row + c, column=self.column + 2).value = i['bdbl']
            c += 1

            sum = float(i['zltgbcgbl'][0:-1]) + sum
        sh.cell(row=row + 10, column=self.column).value = sum

        wb.save('b.xlsx')

        while 1:
            self.column += 4
            self.gupiao_name = gupiao_list.pop()
            try:
                self.id = re.findall('(.*?)' + self.gupiao_name, id_list)[0].upper().strip()
                break
            except:
                pass


        self.szid = re.findall('(\d+)', self.id)[0]

        if "SZ" in self.id:
            self.szbh = '0'
        else:
            self.szbh = '1'

        url = 'http://f10.eastmoney.com/NewFinanceAnalysis/MainTargetAjax?type=1&code={}'.format(self.id)

        yield Request(url,callback=self.head_data)
