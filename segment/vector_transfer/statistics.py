# -*- coding: utf-8 -*-
# @Time    : 2017/7/16 23:55
# @Author  : chen
# @Site    :
# @File    : vector_util.py
# @Software: PyCharm
import pandas as pd

from load.import_util import file_to_dict, file_to_list


def deal_ida_format(types):
    # f = open("D:/python/workspace/TextProcess/segment/data/lda/one-annals.lda-c", "r")
    f = open("D:/python/workspace/TextProcess/segment/data/lda/"+ types +".lda-c", "r")

    total_words_nums = []
    total_words_freq = []
    for line in f.readlines():
        datas = line.split()
        total_words_nums.append(datas[0])
        word_freq = {}
        for data in datas:
            dict = data.split(":")
            if len(dict) == 2:
                word_freq[dict[0]] = dict[1]
        total_words_freq.append(word_freq)

    # print total_words_nums
    # for key in total_words_freq:
    #     print key

    return total_words_nums, total_words_freq


# deal_ida_format()

# all_extend_dict left join tokens2

def account_dict2id(worddict_path, word_dict, types):
    all_extend_ids = {}

    lda_path = "D:/python/workspace/TextProcess/segment/data/lda/"
    v1_tokens2id = file_to_dict(lda_path, types + ".tokens2id")

    all_extend_list = file_to_list(worddict_path, word_dict)

    for word in all_extend_list:
        if word in v1_tokens2id:
            all_extend_ids[word] = v1_tokens2id[word]

    # for word in all_extend_ids:
    #     print word, all_extend_ids[word]
    # print len(all_extend_ids)

    return all_extend_ids


# account_dict2id()

def compute_account_freq(worddict_extend_path, word_dict, types):
    all_extend_ids = account_dict2id(worddict_extend_path, word_dict, types)
    # ids_set = all_extend_ids.keys()
    ids_set = set(all_extend_ids.values())

    pure_words_nums, total_words_freq = deal_ida_format(types)

    nums = []
    total_words_nums = []
    join_words = []
    for words_freq in total_words_freq:
        words_num = 0
        for freq in words_freq.values():
            words_num += int(freq)
        total_words_nums.append(words_num)

        num = 0
        key_set = set(words_freq.keys())
        join_set = ids_set.intersection(key_set)
        join_words.append(len(join_set))
        for id in join_set:
            num += int(words_freq[id])

        nums.append(num)
    st = pd.DataFrame(data={"MDA总词数": total_words_nums, "(MDA中)宏观词汇个数": nums, "纯的MDA总词数": pure_words_nums,
                            "纯的(MDA中)宏观词汇个数": join_words})

    file2id = pd.read_csv(
        "D:/python/workspace/TextProcess/dataset/output/csv/" + types.split("_")[1] + "_file2id.csv",
        dtype={'code': str})
    statistic = file2id.join(st, on="id")
    statistic.to_csv(
        "D:/python/workspace/TextProcess/segment/statistic/" + types + "/" + word_dict.split(".")[0] + ".csv")

    # print total_words_nums
    # print nums


#
# def connect_id():
#     median_file2id = pd.read_csv("../../dataset/output/txt/v1_file2id.csv", dtype={'code':str})
#     st = pd.read_csv("st.csv")
#
#     statistic = median_file2id.merge(st, on="id")
#     statistic.to_csv("statistic.csv")

if __name__ == '__main__':
    # connect_id()
    compute_account_freq()
