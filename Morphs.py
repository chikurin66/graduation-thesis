# coding: UTF-8

import CaboCha
import re
import time
import MeCab
import sys
import json

step_size = 5000

def PlainText(data_name):
    pattern = r'(.*?)(。|[d^]\D\.|か？|か\?|ね？|ね\?|う？|う\?|！|\!)(.*)'
    sentences = []
    count = 0
    f = open('data/plainText_' + data_name + '.txt', 'w')
    for line in open('data/' + data_name + '.tsv', 'r'):
        try:
            a = line.split('\t')[4]
            if a != '':
                match = re.search(pattern, a)
                while match:
                    if len(match.group(1)) > 20 and 'http' not in match.group(1) and "*" not in match.group(1):
                        sentences.append(match.group(1) + match.group(2) + '\n')
                    match = re.search(pattern, match.group(3))
        except:
            print "something wrong"
            print line
        count += 1
        if count%step_size == 0:
            print "PlainText:" + str(count)
            f.writelines(sentences)
            sentences = list()
    print "PlainText:" + str(count)
    f.writelines(sentences)
    f.close()

def Dependency(data_name):
    count = 0
    c = CaboCha.Parser()
    result = []
    w = open('data/' + data_name + '.cabocha', 'w')
    for sentence in open('data/plainText_' + data_name + '.txt', 'r'):
        tree = c.parse(sentence)
        result += tree.toString(CaboCha.FORMAT_LATTICE)
        count += 1
        if count%step_size == 0:
            print "Dependency:" + str(count)
            w.write(''.join(result))
            result = list()
    print "Dependency:" + str(count)
    w.write(''.join(result))
    w.close()

def wakachi(filename):

    tagger = MeCab.Tagger('-F\s%f[6] -U\s%m -E\\n')

    fi = open("data/" + filename + ".txt", 'r')
    fo = open("data/wakachi_" + filename + ".txt", 'w')

    line = fi.readline()
    while line:
        result = tagger.parse(line)
        fo.write(result[1:])  # skip first \s
        line = fi.readline()

    fi.close()
    fo.close()

def wakati_w2v(filename):
    tagger = MeCab.Tagger('-Ochasen')
    # f = open('data/verbDict_w2v_' + filename + '.json', 'r')
    f = open('data/verbDict_w2v_' + filename + '.json', 'r')
    verbDict = json.load(f)
    f.close()

    fo1 = open("data/trainingData_w2v_" + filename + ".tsv", 'w')
    fo2 = open("data/resource_w2v_" + filename + ".txt", 'w')

    for line in open("data/plainText_" + filename + ".txt", 'r'):
        result = tagger.parse(line)
        fo.write(result[1:])  # skip first \s
        line = fi.readline()

    fi.close()
    fo.close()


def main(filename):
    start = time.time()
    data_name = filename
    PlainText(data_name)
    print data_name + " : PlaneText has dane"
    Dependency(data_name)
    print data_name + " : Dependency has dane"
    elapsed_time = time.time() - start
    print "elapsed_time : %s [sec]" % elapsed_time
    print "elapsed_time : %s [min]" % (elapsed_time / 60)
    print "elapsed_time : %s [h]" % (elapsed_time / 3600)


if __name__ == '__main__':
    # main('')
    # wakachi(filename="neko")
    # PlainText("ans_1")
    wakati_w2v("ans_1")