#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/6 21:02
# @Author  : chen
# @Site    : 
# @File    : simplePDF.py
# @Software: PyCharm
import os
from cStringIO import StringIO

import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


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

def convert_pdf_to_txt(src_filename, dest_filename):
    # src_dir = u"G:/data/business/AStock/scripts/chen/input/"
    # dest_dir = u"G:/data/business/AStock/scripts/chen/output/"
    # filename = '2407409.PDF'
    # filename = u'S深发展A：2006年年度报告.PDF'
    with file(dest_filename +".txt", "wb") as f:
        f.write(convert_pdf_2_text(src_filename))

if __name__ == '__main__':

    src_dir = u"G:/data/business/AStock/financial_report"
    dest_dir = u"G:/data/business/AStock/third_parse"
    # filename = '2407409.PDF'
    filename = u'S深发展A：2006年年度报告.PDF'
    src_file =src_dir + filename
    with file(dest_dir + filename+".txt", "wb") as f:
        f.write(convert_pdf_2_text(src_file))
