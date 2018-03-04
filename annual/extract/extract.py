#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/11 12:54 
# @Author  : chesian
# @Site    : 
# @File    : extract.py
# @Software: PyCharm


"""
单线程   处理  convert_pdf_2_text

"""

import os
from cStringIO import StringIO

from Queue import Queue

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage



# 将pdf转为text
def convert_pdf_2_text(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    with open(path, 'rb') as fp:
        for page in PDFPage.get_pages(fp, set()):
            interpreter.process_page(page)
        text = retstr.getvalue()
    device.close()
    retstr.close()
    return text


def consumer(queue):
    while True:
        fpathe, f = queue.get()
        if f is None:
            break
        path = os.path.join(fpathe,f)
        print path, "starting"

        meta = f.split("_")
        # pathTxT = os.path.join(u"G:/ARTEXT/", meta[1])
        pathTxT = os.path.join(u"G:/ARTEXT/", meta[0])
        dest_file = os.path.join(pathTxT, f +".txt")

        if os.path.exists(dest_file):
            print path, "has exist"
        else:
            try:
                text = convert_pdf_2_text(path)
                if not os.path.exists(pathTxT):
                    # 如果不存在则创建目录
                    # 创建目录操作函数
                    os.makedirs(pathTxT)

                with file(dest_file, "wb") as f:
                    f.write(text)
                print path, "done"
            except :
                print path, "has error"

def traverse():
    # path = u"G:/AR/2001to2014AR/AR2013-2014/"  f
    # path = u"G:/AR/2015AR_1/"    f
    # path = u"G:/AR/2015AR_4/"    f
    # path = u"G:/AR/2016ARpdf/"    f

    # path = u"G:/AR/2001to2014AR/1999-2000/"     f
    path = u"G:/AR/2001to2014AR/1999-2000/"
    # path = u"G:/AR/2001to2014AR/2010-2012/"
    # path = u"G:/AR/2001to2014AR/sh2001-2009/"     f
    # path = u"G:/AR/2001to2014AR/sz2001-2009/"

    # 遍历 path 下的所有文件
    # 父路径 文件夹 文件
    for fpathe,dirs,fs in os.walk(path):
        for f in fs:
            filenames_queue.put((fpathe, f))
            # print (fpathe, f)

    # print filenames_queue.qsize()

if __name__ == "__main__":
    filenames_queue = Queue()
    traverse()
    consumer(filenames_queue)
