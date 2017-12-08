#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/30 13:08 
# @Author  : chesian
# @Site    : 
# @File    : vocab_weight.py
# @Software: PyCharm
from load.import_util import file_to_dict, file_to_list
import pandas as pd
voca_path = "D:/python/workspace/TextProcess/similarity/voc/"
extend_words_path = "D:/python/workspace/TextProcess/segment/worddict/extension/"


def wordlist_wm_value(name, word_dict):

    # 计算 wordlist  word_freq 权重
    word_freq = {}

    wordlist = file_to_list(extend_words_path + name + "/", name +"_extend_" + word_dict)
    voca_freq = file_to_dict(voca_path, name + "_vocabulary")
    for word in wordlist:
        word_freq[word] = int(voca_freq[word])

    total_word_num =  sum(word_freq.values())


    # 1、  word_freq   to   idlist  weight         need   word2id, total_word_num    计算 得出 [idlist ， weight]
    path = "D:/python/workspace/TextProcess/segment/data/lda/"
    filename = name + ".tokens2id"
    word2id = file_to_dict(path, filename)
    # print word2id

    idlist_weight = {}
    for word in word_freq:
        if word in word2id:
            idlist_weight[word2id[word]] = (word_freq[word] * 1.0) / total_word_num

    # doc  宏观经济词汇的 权重值 加权平均和
    docs_wordlist_wm_value = {}

    #  加载 lda 词统计库
    path = "D:/python/workspace/TextProcess/segment/data/lda/"
    filename = name + ".lda-c"
    data = open(path + filename).readlines()
    for key, annual in enumerate(data):

        annual = annual.split(" ")

        total_annual_word = int(annual[0])
        if total_annual_word == 0:
            docs_wordlist_wm_value[key] = 0
            continue

        # id   freq
        annual_word = annual[1:]


        id_freq_dict = {}
        for word2id_freq in annual_word:
            item = word2id_freq.split(":")
            id_freq_dict[item[0]] = int(item[1])

        sum_weight = 0
        for id in idlist_weight:
            if id in id_freq_dict:
                sum_weight += id_freq_dict[id] * idlist_weight[id]

        docs_wordlist_wm_value[key] = sum_weight / total_annual_word

    return docs_wordlist_wm_value

# 合并  docs_wordlist_wm_value
def merge_wordlist_wm_value(name):


    id_path = "D:/python/workspace/TextProcess/dataset/output/csv/%s_file2id.csv"
    type = name.split("_")[1]
    file2id = pd.read_csv(id_path % type)
    # print file2id.columns

    word_dict1 = "macro_economic_dict.txt"
    word_dict2 = "financial_account.txt"
    word_dict3 = "financial_market.txt"
    word_dict4 = "financial_taxation_policy.txt"
    word_dict5 = "inflation.txt"
    word_dict6 = "monetary_policy.txt"
    word_dict7 = "general_macro.txt"

    # word_dicts = [word_dict1,word_dict2,word_dict3,word_dict4,word_dict5,word_dict6,word_dict7]
    word_dicts = [word_dict1]
    for word_dict in word_dicts:
        docs_wordlist_wm_value = wordlist_wm_value(name, word_dict)
        file2id["macro_economic_value"] = file2id["id"].apply(lambda x: docs_wordlist_wm_value[x])
        file2id.to_csv("D:/python/workspace/TextProcess/dataset/output/statistic/" + name +"_" + word_dict.split(".")[0] +"_wm_value.csv", index=False)



if __name__ == "__main__":
    # name = "mda_mda"
    # name = "all_mda"
    name = "all_all"

    merge_wordlist_wm_value(name)
