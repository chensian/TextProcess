#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/18 13:05
# @Author  : chen
# @Site    : 
# @File    : data_util.py
# @Software: PyCharm
import os

import lda.utils


_test_dir = os.path.join(u"D:\python\workspace\TextProcess\segment\data", 'lda')


def load_annals():
    annals_ldac_fn = os.path.join(_test_dir, 'annals.lda-c')
    return lda.utils.ldac2dtm(open(annals_ldac_fn), offset=0)


def load_annals_vocab():
    annals_vocab_fn = os.path.join(_test_dir, 'annals.tokens')
    with open(annals_vocab_fn) as f:
        vocab = tuple(f.read().split())
    return vocab


def load_annals_titles():
    annals_titles_fn = os.path.join(_test_dir, 'annals.titles')
    with open(annals_titles_fn) as f:
        titles = tuple(line.strip() for line in f.readlines())
    return titles
