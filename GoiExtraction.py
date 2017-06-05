#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Wordnet_jp as wn
import json


def getGoiDict(filename="goi.csv", verbOnly=True, levelOnly=True):
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

    if levelOnly:
        goiLevelDict = {}
        for key, value in goidict.items():
            goiLevelDict[key] = value[0]
        return goiLevelDict

    else:
        return goidict


def showGoiDict(goidict):
    print len(goidict)
    for word, value in goidict.items():
        print word, '\t',
        if isinstance(value, list):
            print value[0], value[1], value[2]
        else:
            print value


def getSynLevelDict(verb):
    synonym_dic = wn.searchSynonym(verb, show=False)
    synonym_set = set()

    for key, value in synonym_dic.items():
        for x in value:
            synonym_set.add(x)

    goidict = getGoiDict("goi.csv", verbOnly=True, levelOnly=True)

    synLevel_dic = {i: list() for i in range(7)[1:]}
    for verb in synonym_set:
        if goidict.has_key(verb):
            synLevel_dic[goidict[verb]].append(verb)

    return synLevel_dic

def getAggregatedDict(goiDict):
    agg_dic = {}
    # 語彙辞書の動詞の類義語をワードネットで探し，
    # その類義語で一番簡単な動詞をkeyとする辞書に追加（list表現で）
    for verb, level in goiDict.items():

        synLevel_dic = getSynLevelDict(verb)
        # 一番簡単な動詞のリストを追加
        for i, value in synLevel_dic.items():
            if len(value) > 0:
                for v in value:
                    if not agg_dic.has_key(v):
                        agg_dic[v] = list()
                    agg_dic[v].append(verb)
                break
    return agg_dic

if __name__ == '__main__':
    dict = getGoiDict("goi.csv", verbOnly=True, levelOnly=True)
    showGoiDict(dict)
    # synLevel_dic = getSynLevelDict("カウント")
    agg_dic = getAggregatedDict(dict)

    for k, v in agg_dic.items():
        print k, " : ",
        for val in v:
            print val,
        print ""

    fo = open('data/aggregatedDict' + '.json', 'w')
    json.dump(agg_dic, fo, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    fo.close()
