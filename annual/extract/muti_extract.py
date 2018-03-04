#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/11 13:58 
# @Author  : chesian
# @Site    : 
# @File    : muti_extract.py
# @Software: PyCharm


"""
多进程  multiprocessing  处理  convert_pdf_2_text

"""


from cStringIO import StringIO

from multiprocessing import Process, JoinableQueue
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os





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

def producer(queue):
    path = u"G:/AR/"
    # 遍历 path 下的所有文件
    # 父路径 文件夹 文件
    for fpathe,dirs,fs in os.walk(path):
        for f in fs:
            queue.put((fpathe, f))

def consumer(queue):
    while True:
        fpathe, f = queue.get()
        path = os.path.join(fpathe,f)
        print path, "starting"
        if path is None:
            break
        text = convert_pdf_2_text(path)

        meta = f.split("_")
        pathTxT = os.path.join(u"G:/ARTEXT/", meta[0])
        if not os.path.exists(pathTxT):
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(pathTxT)

        with file(os.path.join(pathTxT, f +".txt"), "wb") as f:
            f.write(text)
        print path, "done"
        queue.task_done()




if __name__ == "__main__":

    queue = JoinableQueue()
    # Process(target=producer, args=(queue,)).start()

    producer(queue)
    print "producer done"
    for i in xrange(10):
        p = Process(target=consumer, args=(queue,))
        p.daemon = True
        p.start()


    queue.join()