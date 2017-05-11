# coding: UTF-8

import re
import json
step_size = 5000
def extractAllWord(filename):
    # dependency.cabochaから単語の原型を全て抽出し，allWordDict.jsonを作成する．
    allWordDict = {}
    pattern = r'^\*'
    repattern = re.compile(pattern)
    counter = 0
    for index, line in enumerate(open('data/' + filename + '.cabocha', 'r')):
        if repattern.search(line):
            continue
        elif "\t" in line:
            surface, other = line.split("\t")
            elements = other.split(",")
            try:
                stemmed = elements[6]
                if '*' in stemmed:
                    stemmed = surface
            except:
                continue

            try:
                allWordDict[stemmed] += 1
            except:
                allWordDict[stemmed] = 1

        elif "EOS" in line:
            counter += 1
            if counter%step_size == 0:
                print "extractAllWord:", str(counter)
            continue

    f = open('data/allWordDict_' + filename + '.json', 'w')
    json.dump(allWordDict, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f.close()

def dictToStopwordList(filename, k):
    # allWordDict.jsonから上位k件を集め，stopList.txtを作成する．
    f = open('data/allWordDict_' + filename + '.json', 'r')
    allWordDict = json.load(f)
    f.close()
    stopList = []
    counter = 0
    for key, value in sorted(allWordDict.items(), key=lambda x: x[1], reverse=True):
        print key, value
        a = key.encode('utf-8') + '\n'
        # a = key + '\n'
        stopList.append(a)
        counter += 1
        if counter >= k:
            break
    f = open('data/stopList_' + filename + '.txt', 'w')
    f.writelines(stopList)
    f.close()

def showDict(filename, dictName, k, showAll):
    # vocabDict.jsonかverbDict.jsonを示す．
    f = open('data/' + dictName + '_' + filename + '.json', 'r')
    dict = json.load(f)
    f.close()
    counter = 0
    if dictName == "vocabDict":
        y = 0
        reverse_flag = False
    elif dictName == "verbDict":
        y = 1
        reverse_flag = False
    elif dictName == "allVerbDict":
        y = 1
        reverse_flag = True
    elif dictName == "allWordDict":
        y = 1
        reverse_flag = True

    for key, value in sorted(dict.items(), key=lambda x: int(x[y]), reverse=reverse_flag):
        print key.encode('utf-8'), value
        counter += 1
        if showAll is False and counter >= k:
            break

def createVocabDict(filename, k, vocabSize):
    # allWordDict.jsonから上位k件を除いて，vocabDict.jsonを作成する．
    vocabDict = {}
    f = open('data/allWordDict_' + filename + '.json', 'r')
    allWordDict = json.load(f)
    f.close()
    counter = 0
    for key, value in sorted(allWordDict.items(), key=lambda x: int(x[1]), reverse=True):
        if counter >= k:
            vocabDict[counter - k] = key.encode('utf-8')
        counter += 1
        if counter >= vocabSize + k:
            break

    f = open('data/vocabDict_' + filename + '.json', 'w')
    json.dump(vocabDict, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f.close()


if __name__ == '__main__':
    filename = "ans_1"
    k = 100
    # extractAllWord(filename)
    # dictToStopwordList(filename, k)
    showDict(filename, dictName="verbDict", k=120, showAll=False)
    # createVocabDict(filename, k, vocabSize=20000)