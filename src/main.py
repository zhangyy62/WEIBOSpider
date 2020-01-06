# _*_ coding: utf-8 _*_

import sys
import os
from bs4 import BeautifulSoup  # BeautifulSoup为python 爬虫库
import requests  # 网络请求库
import csv
import time
from lxml import etree
from urllib.request import urlretrieve  # 用于图片下载

# 改成自己的user_id和cookie
user_id = 1757693565
cookie = {"Cookie": "WEIBOCN_FROM=1110006030; ALF=1580917952; _T_WM=23874700983; MLOGIN=1; XSRF-TOKEN=25ea6c; SCF=Ah6537r_7dpXQpHU2_gjl6RK5BgzADb8STqMYONVCAcs6bmF9U5HrvpcPUAPYxN8nZ25THthblU6nJbJYs-NhGY.; SUB=_2A25zFyouDeRhGeNH41cZ8yrFzTiIHXVQ-7ZmrDV6PUJbktAKLUunkW1NSmeY2G-sDLop_tdjkhBz-DZ3W2I7Ro9H; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWAsGrPdehLHjqxwQ0i8K7P5JpX5K-hUgL.Fo-41h-Re0B4SoB2dJLoIXnLxKnLBoML1-qLxKqL1hnL1K2LxKBLBonL1h5LxKnLBo-LBoMLxKqLBKnLB-2LxKqL1h.LB-zLxK-L12BL1heLxK-L1hqL1-zt; SUHB=0mxUHb_naevAmc; SSOLoginState=1578326654; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253DSimon_%25E9%2598%25BF%25E6%2596%2587%26from%3D102003%26fid%3D1005051757693565%26uicode%3D10000011"}
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
pageNum = 1

times = 5
one_step = int(pageNum/times)
f = open('%d.csv' % user_id, 'w', encoding='utf-8')
csv_writer = csv.writer(f)
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
            # content = selector.xpath('//span[@class="ctt"]')
            content = selector.xpath('//div[@class="c" and @id]')
            # 遍历每条微博
            for each in content:
                list1 = []
                # 获取文本内容，加入result，记录条数
                zhuanfa = each.xpath('//span[@class="ctt"]')
                print(111)
                print(each.xpath('string(.)'))
                list1.append(each.xpath('string(.)'))

                # for each2 in zhuanfa:
                #     res1 = each2.xpath('string(.)')
                #     print('zhuanfa', res1)
                #     list1.append(res1)

                # print(222)
                # text = each.xpath('string(.)')
                # text = "%d: " % (word_count) + text + "\n"
                # print('each', len(each))

                if len(each) > 2:
                    list1.append(each[2].xpath('a')[
                                 last()-3].xpath('string(.)'))
                    list1.append(each[2].xpath('a')[
                                 last()-2].xpath('string(.)'))
                    list1.append(each[2].xpath('a')[
                                 last()-1].xpath('string(.)'))
                    # print('zhuanfa', each[2].xpath('a')[1].xpath('string(.)'), each[2].xpath(
                    #     'a')[2].xpath('string(.)'), each[2].xpath('a')[3].xpath('string(.)'))
                elif len(each) == 2:
                    list1.append(each[1].xpath('a')[
                                 last()-3].xpath('string(.)'))
                    list1.append(each[1].xpath('a')[
                                 last()-2].xpath('string(.)'))
                    list1.append(each[1].xpath('a')[
                                 last()-1].xpath('string(.)'))
                    # print('zhuanfa', each[1].xpath('a')[1].xpath('string(.)'), each[1].xpath(
                    #     'a')[2].xpath('string(.)'), each[1].xpath('a')[3].xpath('string(.)'))

                elif len(each) == 1:
                    list1.append(each[0].xpath('a')[
                                 last()-3].xpath('string(.)'))
                    list1.append(each[0].xpath('a')[
                                 last()-2].xpath('string(.)'))
                    list1.append(each[0].xpath('a')[
                                 last()-1].xpath('string(.)'))
                    # print('zhuanfa', each[0].xpath('a')[1].xpath('string(.)'), each[0].xpath(
                    # 'a')[2].xpath('string(.)'), each[0].xpath('a')[3].xpath('string(.)'))

                # print('text', text)
                # csv_writer.writerow([word_count, text])
                csv_writer.writerow(list1)
                list1 = []
                # result = result + text
                word_count += 1
            print('第%d页微博内容爬取完完成' % (page))
        except:
            print('第', page, '页发生错误')

        time.sleep(0.005)  # 爬取每页间隔时间
    print('正在进行第', step + 1, '次停顿，防止访问次数过多')
    time.sleep(1)


try:
    # 打开文本存放文件，如果不存在则新建
    # fo_txt = open(os.getcwd()+"/%d" % user_id+".txt", "w")
    # result_path = os.getcwd() + '/%d' % user_id+".txt"
    # print('微博内容文本存放路径为 :', result_path)
    # fo_txt.write(result)  # 将结果写入文件
    # print('爬取成功！\n该用户微博内容：\n\n%s\n文本存放路径为%s' % (result, result_path))
    f.close()

except:
    print('微博文本内容保存失败')
