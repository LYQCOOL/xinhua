# coding: utf-8
import sys
sys.path.append("..")
import re
import requests
from Xpath import *
import json
import pymongo
from NewsComment import NewsComment
from Pipe import MongoDB
from huancun import huanCun
class genZong(object):
    def __init__(self):
        self.comment = NewsComment()
        self.mongo = MongoDB()
        self.huan = huanCun()
    def run(self):
        client = pymongo.MongoClient('localhost', 27017)
        db = client['news']
        collection_zhuizong = db['zhuiZong']
        collection_del = db['zhuiZong']
        collecthion = collection_zhuizong.find()
        for i in collecthion:
            num = self.getCommentNumber(i['url'])
            if num == i['num']:
                collection_del.delete_one({'url': i['url']})
            else:
                all_page = num / 20
                for page in xrange(1, all_page + 2):
                    self.comment.run(i['url'], page)
                dict_zhui = {}
                dict_zhui['url'] = i['url']
                dict_zhui['num'] = num
                dict_zhui['_id'] = i['url']
                '''print json.dumps(dict_zhui, ensure_ascii=False, indent=4)'''
                self.huan.put_zhuizong(dict_zhui)
    def getCommentNumber(self,news_url):
        jison_object = dict()
        bu = re.split(r'c_|.htm', news_url)[1]
        comment_url = 'http://comment.home.news.cn/a/newsCommAll.do?newsId=1-' + bu
        flag = 1
        while 1:
            try:
                json_object = json.loads(
                    requests.get(comment_url, timeout=30).content.replace('var commentJsonVarStr___=', '')[:-1])
                break
            except Exception as e:
                flag += 1
                print e
            if flag > 5:
                return
        # 评论数
        ping_lun_shu_liang = json_object['totalRows']
        return ping_lun_shu_liang




if __name__ == "__main__":
    gen_zong = genZong()
    gen_zong.run()
