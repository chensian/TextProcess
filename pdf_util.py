#!/usr/bin/env python
# -*- coding: utf8 -*-
# @Time    : 2017/7/3 21:54
# @Author  : chen
# @Site    : 
# @File    : PDFUtil.py
# @Software: PyCharm
from layout_scanner import get_pages
import io_utils as io


def convertPDFToTxt(src_file, dest_dir, filename):
    pages = get_pages(src_file, None)
    if pages is not None:
        plain_text = []
        for page in pages:
            plain_text.append(page.strip())

        io.write_file(dest_dir, io.generate_txt_name(filename), ''.join(plain_text))

        print 'finished parsing ', len(plain_text) ,' to ', (dest_dir + filename).decode('gbk')
    else:
        print 'None pages in ', src_file.decode('gbk')


if __name__ == '__main__':
    import sys

    src_dir = "G:/data/business/AStock/scripts/chen/input/"
    dest_dir = "G:/data/business/AStock/scripts/chen/output/"
    # filename = 'S深发展A：2006年年度报告.PDF'.decode('utf-8').encode(sys.getfilesystemencoding())
    filename = '2407409.PDF'.decode('utf-8').encode(sys.getfilesystemencoding())
    # print filename
    # with file(dest_dir + filename, "wb") as f:
    #     f.write("sss")
    src_file =src_dir + filename
    convertPDFToTxt(src_file, dest_dir, filename)