#coding:utf-8
from NewsMessage import NewsMessage
import sys
import time
import datetime
sys.path.append("..")

class Run(object):
    def __init__(self):
        self.News = NewsMessage()
    def run(self):
        self.News.getNewsMessage()


if __name__ == "__main__":
    run = Run()
    while(True):
        try:
            print u'开始'
            run.run()
        except Exception as e:
            print "RUNERROR:",e
        """获取睡眠时间"""
        print u'结束'
        today = datetime.datetime.now()
        tow = today + datetime.timedelta(days=1)
        tomorrow = datetime.datetime(tow.year, tow.month, tow.day, 21, 30)
        s = (tomorrow - today).total_seconds()
        time.sleep(int(s))
