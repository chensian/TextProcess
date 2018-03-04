#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/9 12:35 
# @Author  : chesian
# @Site    : 
# @File    : statistic.py
# @Software: PyCharm
import pandas as pd

output_path = "G:/Stock/output/"

# 统计 总词数
from annual.dataset.import_util import file_to_dict

def compute_word_num(name):

    path = "D:/python/workspace/TextProcess/segment/data/lda/"
    filename = name + ".lda-c"

    annual_word_pure_num = {}
    annual_word_num = {}
    data = open(path + filename).readlines()

    for key, annual in enumerate(data):
        annual = annual.split(" ")
        annual_word_pure_num[key] = annual[0]

        annual_word = annual[1:]

        # 统计不重复数
        word_num = 0
        for word2id_freq in annual_word:
            try:
                word_num += int(word2id_freq.split(":")[1])
            except:
                print key, word2id_freq
        annual_word_num[key] = word_num

    return annual_word_pure_num, annual_word_num


# 统计 总字数
def compute_char_num(name):
    path = "D:/python/workspace/TextProcess/dataset/output/seg/"
    filename = "seg_result_" + name + ".txt"
    data = open(path + filename).readlines()

    annual_char_num = {}

    for key, annual in enumerate(data):
        # print len(annual)
        annual = annual.replace(" ", "")
        annual_char_num[key] = len(annual) / 3
    return annual_char_num

# 合并  字数  次数
def turn_merge_char_word(name):

    annual_char_num = compute_char_num(name)
    annual_word_pure_num, annual_word_num = compute_word_num(name)

    id_path = "D:/python/workspace/TextProcess/dataset/output/csv/%s_file2id.csv"
    type = name.split("_")[1]
    file2id = pd.read_csv(id_path % type)
    # print file2id.columns

    file2id["word_pure_num"] = file2id["id"].apply(lambda x: annual_word_pure_num[x])
    file2id["word_num"] = file2id["id"].apply(lambda x: annual_word_num[x])
    file2id["char_num"] = file2id["id"].apply(lambda x: annual_char_num[int(x)])
    file2id.to_csv("D:/python/workspace/TextProcess/dataset/output/statistic/" + name +"_annual_statistic.csv", index=False)


# 匹配 单词
def match_word_freq(name, wordlist):

    # 1、  wordlist   to   idlist          need word2id

    path = "D:/python/workspace/TextProcess/segment/data/lda/"
    filename = name + ".tokens2id"
    word2id = file_to_dict(path, filename)
    # print word2id

    idlist = []
    for word in wordlist:
        # if word in word2id:
        for token in word2id:
            if token.find(word) != -1:
                print token, word2id[token]
                idlist.append(word2id[token])


    #  加载 lda 词统计库
    path = "D:/python/workspace/TextProcess/segment/data/lda/"
    filename = name + ".lda-c"
    data = open(path + filename).readlines()
    docs_freq_num = {}
    for key, annual in enumerate(data):

        annual = annual.split(" ")
        # id   freq
        annual_word = annual[1:]

        id_freq_dict = {}
        for word2id_freq in annual_word:
            item = word2id_freq.split(":")
            try:
                id_freq_dict[item[0]] = int(item[1])
            except:
                print key, word2id_freq

        freq_num = 0

        for id in idlist:
            if id in id_freq_dict:
                freq_num += id_freq_dict[id]
        docs_freq_num[key] = freq_num

    return docs_freq_num


# 合并  wordlist  在name 出现的次数
def merge_char_word(name):

    wordlist1 = ["丝绸之路", "一带一路"]
    wordlist2 = ["结构性改革", "供给侧改革"]
    wordlist3 = ["新常态"]

    id_path = "D:/python/workspace/TextProcess/dataset/output/csv/%s_file2id.csv"
    type = name.split("_")[1]
    file2id = pd.read_csv(id_path % type)
    # print file2id.columns

    docs_freq_num1 = match_word_freq(name, wordlist1)
    docs_freq_num2 = match_word_freq(name, wordlist2)
    docs_freq_num3 = match_word_freq(name, wordlist3)

    file2id["wordlist1"] = file2id["id"].apply(lambda x: docs_freq_num1[x])
    file2id["wordlist2"] = file2id["id"].apply(lambda x: docs_freq_num2[x])
    file2id["wordlist3"] = file2id["id"].apply(lambda x: docs_freq_num3[x])

    file2id.to_csv("D:/python/workspace/TextProcess/dataset/output/statistic/" + name +"_match_word_freq.csv", index=False)

if __name__ == "__main__":

    # name = "mda_mda"
    # name = "all_mda"
    name = "all_all"
    # turn_merge_char_word(name)

    merge_char_word(name)

