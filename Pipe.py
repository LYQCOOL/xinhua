# coding: utf-8

import pymongo

class MongoDB(object):
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        '''client = pymongo.MongoClient('182.150.37.55', 50070)'''
        db = client['news']
        self.collection_zhengwen = db['content']
        self.collection_comment = db['comment']

    def put_content(self, value):
        return self.collection_zhengwen.save(value)

    def put_comment(self, value):
        return self.collection_comment.save(value)
