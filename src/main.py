# _*_ coding: utf-8 _*_

import sys
import os
from bs4 import BeautifulSoup  # BeautifulSoup为python 爬虫库
import requests  # 网络请求库
import csv
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

print('该用户微博页数 : ', pageNum)

times = 5
one_step = int(pageNum/times)
f = open('%d.csv' % user_id, 'w', encoding='utf-8')
csv_writer = csv.writer(f)
csv_writer.writerow(['内容', '赞', '转发', '评论', '是否转发'])

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
            url = 'http://weibo.cn/%d/profile?page=%d' % (user_id, page)
            print('正在爬取url : ', url)
            # 获取当前url页面微博内容
            lxml = requests.get(url, cookies=cookie).content
            selector = etree.HTML(lxml)
            # 获取该页面微博list
            content = selector.xpath('//div[@class="c" and @id]')
            # 遍历每条微博
            for each in content:
                list1 = []
                # 获取文本内容，加入result，记录条数
                zhuanfa = each.xpath('//span[@class="ctt"]')
                text = each.xpath('string(.)')
                list1.append(text)

                if len(each) > 2:
                    nodes = each[2].xpath('a')
                    length = len(nodes)
                    list1.append(nodes[length - 4].xpath('string(.)').replace('赞[', '').replace(']', ''))
                    list1.append(nodes[length - 3].xpath('string(.)').replace('转发[', '').replace(']', ''))
                    list1.append(nodes[length - 2].xpath('string(.)').replace('评论[', '').replace(']', ''))
                elif len(each) == 2:
                    nodes = each[1].xpath('a')
                    length = len(nodes)
                    list1.append(nodes[length - 4].xpath('string(.)').replace('赞[', '').replace(']', ''))
                    list1.append(nodes[length - 3].xpath('string(.)').replace('转发[', '').replace(']', ''))
                    list1.append(nodes[length - 2].xpath('string(.)').replace('评论[', '').replace(']', ''))
                elif len(each) == 1:
                    nodes = each[0].xpath('a')
                    length = len(nodes)
                    list1.append(nodes[length - 4].xpath('string(.)').replace('赞[', '').replace(']', ''))
                    list1.append(nodes[length - 3].xpath('string(.)').replace('转发[', '').replace(']', ''))
                    list1.append(nodes[length - 2].xpath('string(.)').replace('评论[', '').replace(']', ''))

                print(text, text.find('转发了'))
                if text.find('转发了') > -1:
                    list1.append('是')
                else:
                    list1.append('否')

                csv_writer.writerow(list1)
                list1 = []
                word_count += 1
            print('第%d页微博内容爬取完完成' % (page))
        except:
            print('第', page, '页发生错误')

        time.sleep(0.01)  # 爬取每页间隔时间
    print('正在进行第', step + 1, '次停顿，防止访问次数过多')
    time.sleep(3)


try:
    f.close()

except:
    print('微博文本内容保存失败')
