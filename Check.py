#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import SVM
import numpy as np
import matplotlib.pyplot as plt

def showVerbDistribution(filename, dictname='verbDict', show=1000):

    f = open("data/" + dictname + "_" + filename + ".json", 'r')
    verbDict = json.load(f)
    f.close()
    result = {}
    n2w = {}
    if dictname == "verbDict":
        for key, value in sorted(verbDict.items(), key=lambda x: int(x[1]), reverse=False):
            print key, value
            result[int(value)] = 0
            n2w[int(value)] = key.encode('utf-8')

        counter = 0
        for line in open('data/vectorData_' + filename + '.csv', 'r'):
            # print line,
            label, facts = line.split('\t')
            result[int(label)] += 1

            counter += 1
            if counter >= show:
                break

        for key, value in sorted(result.items(), key=lambda x: int(x[0]), reverse=False):
            print key, n2w[key], '          \t', float(value*100)/float(show), '%', '\t', "(=", value,")"

    else:
        data = list()
        # for key, value in sorted(verbDict.items(), key=lambda x:int(x[1]), reverse=True):
        #     data.append(value)
        #     print value
        data = sorted(verbDict.values(), reverse=True)
        for i, item in enumerate(sorted(verbDict.items(), key=lambda x:int(x[1]), reverse=True)[:show]):
            print i, item[0], item[1]

        return data


def showVocabDistribution(filename, n_stopword):
    counter = 0
    f = open('data/stopDict_' + filename + '.json', 'r')
    stopDict = json.load(f)
    f.close()

    n_vocab = SVM.getDictSize("VocabDict", filename)

    sum_stopword = 0
    sum_vocab = 0
    sum_other = 0
    for key, value in sorted(stopDict.items(), key=lambda x: int(x[1]), reverse=True):
        if counter < n_stopword:
            sum_stopword += int(value)
        elif counter < n_vocab + n_stopword:
            sum_vocab += int(value)
        else:
            sum_other += int(value)
        counter += 1
    print sum_stopword
    print sum_vocab
    print sum_other
    total = float(sum_stopword + sum_vocab + sum_other)
    print "stopword :", float(sum_stopword)/total*100, "%"
    print "vocab :", float(sum_vocab) / total*100, "%"
    print "other :", float(sum_other) / total*100, "%"


def showallVerbDictDistribution(filename, min=0, max=10):
    counter = 0
    f = open('data/allWordDict_' + filename + '.json', 'r')
    stopDict = json.load(f)
    f.close()

    sum = 0
    for key, value in sorted(stopDict.items(), key=lambda x: int(x[1]), reverse=True):

        if counter >= max:
            break
        sum += int(value)
        if counter >= min:
            print key, value
        counter += 1
    print "sum:", sum


def fullword_avarage():

    avg = []
    for line in open('data/vectorData_fullword_ans_1.csv', 'r'):
        _, words = line.split('\t')
        elems = words.split(',')
        # print elems
        avg.append(len(elems))
    average = float(sum(avg)) / float(len(avg))
    avg.sort(reverse=True)
    print avg[:100]
    # print average, "=", (avg), "/", len(avg)
    print "average :", average
    print "max", max(avg), " min",min(avg)
    # print avg


def coverage_graph(filename, inputdata):

    rawdata = np.array(inputdata)
    deletedNum = 0  # 20000個以上の動詞の数
    height = list()
    sum = 0.0
    print "a"
    pruningNum = 500
    for i, data in enumerate(rawdata[:pruningNum]):
        sum += data
        height.append(sum)
        if data > 20000:
            deletedNum = i
            print data
    for data in rawdata[pruningNum:]:
        sum += data
    height.append(sum)

    print "b"
    for i in xrange(len(height)):
        height[i] = height[i]/sum
    print deletedNum, ":", height[deletedNum]
    print "99 :", height[99]
    print "129:", height[129]
    print "c"
    label = [i for i in xrange(len(height))]
    plt.bar(label, height)
    plt.bar(label, height, width=1.0)
    print "d"


    # n_x, bins_x, pathces_x = plt.hist(data, label=u"文の総数", bins=len(data), color="red")
    # plt.title(u"ヒストグラム")
    # plt.xlabel(u"15単語が占める割合[%]")
    # plt.ylabel(u"文章の数")
    # plt.legend()

    # for i in range(len(data_list)):
    #     print "n", i
    #     for j in range(len(n[i])):
    #         print n[i][j],
    #     print ""

    # plt.savefig('data/output/coverage_' + filename + '.png')
    plt.show()
    print "e"


if __name__ == '__main__':
    data = showVerbDistribution(filename="ans_1", dictname="allVerbDict", show=200)
    # showVocabDistribution(filename="ans_1", n_stopword=10)
    # fullword_avarage()
    # showallVerbDictDistribution('ans_1', min=0, max=10)
    coverage_graph("ans_1", data)