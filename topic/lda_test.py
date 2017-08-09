#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/10 19:11
# @Author  : chen
# @Site    : 
# @File    : lda_test.py
# @Software: PyCharm
from __future__ import division, print_function

import numpy as np
import lda
import lda.datasets

# document-term matrix
from topic import data_util


def load_data():
    X = data_util.load_annals()
    print("type(X): {}".format(type(X)))
    print("shape: {}\n".format(X.shape))
    # print(X[:5, :5])
    return X


def load_vocab():
    # the vocab
    vocab = data_util.load_annals_vocab()
    print("type(vocab): {}".format(type(vocab)))
    print("len(vocab): {}\n".format(len(vocab)))
    print(vocab[:6])
    return vocab


def load_titles():
    # titles for each story
    titles = data_util.load_annals_titles()
    print("type(titles): {}".format(type(titles)))
    print("len(titles): {}\n".format(len(titles)))
    print(titles[:2])  # 前两篇文章的标题
    return titles


X = load_data()
vocab = load_vocab()
# titles = load_titles()


# 训练数据，指定20个主题，500次迭代：
model = lda.LDA(n_topics=2, n_iter=500, random_state=1)
model.fit(X)

logfile = open('.../yourfile.txt', 'a')
print >> logfile, lda.show_topics(topics=-1, topn=10)

# 主题-单词（topic-word）分布
topic_word = model.topic_word_
print("type(topic_word): {}".format(type(topic_word)))
print("shape: {}".format(topic_word.shape))

# topic_word中一行对应一个topic，一行之和为1。 看一看'church', 'pope', 'years'这三个单词在各个主题中的比重：
# print(topic_word[:, :3])

# 获取每个topic下权重最高的5个单词：
n = 15
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n + 1):-1]
    print('*Topic {}\n- {}'.format(i, ' '.join(topic_words)))

# 关于数据集替换
#
# 下载包以后,把datasets.py里面的load_annals()里面的
# annals.ldac,load_annals_vocab()里面的annals.tokens,load_annals_titles()里面的annals.titles替换成自己的数据集就行了.数据集格式按照包里的生成就行.

# 文档-主题（Document-Topic）分布：


doc_topic = model.doc_topic_
print("type(doc_topic): {}".format(type(doc_topic)))
print("shape: {}".format(doc_topic.shape))

# 输入前10篇文章最可能的Topic：

for n in range(8):
    topic_most_pr = doc_topic[n].argmax()
    print("doc: {} topic: {}".format(n, topic_most_pr))
