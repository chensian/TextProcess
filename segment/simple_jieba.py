#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/25 20:37
# @Author  : chen
# @Site    : 
# @File    : simple_jieba.py
# @Software: PyCharm

# encoding=utf-8
import jieba
#
# seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式
#
# seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
# print(", ".join(seg_list))

# seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
# print(", ".join(seg_list))
from load.import_util import import_txt



def test_hmm():

    # text = import_txt(u"D:/python/workspace/TextProcess/dataset/output/txt/example/",u"2407409.PDF.txt")
    text = "________________________________________________________"
    print unicode(text)

    seg_list_1 = jieba.lcut(text, cut_all=False, HMM=False)
    seg_list_2 = jieba.lcut(text, cut_all=False, HMM=True)

    jieba.load_userdict(u"worddict/account_dict.txt")

    seg_list_3 = jieba.lcut(text, cut_all=False, HMM=False)
    seg_list_4 = jieba.lcut(text, cut_all=False, HMM=True)

    set1 = set(seg_list_1)
    set2 = set(seg_list_2)
    set3 = set(seg_list_3)
    set4 = set(seg_list_4)



    print "HMM    : baseline: ", " ".join(set2.difference(set1))
    print "词典   : baseline:", " ".join(set3.difference(set1))
    print "词典HMM: baseline:", " ".join(set4.difference(set1))
    print "词典HMM：词典    :", " ".join(set4.difference(set3))
    print "词典HMM: HMM     :", " ".join(set4.difference(set2))

    print "ddd:", " ".join(set3.difference(set1).difference(set4.difference(set2)))
    print "ddd:", " ".join(set4.difference(set3).difference(set2.difference(set1)))
    print "ddd:", " ".join(set2.difference(set1).difference(set4.difference(set3)))

test_hmm()


