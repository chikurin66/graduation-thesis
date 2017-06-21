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


def d2e():
    f = open('data/aggregatedDict.json', 'r')
    agg_e2d = json.loads(f.read(), 'utf-8')
    f.close()

    agg_d2e = {}
    for key, value in agg_e2d.items():
        for v in value:
            if v not in agg_d2e:
                agg_d2e[v] = list()
            agg_d2e[v].append(key)

    text1 = json.dumps(agg_e2d, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    with open('data/aggregatedDict_e2d.json', 'w') as f1:
        f1.write(text1.encode("utf-8"))

    text2 = json.dumps(agg_d2e, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    with open('data/aggregatedDict_d2e.json', 'w') as f2:
        f2.write(text2.encode("utf-8"))


def showDict(opt="e2d", mc=1):
    f = open('data/aggregatedDict_' + opt + '.json', 'r')
    agg_dict = json.load(f)
    f.close()
    counter = 0
    for key, value in agg_dict.items():
        if len(value) >= mc:
            counter += 1
            print key, " : ",
            for v in value:
                print v,
            print ""
    print "# of key is", counter


if __name__ == '__main__':
    # dict = getGoiDict("goi.csv", verbOnly=True, levelOnly=True)
    # showGoiDict(dict)

    # text1 = json.dumps(dict, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    # with open('data/goiLevelDict.json', 'w') as f1:
    #     f1.write(text1)

    # synLevel_dic = getSynLevelDict("カウント")
    # agg_dic = getAggregatedDict(dict)

    # fo = open('data/aggregatedDict' + '.json', 'w')
    # json.dump(agg_dic, fo, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    # fo.close()
    goiDict = getGoiDict()
    showGoiDict(goiDict)

    with open("data/goiDi")
    json.dump()

    showDict(opt="e2d", mc=2)
