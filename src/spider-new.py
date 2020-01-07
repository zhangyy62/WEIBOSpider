# _*_ coding: utf-8 _*_

import sys
import os
from bs4 import BeautifulSoup  # BeautifulSoup为python 爬虫库
import requests  # 网络请求库
import csv
import json
import time
from lxml import etree
from urllib.request import urlretrieve  # 用于图片下载

endTime = '2019-01-01 00:00:00'

# 改成自己的user_id和cookie
user_id = your_id
cookie = {"Cookie": ""}
# 初始url
url = 'http://weibo.cn/%d/profile?page=1' % user_id
# 获取初始url页面html内容，获取user_id和cookie（在返回的response header中）
html = requests.get(url, cookies=cookie).content
# print('user_id和cookie读入成功')

# html元素selector
selector = etree.HTML(html)
# 通过xpath获取该用户微博页面总数
pageNum = int(selector.xpath('//input[@name="mp"]')[0].attrib['value'])

result = ""
word_count = 1  # 爬取的微博和图片数
image_count = 1
pageNum = 120
print('该用户微博页数 : ', pageNum)

times = 5
one_step = int(pageNum/times)
f = open('%d.csv' % user_id, 'w', encoding='utf-8-sig')
csv_writer = csv.writer(f)
csv_writer.writerow(['日期', '内容', '阅读量', '转发数', '评论数', '点赞数', '类型'])

for step in range(times):
    if step < times - 1:
        i = int(step * one_step + 1)
        j = int((step + 1) * one_step + 1)
    else:
        i = int(step * one_step + 1)
        j = int(pageNum + 1)
    for page in range(i, j):
        try:
            # 目标页面 url
            # url = 'http://weibo.cn/%d/profile?page=%d' % (user_id, page)
            url = 'https://m.weibo.cn/api/container/getIndex?containerid=2304131757693565_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page=%d' % page
            cont = requests.get(url, cookies=cookie).text
            obj = json.loads(cont)
            cards = obj['data']['cards']

            for each in cards:
                if 'mblog' in each:
                    mblog = each['mblog']
                    list1 = []
                    list1.append(mblog['created_at'])
                    list1.append(mblog['text'])
                    list1.append(mblog['reads_count'])
                    list1.append(mblog['reposts_count'])
                    list1.append(mblog['comments_count'])
                    list1.append(mblog['attitudes_count'])
                    # list1.append(each['scheme'])
                    if 'retweeted_status' in mblog:
                        list1.append('转发')
                    else:
                        list1.append('原创')
                    
                    csv_writer.writerow(list1)
            print('第%d页微博内容爬取完完成' % (page))
            time.sleep(3)
        except:
            print('第', page, '页发生错误')
    print('正在进行第', step + 1, '次停顿，防止访问次数过多')
    time.sleep(5)


try:
    f.close()

except:
    print('微博文本内容保存失败')
