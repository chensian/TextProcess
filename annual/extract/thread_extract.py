#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/11 14:38 
# @Author  : chesian
# @Site    : 
# @File    : thread_extract.py
# @Software: PyCharm

"""
多线程   threading  处理  convert_pdf_2_text

"""

import os
from cStringIO import StringIO
from threading import Thread

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

from Queue import Queue
filenames_queue = Queue()


# PDF转换 线程，  不断的从queue 拿 path 转换
class ConvertWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = filenames_queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            fpathe, f = self.queue.get()
            path = os.path.join(fpathe,f)
            if path is None:
                break
            print path, "starting"
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
            self.queue.task_done()



def traverse():
    path = u"G:/AR/"
    # 遍历 path 下的所有文件
    # 父路径 文件夹 文件
    for fpathe,dirs,fs in os.walk(path):
        for f in fs:
            filenames_queue.put((fpathe, f))
            # print (fpathe, f)

            # print filenames_queue.qsize()

if __name__ == "__main__":

    traverse()

    # Create 8 worker threads
    for x in range(10):
        worker = ConvertWorker(filenames_queue)
        # Setting daemon to True will let the main thread exit even though the
        # workers are blocking
        worker.daemon = True
        worker.start()



