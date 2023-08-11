# -*- coding: utf-8 -*-
# @Time    : 2023/8/11 11:35
# @Author  : 莫枫
# @Site    : 
# @File    : down_text.py
# @Software: PyCharm
import logging
import os
import requests
from lxml import etree
from logger import logger

class down:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',

        }

    @staticmethod
    def get_response(url, headers):
        for i in range(4):
            try:
                r = requests.get(url, headers=headers, timeout=4, verify=False)  # , proxies=proxy()
                return r
            except Exception as e:
                logger.error(e)

    def load(self,text,name):
        path = os.path.abspath(name+".txt")
        logger.info(path)
        with open(path,'a+',encoding='utf-8') as f:
            f.write(text)

    def parse(self,title,url,name):
        r_ = self.get_response(url,headers=self.headers)
        html_1 = etree.HTML(r_.text)
        text = ''.join(html_1.xpath('//div[@id="content"]//text()')).replace('app2();','')
        text = title + '\r\n' + text + '\r\n'
        self.load(text,name)

    def start(self):
        url = 'https://www.2mcnm.com/html/book/13/13499/607170072.html'
        r = self.get_response(url,headers=self.headers)
        html = etree.HTML(r.text)
        list_1 = html.xpath('//div[@class="listmain"]/dl/dt[last()]/following-sibling::*')
        name = ''.join(html.xpath('//div[@id="info"]/h1/text()'))
        for i in list_1:
            title = ''.join(i.xpath('.//a/text()'))
            url = 'https://www.2mcnm.com' + ''.join(i.xpath('.//a/@href'))
            logger.info(title)
            logger.info(url)
            self.parse(title,url,name)

if __name__ == '__main__':
    a = down()
    a.start()