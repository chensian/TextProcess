#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/9 14:11
# @Author  : chen
# @Site    : 
# @File    : compare.py
# @Software: PyCharm
from load.import_util import file_to_list, file_to_dict


def join_dict(worddict_path, word_dict, vacabulary):
    '''
    word_dict_path = u"D:/python/workspace/TextProcess/similarity/model/"
    account_dict_path = u"D:/python/workspace/TextProcess/segment/worddict/
    :param word_dict:
    :param vacabulary:
    :return:
    '''
    v1_dict_name = u"D:/python/workspace/TextProcess/similarity/voc/" + vacabulary + "_vocabulary"
    account_dict_name = worddict_path + word_dict

    v1_dict = file_to_dict("", v1_dict_name)
    v1_list = v1_dict.keys()

    account_list = file_to_list("", account_dict_name)

    v1_set = set(v1_list)
    account_set = set(account_list)

    return account_set.intersection(v1_set)



def compute_dict_join():

    v1_dict_name = u"D:/python/workspace/TextProcess/similarity/model/vv1_vocabulary"
    v2_dict_name = u"D:/python/workspace/TextProcess/similarity/model/v1_vocabulary"
    account_dict_name = u"D:/python/workspace/TextProcess/segment/worddict/macro_economic_dict.txt"

    v1_dict = file_to_dict("", v1_dict_name)
    v1_list = v1_dict.keys()

    v2_dict = file_to_dict("", v2_dict_name)
    v2_list = v2_dict.keys()


    account_list = file_to_list("", account_dict_name)

    for i in v2_list[0:10]:
        print i
    #
    # for i in account_list[0:10]:
    #     print i

    v1_set = set(v1_list)
    v2_set = set(v2_list)
    account_set = set(account_list)

    print len(v1_set), len(account_set)

    print len(v2_set.difference(v1_set))
    print len(v1_set.difference(v2_set))
    # print len(v1_set.difference(account_set))

    # for key in account_set.intersection(v1_set):
    for key in v2_set.difference(v1_set):
        print key, v1_dict[key]
        print key

    # for key in account_set.difference(v1_set):
    #     # print key, v1_dict[key]
    #     print key

# compute_dict_join()
if __name__ == '__main__':

    join = join_dict()
    print len(join)
    for key in join:
        print key