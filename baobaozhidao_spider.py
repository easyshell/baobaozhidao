#encoding:utf-8

import sys
if __name__ == '__main__':
    print(sys.path)

from scrapy.http import Request

import scrapy
#global scrapy_version
#if scrapy.__version__!='0.15.0':
from scrapy.spider import Spider
from scrapy.selector import Selector
#    scrapy_version = 'new'
#else:
#    from scrapy.spider import BaseSpider
#    from scrapy.selector import HtmlXPathSelector
#    scrapy_version = 'old'

import re
import codecs
from urlparse import urljoin
import urlparse
from posixpath import normpath

class BaoBaoZhiDaoSpider(Spider):
    name = "baobaozhidao_spider"
    list_urls = {}

    def url_pattern(self):
        pattern = 'http://baobao.baidu.com/\d+(/$|$)'
        post_url_re = re.compile(pattern)
        return post_url_re

    def __init__(self):
        print('init')
        self.make_urls()
        self.post_url_re = self.url_pattern()

    def make_urls(self):
        self.get_list_urls('http://baobao.baidu.com/browse?pn=',1,101, 1)

    def get_list_urls(self,home_url,start_pages_num,end_pages_num,flag):
        pages_num = end_pages_num - start_pages_num + 1
        print(pages_num)
        for i in range(pages_num):
            i = i + (start_pages_num-1)
            print(i)
            url = home_url+str(i*20)
            self.list_urls.update({url:flag})

    def write_urls(self,flag):
        filename = 'baobaozhidao_question_urls%s.my'%(flag)
        writer = codecs.open(filename, 'a+', 'utf-8', errors='ignore')
        return writer

    def start_requests(self):
        reqs = []
        for url,flag in self.list_urls.iteritems():
            req = Request(url,callback=self.parse,dont_filter=True,meta={'url':url,'flag':flag})
            reqs.append(req)
        return reqs

    def group_url(self,urls,base_url):
        post_urls = []
        for u in urls:
            if u.startswith('http:') or u.startswith('https:'):
                tmp = u
            else:
                full_url = urljoin(base_url,u)
                list_url = urlparse.urlparse(full_url)
                path = normpath(list_url.path)
                final_url = urlparse.urlunparse((list_url.scheme,list_url.netloc,path,list_url.params,list_url.query,list_url.fragment))

                if final_url == base_url:
                    continue
                tmp = final_url
                if ':' not in tmp or 'http' not in tmp:
                    continue
            post_urls.append(tmp)
        return post_urls

    def parse(self,response):
	#print response.url
        url = response.meta.get('url')
        flag = response.meta.get('flag')
        #         print url
        #         print flag
        content = response.body_as_unicode()
	    #open('content.html','w').write(content)
        content = content.replace('<!--','').replace('-->','')
        sel = Selector(text=content)

        #if scrapy_version=='new':
        urls = sel.xpath('//a[@class="clearfix f-14"]/@href').extract()
        print(len(urls))
	    #print urls
        #elif scrapy_version=='old':
        #    urls = hxs.select('//a[@class="j_th_tit"]/@href').extract()

        post_urls = self.group_url(urls,url)
        writer = self.write_urls(flag)
        for url in post_urls:
            writer.write(url+'\n')



