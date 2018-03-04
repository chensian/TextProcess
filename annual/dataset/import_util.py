#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/23 12:07 
# @Author  : chesian
# @Site    : 
# @File    : import_util.py
# @Software: PyCharm
import codecs
import re
from requests.packages import chardet

def file_to_list(path, filename):
    with codecs.open(path + filename, "rb", "utf-8") as f:
        lines = f.readlines()
    txtList = []
    for line in lines:
        line = line.replace('\r', '').replace('\n', '')
        tokens = re.split(",| ", line)
        txtList.append(tokens[0])
    return txtList


def file_to_dict(path, filename):
    with codecs.open(path + filename, "rb", "utf-8") as f:
        lines = f.readlines()
    txt_dict = {}
    for line in lines:
        line = line.replace('\r', '').replace('\n', '')
        tokens = re.split(",| ", line)
        txt_dict[tokens[0]] = tokens[1]
    return txt_dict

def import_txt2utf8_row(path, filename):
    txtList = []
    print path + filename
    with codecs.open(path+ filename, "rb", "utf-8") as f:
        lines = f.readlines()
        # for line in lines:
        # 特殊格式输出 4：len(lines) - 1
        for line in lines[4: len(lines) - 1]:
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
                    result = re.findall(u"[\u4e00-\u9fa5]+", read, re
                                        .I)
                    if result is not None:
                        txtList.append("".join(result))
                    break
            result = re.findall(u"[\u4e00-\u9fa5]+", line, re.I)
            if result is not None:
                txtList.append("".join(result))
    return "".join(txtList)

def dict_to_txt(data_dict, file, key=True, value=True):
    if data_dict is None:
        print "no data!"
    else:
        with codecs.open(file, "a","utf-8") as f:
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

def list_to_txt(data_list, file):
    if data_list is None:
        print "no data!"
    else:
        with codecs.open(file, "a", "utf-8") as f:
            for row in data_list:
                f.write(row + "\n")

if __name__ == "__main__":
    # func()
    pass

