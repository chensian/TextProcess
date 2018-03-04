# -*- coding: utf-8 -*-
# @Time    : 2017/7/16 23:55
# @Author  : chen
# @Site    :
# @File    : vector_util.py
# @Software: PyCharm

# Corpora and Vector Spaces
import codecs
import json
import logging
import sys

from gensim import corpora
from gensim.models import word2vec

from annual.dataset.import_util import dict_to_txt

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

data_path = "G:/Stock/output/"

def corpora_util():

    dictionary = corpora.Dictionary(line.split() for line in codecs.open(data_path + u"seg/seg_result_mda.txt", "r", "utf-8"))
    class MyCorpus(object):
        def __iter__(self):
             for line in codecs.open(data_path + u"seg/seg_result_mda.txt", "r", "utf-8"):
                 # assume there's one document per line, tokens separated by whitespace
                 yield dictionary.doc2bow(line.split())

    corpus_memory_friendly = MyCorpus()  # doesn't load the corpus into memory!
    # json.dump(dictionary.token2id, codecs.open(data_path + u"lda/seg_result_mda.tokens2id", "w", "utf-8"), ensure_ascii=False)
    dict_to_txt(dictionary.token2id, data_path + u"lda/seg_result_mda.tokens2id")
    # corpora.BleiCorpus.serialize(data_path + u"lda/seg_result_mda.lda-c", corpus_memory_friendly)

def operate_corpus():
    corpus = corpora.MmCorpus(data_path + u"mm/deerwester.mm")
    corpora.BleiCorpus.serialize(data_path + u"lda/corpus.lda-c", corpus)

def text_wordv2c_util():
    sentences = word2vec.Text8Corpus(data_path + u"seg/seg_result_mda.txt")
    model = word2vec.Word2Vec(sentences, min_count=5, size=100)
    model.save(data_path + u"model/word2vec_gensim")
    # model  = word2vec.Word2Vec.load(data_path + "model/word2vec_gensim")
    model.save_word2vec_format(data_path + "model/word2vec_org", fvocab=data_path + "model/vocabulary",
                                  binary=False)

if __name__ == '__main__':

    # 统计词汇 word-2-bag
    corpora_util()

    # 保存模型 和加载模型
    # operate_corpus()

    # 使用word2vec  构建 word 向量空间
    # text_wordv2c_util()
