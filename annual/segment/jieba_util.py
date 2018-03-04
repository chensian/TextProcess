#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/23 12:15 
# @Author  : chesian
# @Site    : 
# @File    : jieba_util.py.py
# @Software: PyCharm


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/6 23:34
# @Author  : chen
# @Site    :
# @File    : jieba.py
# @Software: PyCharm
import codecs
import os
import jieba
import logging
import pandas as pd
from annual.dataset.import_util import import_txt2utf8_row, file_to_list

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

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
            if word not in stop_words:
                result_list.append(word)
    f2.write(" ".join(result_list) + "\n")

def test_cut_string():
    txt_str = import_txt2utf8_row("G:/Stock/median/2005/", u"2005_1.pdf.txt")
    seg_list = jieba.cut(txt_str, cut_all=False)
    print " ".join(seg_list)

def file2id():

    filenames = []
    codess = []
    yearss = []
    src_dir = u"G:/Stock/median/"
    for src_filename in sorted(os.listdir(src_dir)):
        sub_src_dir = os.path.join(src_dir, src_filename)
        print src_filename

        for filename in sorted(os.listdir(sub_src_dir)):
            src_file = os.path.join(sub_src_dir, filename)
            # print src_file
            filename = filename.split("_")
            if src_filename == "2015":
                codess.append(filename[1].split(".")[0])
                yearss.append(str(int(filename[0])-1))
            elif src_filename == "2016":
                codess.append(filename[0].split(".")[0])
                yearss.append(filename[1])
            else:
                codess.append(filename[1].split(".")[0])
                yearss.append(filename[0])

    file2id = pd.DataFrame({"code": codess, "year":yearss})
    file2id.to_csv("G:/Stock/output/seg/file2id.csv")


def segment():
    dict_name = u"G:/Stock/output/wordlist/all_vocabulary"
    jieba.load_userdict(dict_name)
    src_dir = u"G:/Stock/median/"
    dest_dir = u"G:/Stock/output/seg/"
    i = 0
    stop_words = file_to_list(u"G:/Stock/output/wordlist/", u"stop_dict.txt")
    stop_words = set(stop_words)
    f2 = codecs.open(dest_dir + "seg_result_mda.txt", 'a', "utf-8")
    for filename in sorted(os.listdir(src_dir)):
        sub_src_dir = os.path.join(src_dir, filename)
        try:
            for filename in sorted(os.listdir(sub_src_dir)):
                src_file = os.path.join(sub_src_dir, filename)
                i += 1
                if i > 0:
                    file_segment(src_file, stop_words, f2)
                    print src_file, "complete!!!"
        except WindowsError:
            print "ERROR", sub_src_dir
    f2.close()

if __name__ == '__main__':
    # 测试分词
    # test_cut_string()
    #
    # segment()

    # file to id
    file2id()





