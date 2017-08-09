#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/8 17:05
# @Author  : chen
# @Site    : 
# @File    : export_util.py
# @Software: PyCharm

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def list_to_txt(data_list, file):
    if data_list is None:
        print "no data!"
    else:
        with open(file, "a") as f:
            for row in data_list:
                f.write(row + "\n")


def dict_to_txt(data_dict, file, key=True, value=True):
    if data_dict is None:
        print "no data!"
    else:
        with open(file, "a") as f:
            lines = []
            data_list = sorted(data_dict.items(), key=lambda d: d[1])
            # print data_dict
            for list in data_list:
                if key and value:
                    lines.append(list[0] + "," + str(list[1]) + "\n")
                else:
                    if key:
                        lines.append(list[0] + "\n")
                    if value:
                        lines.append(list[1] + "\n")
            f.writelines(lines)

def merge_file():

    f1 = open(u"D:/python/workspace/TextProcess/dataset/output/seg/seg_result_all_1.txt")
    f2 = open(u"D:/python/workspace/TextProcess/dataset/output/seg/seg_result_all_2.txt")

    f3 = "D:/python/workspace/TextProcess/dataset/output/seg/seg_result_all_new.txt"
    with open(f3, "a") as f:
        f.writelines(f1.readlines())
        f.writelines(f2.readlines())

    f1.close()
    f2.close()

def unicode_tran():
    lines = open('D:/python/workspace/TextProcess/dataset/output/seg/seg_result_all_new.txt').readlines()
    f = open('D:/python/workspace/TextProcess/dataset/output/seg/seg_result_all.txt', "a")
    for line in lines:
        row = []
        for word  in line.split():
            try:
                word = unicode(word)
            except:
                print word
                word=""
            row.append(word)
        f.write(" ".join(row) + "\n")
    f.close()

if __name__ == '__main__':
    # merge_file()
    # unicode_tran()

    print len(open('D:/python/workspace/TextProcess/dataset/output/seg/seg_result_mda.txt').readlines())


