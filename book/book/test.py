import requests
import re

num_str = 9780358434696    # 一个给定的图书ISBN编码

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}
proxies={'http': 'http://127.0.0.1:1080', 'https': 'http://127.0.0.1:1080'}

r = requests.get('https://www.barnesandnoble.com/w/?ean={}/'.format(num_str),proxies=proxies,headers=headers)

name = re.findall('<h1 itemprop="name" class="pdp-header-title ">(.*?)</h1>',r.text)[0]
isbn = re.findall('<th>ISBN-13:</th>[\s\S]+?<td>(\d+)</td>',r.text)[0]
price = re.findall('<span id="[\s\S]+?" class="price current-price ml-0">[\s\S]+?</sup>(.*?)</span>',r.text)[0]
overview = re.findall('<div class="text--medium overview-content">([\s\S]+?)</div>',r.text)[0]
overview = re.sub('(<P>)|(<b>)|(<i>)|(</i>)|(</b>)|(<br>)|(</br>)|(<span([\s\S]+?)>)|(</span>)','',overview,flags=re.I).strip()
img = re.findall('<img id="pdpMainImage" tabindex="-1" src="(.*?.jpg)"',r.text)[0]
r_img = requests.get('http:'+img,proxies=proxies,headers=headers)
with open(isbn+'.jpg','wb') as f:
    f.write(r_img.content)
author = re.findall('<span id="key-contributors" class="contributors"> by <a href="[\s\S]+?">(.*?)</a>',r.text)[0]

print(name,'\n',isbn,'\n',price,'\n',overview,'\n',author)

