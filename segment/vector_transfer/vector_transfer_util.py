# -*- coding: utf-8 -*-
# @Time    : 2017/7/16 23:55
# @Author  : chen
# @Site    :
# @File    : vector_util.py
# @Software: PyCharm

# Corpora and Vector Spaces
import logging
import sys


from load.export_util import dict_to_txt

reload(sys)
sys.setdefaultencoding('utf-8')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# types = "mda_mda"
# types = "all_mda"
types = "all_all"

from gensim import corpora

def formal(line):
    row = []
    for word in line.split():
        try:
            word = unicode(word)
            row.append(word)
        except:
            print word
    # print word
    return row

dictionary = corpora.Dictionary(formal(line) for line in open("D:/python/workspace/TextProcess/dataset/output/seg/seg_result_" + types+ ".txt"))
# pprint(texts)

class MyCorpus(object):
    def __iter__(self):
         for line in open(u"D:/python/workspace/TextProcess/dataset/output/seg/seg_result_" + types+ ".txt"):
             # assume there's one document per line, tokens separated by whitespace
             yield dictionary.doc2bow(line.split())

corpus_memory_friendly = MyCorpus()  # doesn't load the corpus into memory!
# print(corpus_memory_friendly)
#
# for vector in corpus_memory_friendly:  # load one vector into memory at a time
#     print(vector)

# dict_to_txt(dictionary.token2id, u"../data/lda/" + types+ ".tokens", value=False)
dict_to_txt(dictionary.token2id, u"../data/lda/" + types+ ".tokens2id")
corpora.BleiCorpus.serialize(u"../data/lda/" + types+ ".lda-c", corpus_memory_friendly)




def save_corpora(types, formal):
    documents = file(u"D:/python/workspace/TextProcess/dataset/output/seg/seg_result_" + types + ".txt").readlines()

    # stoplist = set('for a of the and to in'.split())
    # stop_words = file_to_list(u"../worddict/", u"stop_dict.txt")

    texts = [[word for word in document.split()] for document in documents]

    # pprint(texts)
    dictionary = corpora.Dictionary(texts)

    # dictionary.save("seg_result.dict")
    #
    # dictionary = corpora.Dictionary.load("seg_result.dict")
    corpus = [dictionary.doc2bow(text) for text in texts]

    dict_to_txt(dictionary.token2id, u"../data/" + formal + "/" + types + ".tokens", value=False)
    dict_to_txt(dictionary.token2id, u"../data/" + formal + "/" + types + ".tokens2id")
    if formal == "lda":
        corpora.BleiCorpus.serialize(u"../data/lda/" + types + ".lda-c", corpus)
    elif formal == "mm":
        corpora.MmCorpus.serialize(u"../data/mm/" + types + ".mm", corpus)  # store to disk, for later use
    else:
        print "formal no correct"


def operate_corpus():
    corpus = corpora.MmCorpus(u'../data/mm/deerwester.mm')
    corpora.BleiCorpus.serialize(u'../data/lda/corpus.lda-c', corpus)
    # print (list(corpus)[0:10])


if __name__ == '__main__':
    # save_corpora(types="all", formal="lda")
    pass
    # operate_corpus()
