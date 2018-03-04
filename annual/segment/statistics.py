# -*- coding: utf-8 -*-
# @Time    : 2017/7/16 23:55
# @Author  : chen
# @Site    :
# @File    : vector_util.py
# @Software: PyCharm
import codecs

import pandas as pd

from annual.segment.vocab_weight import wordlist_wm_value
from load.import_util import file_to_dict, file_to_list

output_path = "G:/Stock/output/"

def deal_ida_format():
    f = codecs.open(output_path + "lda/seg_result_mda.lda-c", "r")
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

    return total_words_nums, total_words_freq


# deal_ida_format()
# all_extend_dict left join tokens2
# 会计词汇 对应 在词汇表的 id
def account_dict2id(worddict_path, word_dict):
    extend_ids = {}
    tokens2id = file_to_dict(output_path + "lda/", "seg_result_mda.tokens2id")
    extend_list = file_to_list(worddict_path, word_dict)

    for word in extend_list:
        # print word
        if word in tokens2id:
            extend_ids[word] = tokens2id[word]
    print len(extend_ids)
    return extend_ids


# account_dict2id()
# 统计词频
def compute_account_freq(worddict_extend_path, word_dict):
    extend_ids = account_dict2id(worddict_extend_path, word_dict)
    # ids_set = all_extend_ids.keys()
    ids_set = set(extend_ids.values())
    pure_words_nums, total_words_freq = deal_ida_format()

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

    file2id = pd.read_csv(output_path + "seg/file2id.csv",dtype={'code': str})
    statistic = file2id.join(st, on="id")


    # 加入 WM value
    # docs_wordlist_wm_value = wordlist_wm_value("seg_result_mda", word_dict)
    # statistic["macro_economic_value"] = statistic["id"].apply(lambda x: docs_wordlist_wm_value[x])

    statistic.to_csv(output_path + "statistic/" + word_dict.split(".")[0] + ".csv")

if __name__ == '__main__':
    # connect_id()
    # compute_account_freq()
    pass
