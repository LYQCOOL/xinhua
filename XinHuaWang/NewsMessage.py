#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
sys.path.append("..")
import requests
import time
from lxml import etree
from NewsComment import NewsComment
from Pipe import MongoDB
from huancun import huanCun
from Xpath import *
import NewsUrl
import json
from gen_zong import genZong
class NewsMessage(object):
    def __init__(self):
        self.comment = NewsComment()
        self.mongo = MongoDB()
        self.huan = huanCun()
        '''self.genzong = genZong()'''
    def getNewsMessage(self):
        '''self.genzong.run()'''
        for news_url in NewsUrl.Run():
            headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
                "Host": re.split(r"/",news_url)[2],
            }
            html = ''
            flag = 1
            while 1:
                try:
                    html = requests.get(news_url, headers=headers, timeout=30).content
                    break
                except Exception as e:
                    flag += 1
                    print "RREQUESTERROR",e
                    print "URL:"+news_url
                if flag > 10:
                    return
            tree = etree.HTML(html)

            '''这一段代码是用来获取阅读数和评论数的'''
            comment_number = self.getCommentNumber(news_url)
            if comment_number:
                yue_du_shu = comment_number[0]
                ping_lun_shu_liang = comment_number[1]
            else:
                yue_du_shu = 0
                ping_lun_shu_liang = 0

            message_dict = dict()
            # 文章网址
            wen_zhang_wang_zhi = news_url
            message_dict['wen_zhang_wang_zhi'] = wen_zhang_wang_zhi

           # 文章标题.//*[@class="h-title"]/text()
            wen_zhang_biao_ti = pathOneNode(tree, ".//*[@class='h-title']/text()|.//*[@class='btt']/h1/text()|.//*[@class='tit']/h1/text()|.//*[@class='sm01']/text()|.//*[@id='title']/text()")
            message_dict['wen_zhang_biao_ti'] = wen_zhang_biao_ti

            # 发布时间
            fa_bu_shi_jian = pathOneNode(tree, ".//*[@class='h-time']/text()|.//*[@class='time']/text()|.//*[@class='gnxx']/div[2]/text()|.//*[@class='tm']/text()|.//*[@class='sm02']/text()|.//*[@id='pubtime']/text()")
            message_dict['fa_bu_shi_jian'] = fa_bu_shi_jian

            # 评论数量 '''
            ping_lun_shu_liang = ping_lun_shu_liang
            message_dict['ping_lun_shu_liang'] = ping_lun_shu_liang

            # 文章来源.//*[@id="source"]/text()
            try:
                wen_zhang_lai_yuan = tree.xpath(".//*[@class='ly']/a/text()|.//*[@class='gnxx']/div[1]/text()|.//*[@class='sus']/a/text()|.//*[@class='sm02']/a/text()|.//*[@id='source']/text()")[-1].replace(u'来源：','').replace('\r\n','').replace(' ','')
            except:
                wen_zhang_lai_yuan=pathAllNode(tree,".//*[@id='source']//text()")
            message_dict['wen_zhang_lai_yuan'] = wen_zhang_lai_yuan

            # 文章正文.//*[@id='xhw']//p
            try:
                wen_zhang_zheng_wen = tree.xpath(".//*[@id='p-detail']//p/text()|.//*[@class='content']//p/text()|.//*[@id='content']//p/text()|.//*[@id='content']//p/text()")
            except:
                wen_zhang_zheng_wen = pathAllNode(tree,".//*[@id='xhw']")
            zheng_wen = ''
            for i in wen_zhang_zheng_wen:
                zheng_wen = zheng_wen + i.replace(u'　','').replace('\r\n','').replace(' ','')
            message_dict['wen_zhang_zheng_wen'] = zheng_wen

            # 抓取时间
            do_time = time.time()
            message_dict['do_time'] = do_time

            # 抓取网站
            zhan_dian = u'新华网'
            message_dict['zhan_dian'] = zhan_dian

            # 图片链接
            photo_URL_qian = re.findall(r'http://[a-z|A-Z]+.xinhuanet.com/[a-z|A-Z]+/\d+-\d+/\d+/|http://ent.news.cn/\d+-\d+/\d+/|http://www.sc.xinhuanet.com/[a-z|A-Z]+/\d+-\d+/\d+/',news_url)[0]
            tu_pian_lian = ''
            try:
                tu_pian_lian_jie = tree.xpath(".//*[@align='center']/img/@src|.//*[@align='center']/span/img/@src")
                if tu_pian_lian_jie:
                    for i in tu_pian_lian_jie:
                        photo_URL = photo_URL_qian + i
                        tu_pian_lian =tu_pian_lian+' '+ photo_URL
                else:
                    pass
            except :
                print"photo Error:"+news_url
            message_dict['tu_pian_lian_jie'] = tu_pian_lian
            # 文章栏目
            if (re.split('/',news_url)[3] == 'politics' or re.split('/',news_url)[3] == 'politics'):
                wen_zhang_lan_mu = re.split('/',news_url)[3]
            elif(re.split('/',news_url)[3] == 'c'):
                wen_zhang_lan_mu = 'sport'
            elif(re.split('/',news_url)[3] == 'content'):
                wen_zhang_lan_mu = 'bendi'
            else:
                wen_zhang_lan_mu = 'yule'
            message_dict['wen_zhang_lan_mu'] = wen_zhang_lan_mu

           # 文章作者

            try:
                try:
                    con = tree.xpath(".//*[@class='tiyi1']/../text()")[-1]
                    wen_zhang_zuo_zhe = ''
                    for i in con:
                        wen_zhang_zuo_zhe += i
                except:
                    wen_zhang_zuo_zhe =  pathAllNode(tree,".//*[@class='p-jc']|.//*[@class='bjn']|.//*[@class='bj']|.//*[@class='editor']")
                message_dict['wen_zhang_zuo_zhe'] = wen_zhang_zuo_zhe.replace(u'【纠错】','').replace(u'责任编辑','').replace(u'体育—','').replace('\r\n','').replace(u'：','').replace(':','').replace('[','').replace(']','')
            except:
                 message_dict['wen_zhang_zuo_zhe'] = None
            # 关键词
            try:
                guan_jian_ci = tree.xpath('.//*[@name="keywords"]/@content')[0].replace('\r\n','')
            except:
                guan_jian_ci = None
            message_dict['guan_jian_ci'] = guan_jian_ci

            # 相关标签

            xiang_guan_biao_qian = None
            message_dict['xiang_guan_biao_qian'] = xiang_guan_biao_qian

            # 阅读数量
            yue_du_shu = yue_du_shu
            message_dict['yue_du_shu'] = yue_du_shu

            # 主键
            message_dict['_id'] = news_url
            if(message_dict['fa_bu_shi_jian']) ==None:
                try:
                    with open("ERROR.text","a") as file:
                        file.write(news_url+"\n")
                finally:
                    pass
            else:
                #print json.dumps(message_dict, ensure_ascii=False, indent=4)
                self.mongo.put_content(message_dict)

            if ping_lun_shu_liang > 0:
                all_page = ping_lun_shu_liang/20
                for page in xrange(1, all_page+2):
                    self.comment.run(news_url, page)
            '''#追踪
            dict_zhui = {}
            dict_zhui['url'] = news_url
            dict_zhui['num'] = ping_lun_shu_liang
            dict_zhui['_id'] = news_url
            self.huan.put_zhuizong(dict_zhui)'''



    def getCommentNumber(self,news_url):
        jison_object = dict()
        bu = re.split(r'c_|.htm',news_url)[1]
        comment_url = 'http://comment.home.news.cn/a/newsCommAll.do?newsId=1-' + bu
        flag = 1
        while 1:
            try:
                json_object = json.loads(requests.get(comment_url, timeout=30).content.replace('var commentJsonVarStr___=', '')[:-1])
                break
            except Exception as e:
                flag += 1
                print e
            if flag > 5:
                return
        # 阅读数
        yue_du_shu = None
        # 评论数
        ping_lun_shu_liang = json_object['totalRows']
        return yue_du_shu, ping_lun_shu_liang

if __name__ == "__main__":
    newsMessage = NewsMessage()
    newsMessage.getNewsMessage()
