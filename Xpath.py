# coding: utf-8
import re


def pathOneNode(tree, path):
    try:
        content = tree.xpath(path)
        return re.sub('\s', '', content[0].replace(u'来源：',''))
    except Exception as e:
        print 'Xpath解析错误:', e
        return None


def pathAllNode(tree, path):
    try:
        content = tree.xpath(path)
        return re.sub('\s| ', '', content[0].xpath('string(.)'))
    except Exception as e:
        print 'Xpath解析错误:', e
        return None

def pathForPhoto(tree, path):
    try:
        content = tree.xpath(path)
        return content
    except Exception as e:
        print 'Xpath解析错误:', e
        return None
