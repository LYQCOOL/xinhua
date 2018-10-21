#coding:utf-8
import sys
sys.path.append("..")
import re
import requests
import time

def Run():
    html = ''
    URL = ['http://qc.wa.news.cn/nodeart/list?nid=113352&pgnum=1&cnt=10&tp=1&orderby=1','http://qc.wa.news.cn/nodeart/list?nid=113352&pgnum=2&cnt=10&tp=1&orderby=1',
           'http://qc.wa.news.cn/nodeart/list?nid=11147664&pgnum=1&cnt=16&tp=1&orderby=1','http://qc.wa.news.cn/nodeart/list?nid=11147664&pgnum=2&cnt=16&tp=1&orderby=1',
            'http://sports.news.cn/zcfx.htm','http://sports.news.cn/tycy.htm','http://sports.news.cn/mls.htm','http://sports.news.cn/zhty.htm','http://sports.news.cn/zgzq.htm',
            'http://sports.news.cn/xhs.htm','http://qc.wa.news.cn/nodeart/list?nid=116716&pgnum=1&cnt=10&tp=1&orderby=1',
            'http://qc.wa.news.cn/nodeart/list?nid=116716&pgnum=2&cnt=10&tp=1&orderby=1','http://qc.wa.news.cn/nodeart/list?nid=1118296&pgnum=1&cnt=10&tp=1&orderby=1',
           'http://qc.wa.news.cn/nodeart/list?nid=1118296&pgnum=2&cnt=10&tp=1&orderby=1','http://qc.wa.news.cn/nodeart/list?nid=116715&pgnum=1&cnt=10&tp=1&orderby=1'
            'http://qc.wa.news.cn/nodeart/list?nid=116715&pgnum=2&cnt=10&tp=1&orderby=1',
           'http://ent.news.cn/pl.htm','http://www.sc.xinhuanet.com/']
    for i in URL:
        while 1:
            try:
                html = requests.get(i, timeout = 30).content
                break
            except Exception as e:
                print e
        re_ = 'http://news.xinhuanet.com/politics/' + time.strftime("%Y-%m/%d") + '/c_\d+.htm|' \
                    'http://news.xinhuanet.com/fortune/' + time.strftime("%Y-%m/%d") + '/c_\d+.htm|' \
                    'http://ent.news.cn/' + time.strftime("%Y-%m/%d") + '/c_\d+.htm|' \
                    'http://sports.xinhuanet.com/c/' + time.strftime("%Y-%m/%d") + '/c_\d+.htm|' \
                    'http://www.sc.xinhuanet.com/content/' + time.strftime("%Y-%m/%d") + '/c_\d+.htm'
        news_url_list = re.findall(re_, html)
        l2 = list(set(news_url_list))
        l2.sort(key=news_url_list.index)
        for news_url in l2:
            yield news_url

        '''l3 = ['http://www.sc.xinhuanet.com/content/2017-12/07/c_1122071732.htm']
        for news_url in l3:
            yield news_url'''

if __name__ =='__main__':
    Run()
