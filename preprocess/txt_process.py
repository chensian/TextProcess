#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/6 23:25
# @Author  : chen
# @Site    : 
# @File    : TxtProcess.py
# @Software: PyCharm
import os

from simple_pdf import convert_pdf_to_txt
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def convert_dir_pdf_to_txt(src_dir, dest_dir):
    for dir_name in sorted(os.listdir(src_dir)):
        sub_src_dir = src_dir + "/" + dir_name
        print "dir ", sub_src_dir
        for filename in sorted(os.listdir(sub_src_dir)):
            src_file = sub_src_dir + "/" + filename

            sub_dest_dir = dest_dir + "/" + dir_name
            if not os.path.exists(sub_dest_dir):
                os.makedirs(sub_dest_dir)

            dest_file = sub_dest_dir + "/" + filename
            # print "file ", filename,
            convert_pdf_to_txt(src_file, dest_file)
            # print "src  ", src_file
            # print "dest ", dest_file
            # print "convert finish..."


if __name__ == '__main__':
    src_dir = u"G:/data/business/AStock/financial_report"
    dest_dir = u"G:/data/business/AStock/third_parse"
    convert_dir_pdf_to_txt(src_dir, dest_dir)
