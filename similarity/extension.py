#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/9 14:11
# @Author  : chen
# @Site    :
# @File    : compare.py
# @Software: PyCharm
import gensim

from load.export_util import list_to_txt
from segment.compare import join_dict
from segment.vector_transfer.statistics import compute_account_freq


def extend_dict(worddict_path, word_dict, types):
    #


    account = join_dict(worddict_path, word_dict=word_dict, vacabulary=types)
    model = gensim.models.Word2Vec.load('model/' + types + '_word2vec_gensim')

    words = set()
    for word in account:
        # print "*" * 40
        # print word
        words.add(word)
        for i in model.most_similar(unicode(word)):
            # print i[0], i[1]
            words.add(i[0])

    # words.extend(account)
    print len(words)
    extension_path = "D:/python/workspace/TextProcess/segment/worddict/extension/" + types + "/"
    list_to_txt(words, extension_path + types + "_extend_" + word_dict)


if __name__ == '__main__':
    # types = "all_mda"
    # types = "mda_mda"
    types = "all_all"

    worddict_path = "D:/python/workspace/TextProcess/segment/worddict/row/"
    worddict_extend_path = "D:/python/workspace/TextProcess/segment/worddict/extension/" + types + "/"

    word_dict1 = "macro_economic_dict.txt"
    word_dict2 = "financial_account.txt"
    word_dict3 = "financial_market.txt"
    word_dict4 = "financial_taxation_policy.txt"
    word_dict5 = "inflation.txt"
    word_dict6 = "monetary_policy.txt"
    word_dict7 = "general_macro.txt"

    word_dicts = [word_dict1,word_dict2,word_dict3,word_dict4,word_dict5,word_dict6,word_dict7]
    for word_dict in word_dicts:
        extend_dict(worddict_path, word_dict, types=types)
        # extend_word_dict = types + "_extend_" + word_dict
        # compute_account_freq(worddict_extend_path, extend_word_dict , types)
        # compute_account_freq(worddict_path, word_dict , types)
