#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/6 23:36
# @Author  : chen
# @Site    : 
# @File    : import.py
# @Software: PyCharm
import jieba
import re

import sys

from requests.packages import chardet

reload(sys)
sys.setdefaultencoding('utf-8')


def file_to_list(path, filename):
    with open(path + filename, "rb") as f:
        lines = f.readlines()
    txtList = []
    for line in lines:
        line = line.replace('\r', '').replace('\n', '')
        tokens = re.split(",| ", line)
        txtList.append(tokens[0])
    return txtList


def file_to_dict(path, filename):
    with open(path + filename, "rb") as f:
        lines = f.readlines()
    txt_dict = {}
    for line in lines:
        line = line.replace('\r', '').replace('\n', '')
        tokens = re.split(",| ", line)
        txt_dict[tokens[0]] = tokens[1]
    return txt_dict

def import_txt(path, filename):
    """
    读取文件 去除空行
    :param path:
    :param filename:
    :return:
    """
    print path, filename
    with open(path + filename, "rb") as f:
        lines = f.readlines()
    txtList = []
    # for line in lines[100:300]:
    # for line in lines[4: len(lines) - 1]:
    for line in lines:
        # print line
        if line.split():
            # txtList.append(line.strip() + "\n")
            line = line.replace('\t', '').replace('\n', '').replace(' ', '').replace('/n', '')
            # 停用词 处理
            # line=   line.replace('，', '').replace('。', '').replace('、', '').replace('；', '').replace('（', '').replace('）', '').replace('~"', '').replace('：', '').replace('《', '').replace('》', '').replace('[', '').replace(']', '').replace('”', '').replace('“', '').replace('(', '').replace(')', '').replace('‘', '').replace('’', '').replace('"', '').replace('—', '').replace('％', '').strip()
            # line = filter(lambda ch: ch not in "0123456789.=-+:,%", line)
            try:
                line = unicode(line)
            except UnicodeDecodeError:
                print "NO unicode:", path + filename, chardet.detect(line)
            # txtList.append(line)
            result = re.findall(u"[\u4e00-\u9fa5]+", line, re.I)
            if result is None:
                # print unicode(line)
                pass
            else:
                # print "".join(result),
                txtList.append("".join(result))
    # print "".join(txtList)
    f.close()
    return "".join(txtList)


def import_txt_xample():
    # importTxt("D:/python/workspace/TextProcess/output/", "2407409.PDF.txt")
    print import_txt(u"D:/python/workspace/TextProcess/input/", u"深发展Ａ2005年年度报告.txt")


import os
import codecs


def parse_file(filepath):
    try:
        lineList = []  # 存放每一行的内容
        with open(filepath, 'r') as fp:
            line = fp.read()
            if line.startswith('\xff\xfe'):
                encoding = 'utf-16-le'
                fp2 = codecs.open(filepath, 'r', encoding)
                lineList = fp2.readlines()
                fp2.stream.close()
        for i in lineList:  # 打印每一行
            print i,
    except Exception, ex:
        print '[ERROR]--', ex


def filter_util(filepath):
    try:
        with open(filepath, "rb") as f:
            f2 = open(filepath + "_new", "wb")
            lines = f.readlines()
            for line in lines:
                word = line.split(" ")
                print word[0], len(word[0])
                if len(word[0]) > 3:
                    f2.writelines(line)
    except Exception, ex:
        print '[ERROR]--', ex

def import_txt2utf8_row(path, filename):
    txtList = []
    print path + filename
    with open(path+ filename, "rb") as f:
        lines = f.readlines()
        for line in lines:
            try:
                line = unicode(line)
            except UnicodeDecodeError:
                with open(path+ filename, "rb") as f2:
                    read = f2.read()
                    print "NO unicode:", path + filename, chardet.detect(read)
                    encoding = chardet.detect(read)["encoding"]
                    if encoding:
                        read = read.decode(encoding)
                    read = read.encode("utf-8")
                    read = unicode(read)
                    result = re.findall(u"[\u4e00-\u9fa5]+", read, re.I)
                    if result is not None:
                        txtList.append("".join(result))
                    break
            result = re.findall(u"[\u4e00-\u9fa5]+", line, re.I)
            if result is not None:
                txtList.append("".join(result))
    return "".join(txtList)



def import_txt2utf8(path, filename):
    txtList = []
    print path + filename
    with open(path+ filename, "rb") as f:
        line = f.read()
        # print line
        try:
            line = unicode(line)
        except UnicodeDecodeError:
            print "NO unicode:", path + filename, chardet.detect(line)
            charset = chardet.detect(line)
            encoding = charset['encoding']
            # encoding = 'utf-16-le'
            # print(chardet.detect(line))
            # print line
            if encoding:
                line = line.decode(encoding)
            line = line.encode("utf-8")
            line = unicode(line)
            # txtList.append(line)
        result = re.findall(u"[\u4e00-\u9fa5]+", line, re.I)
        if result is None:
            # print unicode(line)
            pass
        else:
            # print "".join(result),
            txtList.append("".join(result))
        # print "".join(txtList)
    return "".join(txtList)

if __name__ == '__main__':
    # import_txt_xample()
    # filepath = u"D:/python/workspace/TextProcess/input/深发展Ａ2005年年度报告.txt"
    # parse_file(filepath)

    # line = "第九节    董事会报告 年本行的净利息收入增长了 %至  亿元人民币。"
    # line = line.replace('\t', '').replace('\n', '').replace(' ','')
    # print line

    # g过滤 单个词
    # filter_util(u"../similarity/model/vocabulary_2")
    # line = "343,2323"
    # print re.split(",| ", line)
    #
    # line = u"是滴是滴 343434 soiadfjiasjd 放松放松  .=-+:,% sdsd？。，、，、、（）【】{}"
    # print "".join(re.findall(ur"[\u4e00-\u9fa5]+", line, re.I))

    path = u"H:/data/business/AStock/parse/000155/"
    filename = u"川化股份：2011年年度报告.txt"
    print import_txt2utf8_row(path, filename)
    # d = "颠三倒四".encode("utf-8")
    # print type(d)
