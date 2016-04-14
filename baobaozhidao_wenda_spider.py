#encoding:utf-8
import json
import re
import time
import datetime
import sys
import urlparse
from bs4 import BeautifulSoup

from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector

from baobaozhidaole.items import *

reload(sys)
sys.setdefaultencoding('utf-8')

class TieziSpider(Spider):
    name = 'baobaozhidao_wenda_spider'
    def __init__(self,**kwargs):
        self.timepattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')
        self.nextpage_pattern = re.compile(ur'<a href="(?P<nextpage>/p/\d+\?pn=\d+)">\u4e0b\u4e00\u9875</a>')
        
        self.seeds = kwargs['seeds'] 
        self.delete_baobaozhidao_wenda = open('delete_baobaozhidao_wenda.dat','w')
        
    def start_requests(self):
        f = open(self.seeds,'r')
        reqs = []
        while True:
            line = f.readline()
            if not line:
                break
            reqs.append(Request(line.strip(),meta={'url':line.strip(), 'pn':0}))
        return reqs
    
    def format_time(self,timestr):
        localtime = time.localtime(float(timestr))
        localtime = datetime.datetime(* localtime[:6])
        return localtime
    
    def parse(self,response):
        #'问题', '问题人','提问时间','答复人', '答复时间', '引用链接'
        url = response.request.meta.get('url')
        cur_pn = int(response.request.meta.get('pn', 0))
        try:
            content = response.body_as_unicode()
        except:
            content = response.body
        sel = Selector(text=content)

        item = sel.xpath('//section[contains(@class, "line qb-section")]').extract()[0]
        item_sel = Selector(text=item)
        wenti = item_sel.xpath('//article/div[1]/h2/span[contains(@class, "qb-icon ask-icon")]/../text()').extract()[1]
        wenti_author = item_sel.xpath('//div[1]/div/a[contains(@class, "username")]/text()').extract()[0]
        wenti_time = item_sel.xpath('//div[1]/div/span/text()').extract()[0]

        dafu_items = item_sel.xpath('//article/div[2]/div[contains(@class, "answer-detail")]').extract()
        with open("dafu_items", "wb") as f:
            f.write(dafu_items[0])
        for dafu_item in dafu_items:
            dafu_item_sel = Selector(text=dafu_item)
            dafu = dafu_item_sel.xpath('//p/text()').extract()[0]
            dafu_author = dafu_item_sel.xpath('//div[contains(@class, "answer-meta")]/a/text()').extract()[0]
            dafu_time = dafu_item_sel.xpath('//div[contains(@class, "answer-meta")]/span/text()').extract()[0]
            result_item = BaobaozhidaoleItem()
            result_item['wenti'] = str(wenti).strip()
            result_item['wenti_author'] = str(wenti_author).strip()
            result_item['wenti_time'] = str(wenti_time).strip()
            result_item['dafu'] = str(dafu).strip()
            result_item['dafu_author'] = str(dafu_author).strip()
            result_item['dafu_time'] = str(dafu_time).strip()
            result_item['href_url'] = str(url).strip()
            yield result_item
        load_more = item_sel.xpath('//article/div[2]/div[contains(@class, "load-more")]').extract()
        if load_more:
            load_more_url = "http://baobao.baidu.com/question/ajax/replymore?"
            qid = urlparse.urlparse(url).path.split("/")[-1].split(".")[0]
            suffix = "qid="+str(qid)+"&pn="+str(cur_pn+5)+"&rn=5"
            load_more_url += suffix
            print(load_more_url)
            yield Request(load_more_url, callback=self.parse_more_dafu, meta={'url':url, 'pn':str(cur_pn+5), 
    
    def parse_more_dafu(self, response):
        #'问题', '问题人','提问时间','答复人', '答复时间', '引用链接'
        url = response.request.meta.get('url')
        cur_pn = int(response.request.meta.get('pn')
        try:
            content = response.body_as_unicode()
        except:
            content = response.body
        sel = Selector(text=content)

        dafu_items = sel.xpath('//div[contains(@class, "answer-detail")]').extract()
        with open("dafu_items", "wb") as f:
            f.write(dafu_items[0])
        for dafu_item in dafu_items:
            dafu_item_sel = Selector(text=dafu_item)
            dafu = dafu_item_sel.xpath('//p/text()').extract()[0]
            dafu_author = dafu_item_sel.xpath('//div[contains(@class, "answer-meta")]/a/text()').extract()[0]
            dafu_time = dafu_item_sel.xpath('//div[contains(@class, "answer-meta")]/span/text()').extract()[0]
            result_item = BaobaozhidaoleItem()
            result_item['wenti'] = str(wenti).strip()
            result_item['wenti_author'] = str(wenti_author).strip()
            result_item['wenti_time'] = str(wenti_time).strip()
            result_item['dafu'] = str(dafu).strip()
            result_item['dafu_author'] = str(dafu_author).strip()
            result_item['dafu_time'] = str(dafu_time).strip()
            result_item['href_url'] = str(url).strip()
            yield result_item
        load_more = item_sel.xpath('//article/div[2]/div[contains(@class, "load-more")]').extract()
        if load_more:
            load_more_url = "http://baobao.baidu.com/question/ajax/replymore?"
            qid = urlparse.urlparse(url).path.split("/")[-1].split(".")[0]
            suffix = "qid="+str(qid)+"&pn="+str(cur_pn+5)+"&rn=5"
            load_more_url += suffix
            print(load_more_url)
            yield Request(load_more_url, callback=self.parse_more_dafu, meta={'url':url, 'pn':str(cur_pn+5)})
        
        


