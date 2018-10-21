# coding: utf-8
import sys
sys.path.append("..")
import json
import re
from Pipe import MongoDB
import time

'''from Pipe import MongoDB'''
import requests


class NewsComment(object):
    def __init__(self):
        self.mongo = MongoDB()

    def run(self, news_url, page):
        bu = re.split(r'c_|.htm',news_url)[1]
        comment_url = 'http://comment.home.news.cn/a/newsCommAll.do?&newsId=1-%s&pid=%d' % (bu, page)
        json_object = dict()
        comment_dict = dict()
        flag = 1
        while 1:
            try:
                json_object = json.loads(requests.get(comment_url, timeout=30).content.replace('var commentJsonVarStr___=', '')[:-1])
                break
            except Exception as e:
                flag += 1
                print "获取评论错误：", e

            if flag > 5:
                return
        for item in json_object['contentAll']:
            # 评论文章url
            news_url = news_url

            # 评论内容
            ping_lun_nei_rong = item["content"]
            comment_dict['ping_lun_nei_rong'] = ping_lun_nei_rong

            # 评论时间
            ping_lun_shi_jian = item["commentTime"]
            comment_dict['ping_lun_shi_jian'] = ping_lun_shi_jian

            # 回复数量
            hui_fu_shu = None
            comment_dict['hui_fu_shu'] = hui_fu_shu

            # 点赞数量
            dian_zan_shu = item["upAmount"]
            comment_dict['dian_zan_shu'] = dian_zan_shu

            # 评论id
            ping_lun_id = item["userId"]
            comment_dict['ping_lun_id'] = ping_lun_id

            # 用户昵称
            yong_hu_ming = item["nickName"]
            comment_dict['yong_hu_ming'] = yong_hu_ming

            # 性别
            xing_bie = None
            comment_dict['xing_bie'] = xing_bie

            # 用户等级
            yong_hu_deng_ji = None
            comment_dict['yong_hu_deng_ji'] = yong_hu_deng_ji

            # 用户省份
            yong_hu_sheng_fen = item["ipInfo"]
            comment_dict['yong_hu_sheng_fen'] = yong_hu_sheng_fen

            # 抓取时间
            do_time = time.time()
            comment_dict['do_time'] = do_time

            # 抓取网站
            zhan_dian = u'新华网'
            comment_dict['zhan_dian'] = zhan_dian

            # 主键
            comment_dict['_id'] = str(ping_lun_id)+news_url

            #print json.dumps(comment_dict, ensure_ascii=False, indent=4)
            self.mongo.put_comment(comment_dict)


if __name__ == '__main__':
    comment = NewsComment()
    comment.run("http://news.xinhuanet.com/politics/2017-07/06/c_1121271158.htm", 1)
