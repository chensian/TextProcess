#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/8 15:31
# @Author  : chen
# @Site    : 
# @File    : extract_tags.py.py
# @Software: PyCharm
import sys
from collections import Counter

from load.import_util import importTxt

sys.path.append('../')

import jieba
import jieba.analyse
from optparse import OptionParser

def cmd():
    USAGE = "usage:    python extract_tags.py [file name] -k [top k]"

    parser = OptionParser(USAGE)
    parser.add_option("-k", dest="topK")
    opt, args = parser.parse_args()


    if len(args) < 1:
        print(USAGE)
        sys.exit(1)

    file_name = args[0]

    if opt.topK is None:
        topK = 10
    else:
        topK = int(opt.topK)

    content = open(file_name, 'rb').read()

    tags = jieba.analyse.extract_tags(content, topK=topK)

    print(",".join(tags))


if __name__ == '__main__':
    content = importTxt("D:/python/workspace/TextProcess/output/", "2407409.PDF.txt")
    topK = 20
    tags = jieba.analyse.extract_tags(content, topK=topK)
    print(",".join(tags))

    tags = jieba.analyse.extract_tags(content, topK=topK, withWeight=True)

    for tag in tags:
        print("tag: %s\t\t weight: %f" % (tag[0],tag[1]))

