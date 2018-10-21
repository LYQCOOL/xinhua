# coding: utf-8

import pymongo

class huanCun(object):
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        '''client = pymongo.MongoClient('182.150.37.55', 50070)'''
        db = client['news']
        self.collection_zhuizong = db['zhuiZong']
    def put_zhuizong(self, value):
        return self.collection_zhuizong.save(value)

