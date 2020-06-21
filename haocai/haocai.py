# -*- coding: utf-8 -*-
import requests
import json
from pprint import pprint
import openpyxl

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}
page = '1'
data_list = []

for page in range(0,360):
    post_data = {"_search":"false","nd":"1591365154823","rows":"25","page":page,"sidx":"specification_code","sord":"asc"}
    res = requests.post(url='http://code.nhsa.gov.cn:8000/hc/stdSpecification/getStdSpecificationListData.html',
                        data=post_data,
                        headers=headers)
    data = json.loads(res.text.encode('GBK','ignore').decode('GBk'))
    print(page)
    data_list.extend(data['rows'])

print(data_list)


wb = openpyxl.load_workbook('a.xlsx')
sh = wb['Sheet1']
row = 1
for data_dic in data_list:
    column = 1
    for i in data_dic:
        sh.cell(row=row, column=column).value = data_dic[i]
        column += 1
    row += 1

wb.save('a.xlsx')


