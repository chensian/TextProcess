#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/16 0:27
# @Author  : chen
# @Site    : 
# @File    : test.py
# @Software: PyCharm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

# documents = ["Human machine interface for lab abc computer applications",
#              "A survey of user opinion of computer system response time",
#              "The EPS user interface management system",
#              "System and human system engineering testing of EPS",
#              "Relation of user perceived response time to error measurement",
#              "The generation of random binary unordered trees",
#              "The intersection graph of paths in trees",
#              "Graph minors IV Widths of trees and well quasi ordering",
#              "Graph minors A survey"]

documents = file("D:/python/workspace/TextProcess/output/seg/seg_result.txt").readlines()

# vectorize the text i.e. convert the strings to numeric features

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)

# cluster documents
# print documents
true_k = 6
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)
# print top terms per cluster clusters

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print "Cluster %d:" % i,
    for ind in order_centroids[i, :10]:
        print ' %s' % terms[ind],
    print

# a = [1,3,4,5,60]
# print a[:]
# print a[ ::-1]