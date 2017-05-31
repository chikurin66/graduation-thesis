#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Wordnet_jp as wn


def getGoiDict(filename="goi.csv", verbOnly='True'):
    isVerb = False
    goidict = {}
    f = open("data/" + filename, 'r')
    lines = f.readlines()
    f.close()
    for line in lines[1:]:
        _, word, _, level, pos, pos1, _ = line.split(',')
        # make level statement int (1~6)
        level = int(level.split(".")[0])

        # 感動詞は除いて，動詞を抽出
        if '感' not in pos and '動詞' in pos:
            isVerb = True

        # サ変を取得
        elif 'サ変' in pos1:
            if 'and' in pos1:
                latter = pos1.split('and')[-1]
                if 'サ変' in latter:
                    isVerb = True

        if verbOnly and isVerb:
            goidict[word] = [level, pos, pos1]
            isVerb = False

        elif not verbOnly:
            goidict[word] = [level, pos, pos1]

    return goidict


def showGoiDict(goidict):
    print len(goidict)
    for word, value in goidict.items():
        print word, '\t',
        print value[0], value[1], value[2]


def simplifyVerb(verb):

    synonym_dic = wn.searchSynonym(verb, show=False)
    synonym_set = set()

    for key, value in synonym_dic.items():
        print key, "\t",
        for x in value:
            synonym_set.add(x)
            print x,
        print ""
    print ""

    goidict = getGoiDict("goi.csv")
    simplest_verb = [synonym_set.pop(), goidict[synonym_set[0]][1]]

    return simplest_verb


if __name__ == '__main__':
    dict = getGoiDict("goi.csv")
    showGoiDict(dict)
    simplest_verb = simplifyVerb("カウント")
    print simplest_verb[0], simplest_verb[1]

