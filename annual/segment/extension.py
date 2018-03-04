#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/9 14:11
# @Author  : chen
# @Site    :
# @File    : compare.py
# @Software: PyCharm
import gensim
from annual.dataset.import_util import list_to_txt, file_to_list, file_to_dict
from annual.segment.statistics import compute_account_freq

output_path = "G:/Stock/output/"

# 返回语料库 词汇 跟会计词汇的 交集
def join_dict(worddict_path, word_dict):
    '''
    word_dict_path = u"D:/python/workspace/TextProcess/similarity/model/"
    account_dict_path = u"D:/python/workspace/TextProcess/segment/worddict/
    :param word_dict:
    :param vacabulary:
    :return:
    '''

    # 语料库 词汇
    type_corpus_dict_name = output_path + "model/vocabulary"

    # 会计词汇
    account_dict_name = worddict_path + word_dict

    type_corpus_dict = file_to_dict("", type_corpus_dict_name)
    account_list = file_to_list("", account_dict_name)

    v1_set = set(type_corpus_dict.keys())
    account_set = set(account_list)

    return account_set.intersection(v1_set)


def extend_dict(worddict_path, word_dict):
    # 1、找到 词汇表 跟 vocal 共同的词
    account = join_dict(worddict_path, word_dict=word_dict)

    # 2、加载模型
    model = gensim.models.Word2Vec.load(output_path + 'model/word2vec_gensim')

    words = set()
    for word in account:
        words.add(word)
        # 3、使用 Word2Vec 语料空间 查找相似词
        for i in model.most_similar(unicode(word)):
            words.add(i[0])

    print len(words)
    # 4、保存
    extension_path = "G:/Stock/output/wordlist/extension/"
    list_to_txt(words, extension_path + "extend_" + word_dict)


if __name__ == '__main__':


    worddict_path = "G:/Stock/output/wordlist/row/"
    extension_path = "G:/Stock/output/wordlist/extension/"

    word_dict1 = "macro_economic_dict.txt"
    word_dict2 = "financial_account.txt"
    word_dict3 = "financial_market.txt"
    word_dict4 = "financial_taxation_policy.txt"
    word_dict5 = "inflation.txt"
    word_dict6 = "monetary_policy.txt"
    word_dict7 = "general_macro.txt"

    word_dicts = [word_dict1,word_dict2,word_dict3,word_dict4,word_dict5,word_dict6,word_dict7]
    for word_dict in word_dicts:

        # 1、 利用年报语料 扩展 会计词汇
        # extend_dict(worddict_path, word_dict)

        # 2、 计算每篇 年报语料 扩展 会计词汇 的出现次数
        extend_word_dict = "extend_" + word_dict
        compute_account_freq(extension_path, extend_word_dict)

