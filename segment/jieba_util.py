#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/6 23:34
# @Author  : chen
# @Site    : 
# @File    : jieba.py
# @Software: PyCharm
import json
import os
from collections import Counter

import jieba
import sys

import logging

from load.export_util import list_to_txt
from load.import_util import import_txt, file_to_list, import_txt2utf8, import_txt2utf8_row

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def mode():
    seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
    print("Full Mode: " + "/ ".join(seg_list))  # 全模式

    seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
    print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

    seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
    print(", ".join(seg_list))

    seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
    print(", ".join(seg_list))


def cut_string(txt_str):
    seg_list_1 = jieba.cut_for_search(txt_str)  # 搜索引擎模式
    seg_list_2 = jieba.cut(txt_str, cut_all=False)  # 精确模式 default
    seg_list_3 = jieba.cut(txt_str, cut_all=True)  # 全模式
    print(" | ".join(seg_list_1))
    print(" | ".join(seg_list_2))
    print("|".join(seg_list_3))
    return seg_list_1


def word_fred(txt_str):
    """
    分词str 并统计词频
    :param txt_str:
    :return:
    """
    # dict_name = u"worddict/account_dict.txt"
    dict_name = u"worddict/test_vocabulary"
    jieba.load_userdict(dict_name)
    seg_list = jieba.cut_for_search(txt_str)
    cnt = Counter()
    for word in seg_list:
        cnt[word] += 1

    cnt = sorted(cnt.iteritems(), key=lambda d: d[1], reverse=True)
    print json.dumps(cnt, ensure_ascii=False)
    # print "/n".join([str(num) for num in cnt.values()])
    # print "/n".join(cnt)
    # # list_to_txt(cnt, "word_fred.txt")
    json.dump(cnt, open("word_fred.json", "w"), ensure_ascii=False)


def file_segment(input_file, stop_words, f2):
    '''
    :param input_file: 输入的文件
    :param output_file: 输出分词后的语料库
    :param stop_words: 停止词
    :return:
    '''

    txt_str = import_txt2utf8_row("", input_file)
    seg_list = jieba.cut(txt_str, cut_all=False)
    result_list = []
    for word in seg_list:
        if len(word) > 1:
            # print type(word), type(stop_words.pop())
            str_word = str(word)
            if str_word not in stop_words:
                result_list.append(word)

    # cnt = Counter()
    # for word in seg_list:
    #     cnt[word] += 1
    f2.write(" ".join(result_list) + "\n")


def test_cut_string():
    txt_str = import_txt2utf8("H:/data/business/AStock/parse/600623/", u"轮胎橡胶2003年年度报告.txt")
    seg_list = jieba.cut(txt_str, cut_all=False)
    print " ".join(seg_list)


def test_file_segment():
    dict_name = u"../similarity/voc/all_vocabulary"
    jieba.load_userdict(dict_name)

    # src_dir = u"H:/data/business/AStock/median"
    src_dir = u"H:/data/business/AStock/parse"
    dest_dir = u"D:/python/workspace/TextProcess/dataset/output/seg/"
    i = 0
    stop_words = file_to_list(u"../segment/worddict/", u"stop_dict.txt")
    stop_words = set(stop_words)
    f2 = open(dest_dir + "seg_result_all_all.txt", 'a')
    for filename in sorted(os.listdir(src_dir)):
        sub_src_dir = os.path.join(src_dir, filename)
        # sub_src_dir += "/v1"
        try:
            for filename in sorted(os.listdir(sub_src_dir)):
                src_file = os.path.join(sub_src_dir, filename)

                i += 1
                if i > 14458:
                    # print src_file
                # print src_file
                # print stop_words
                    file_segment(src_file, stop_words, f2)
        except WindowsError:
            print "ERROR", sub_src_dir
    f2.close()


if __name__ == '__main__':
    # test_cut_string()
    test_file_segment()


    # stop_words = file_to_list(u"../segment/worddict/", u"stop_dict.txt")
    #
    # seg_list = " 变化 使得 本行 中国 会计准则 列报 之下 净资产 接近 国际标准 本行 管理层 决定 提前 采用 关于 外汇交易 会计准则 并且 一次 本行 本年度 营业费用 增加 亿元 人民币 尽管 费用".split()

    # print set(stop_words)
