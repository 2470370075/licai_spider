import requests


import re
def get_cookies(cookies_string):
    cookies_string = '; '+cookies_string+';'
    keys = re.findall('; (.*?)=',cookies_string)
    values = re.findall('=(.*?);',cookies_string)
    cookies = dict(zip(keys,values))
    return cookies

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}

cookies = 'jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1ZWIyMjcyMWI0Yzg0ZTc1NDYxNTVmZmEiLCJpYXQiOjE1ODg3MzM3ODksImV4cCI6MTU4OTk0MzM4OX0.ycGDJuGvl8PvFOf6v12ppWA8Wi111SY2YIIuX2eHTck'

url = 'https://www.lixinger.com/analytics/index/indexsp/.INX/6472/detail/value'

res = requests.get(url,cookies=get_cookies(cookies),headers=headers)
print(res.text)