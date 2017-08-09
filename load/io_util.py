#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/9 14:11
# @Author  : chen
# @Site    :
# @File    : compare.py
# @Software: PyCharm
import os
import re

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def list_dir(src_dir):
    file2id = []

    # f = open("../dataset/output/csv/all_file2id.csv", "a")
    f = open("../dataset/output/csv/mda_file2id.csv", "a")
    f.write("id,code,filename,year\n")
    i = -1
    for sub_dir in sorted(os.listdir(src_dir)):
        sub_src_dir = os.path.join(src_dir, sub_dir)
        sub_src_dir += "/v1"
        try:
            for filename in sorted(os.listdir(sub_src_dir)):

                row = []

                src_file = os.path.join(sub_src_dir, filename)
                # print src_file
                # print stop_words
                i += 1
                try:
                    year = re.findall("\d{4}", filename)[0]
                except:
                    print filename
                    year = 0
                row.append(str(i))
                row.append(str(sub_dir))
                row.append(str(src_file))
                row.append(str(year))

                f.write(",".join(row) + "\n")
        except WindowsError:
            print "ERROR", sub_src_dir


def convert_pdf_dir(src_dir):
    for sub_dir in sorted(os.listdir(src_dir)):
        sub_src_dir = os.path.join(src_dir, sub_dir)
        try:
            for filename in sorted(os.listdir(sub_src_dir)):
                print filename
        except:
            print "ss"


if __name__ == '__main__':
    # src_dir = u"H:/data/business/AStock/parse"
    src_dir = u"H:/data/business/AStock/median"
    list_dir(src_dir=src_dir)

    # f =open("D:\python\workspace\TextProcess\dataset\output\seg\seg_result_v1.txt", "r")
    # print len(f.readlines())
