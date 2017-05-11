#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

def Histogram(filename, x, y):
    n_x, bins_x, pathces_x = plt.hist(x, label=u"文の総数", range=(0, 100), bins=10, color="red")
    n_y, bins_y, pathces_y = plt.hist(y, label=u"正答数", range=(0, 100), bins=10, color="blue")
    plt.title(u"ヒストグラム")
    plt.xlabel(u"15単語が占める割合[%]")
    plt.ylabel(u"文章の数")
    plt.legend()

    print "n_y"
    for i in range(len(n_x)):
        print n_y[i],
    print ""
    print "n_x"
    for i in range(len(n_x)):
        print n_x[i],
    print ""
    print "(n_y/n_x)*100"
    for i in range(len(n_x)):
        print n_y[i] / n_x[i] * 100,
    print ""

    plt.savefig('data/output/histogram4_' + filename + '.png')
    # plt.show()

def Histogram_verbFixed(filename, data_list, label_list):

    color_list = ["red", "blue", "green", "yellow", "white", "gray", "black", "pink", "purple", "orange"]
    n = list()
    bins = list()
    pathces = list()
    n_sum = [0,0,0,0,0,0,0,0,0,0]
    for i in range(len(data_list)):
        n_, bins_, pathces_ = plt.hist(data_list[i], stacked=True, label=label_list[i], range=(0, 100), bins=10, color=color_list[i])
        for j in range(len(n_)):
            n_sum[j] += n_[j]
        n.append(n_sum)
        bins.append(bins_)
        pathces.append(pathces_)


    plt.title(u"ヒストグラム")
    plt.xlabel(u"15単語が占める割合[%]")
    plt.ylabel(u"文章の数")
    plt.legend()

    for i in range(len(data_list)):
        print "n", i
        for j in range(len(n[i])):
            print n[i][j],
        print ""

    plt.savefig('data/output/histogram_verbFixed_' + filename + '.png')
    plt.show()

if __name__ == '__main__':
    # x = [1, 10, 40, 45, 35, 10, 87, 79]
    # y = [10, 45, 87, 79]
    # Histogram("aaa", x, y)
    data_list_before = [[1,2,3,4,5],
                        [2,3,4,5,39]]
    label_list = [u"あ", u"い"]

    data_list_after = [0,0,0,0,0,0,0,0,0,0]
    data_temp = list()
    for data in data_list_before:
        for x in data:
            data_temp.append(x)

    Histogram_verbFixed("test", data_list_after, label_list)