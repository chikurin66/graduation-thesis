# coding: UTF-8

import json

step_size = 10000

def CreateVector(filename, useWord, verbDictSize, removeVerb):
    verbDictName = filename
    vocabDictName = filename
    stopListName = filename

    f = open('data/allVerbDict_' + verbDictName + '.json', 'r')
    allVerbDict = json.load(f)
    f.close()
    g = open('data/vocabDict_' + vocabDictName + '.json', 'r')
    vocabDict = json.load(g)
    g.close()

    counter = 0
    verbDict = {}
    print "allVerbDict Size :", len(allVerbDict)
    print "verbDict"
    for key, value in sorted(allVerbDict.items(), key=lambda x: int(x[1]), reverse=True):
        if counter < removeVerb:
            counter += 1
            continue
        elif counter < verbDictSize + removeVerb:
            verbDict[key.encode('utf-8')] = str(counter-removeVerb)
            print key, counter
            counter += 1
        else:
            break

    vocabDict1 = {}
    print "vocabDict"
    for key, value in sorted(vocabDict.items()):
        print key, value
        vocabDict1[value.encode('utf-8')] = key.encode('utf-8')

    h = open('data/vectorData_uw' + str(useWord) + '_' + filename + '.csv', 'w')

    trainingVec = []
    sampleList = []
    wordCounter = 0
    counter = 0

    for line in open('data/trainingData_' + filename + '.csv', 'r'):

        _, vplace, verb, sentence = line.split('\t')

        if useWord < int(vplace) and verb in verbDict:
            for word in sentence.split(' '):
                wordCounter += 1
                try:
                    trainingVec.append(vocabDict1[word].encode('utf-8'))
                except:
                    trainingVec.append("<unk>")

                if wordCounter >= useWord:
                    break

            # sampleList : 23   290,300,12,5,105
            sampleList.append(verbDict[verb] + '\t' + ','.join(trainingVec) + '\n')
            trainingVec = []
            wordCounter = 0

        counter += 1
        if counter%step_size == 0:
            print "CreateVector:", counter
            h.writelines(sampleList)
            sampleList = []

    print "CreateVector:", counter
    h.writelines(sampleList)
    h.close()

    f = open('data/verbDict_' + filename + '.json', 'w')
    json.dump(verbDict, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f.close()

def CreateVector_fullword(filename, minWord, verbDictSize, removeVerb):
    verbDictName = filename
    vocabDictName = filename
    stopListName = filename

    f = open('data/allVerbDict_' + verbDictName + '.json', 'r')
    allVerbDict = json.load(f)
    f.close()
    g = open('data/vocabDict_' + vocabDictName + '.json', 'r')
    vocabDict = json.load(g)
    g.close()

    counter = 0
    verbDict = {}
    print "allVerbDict Size :", len(allVerbDict)
    print "verbDict"
    for key, value in sorted(allVerbDict.items(), key=lambda x: int(x[1]), reverse=True):
        if counter < removeVerb:
            counter += 1
            continue
        elif counter < verbDictSize + removeVerb:
            verbDict[key.encode('utf-8')] = str(counter-removeVerb)
            print key, counter
            counter += 1
        else:
            break

    vocabDict1 = {}
    print "vocabDict"
    for key, value in sorted(vocabDict.items()):
        print key, value
        vocabDict1[value.encode('utf-8')] = key.encode('utf-8')

    h = open('data/vectorData_fullword_' + filename + '.csv', 'w')

    trainingVec = []
    sampleList = []
    wordCounter = 0
    counter = 0

    for line in open('data/trainingData_' + filename + '.csv', 'r'):

        _, vplace, verb, sentence = line.split('\t')

        if minWord < int(vplace) and verb in verbDict:
            for word in sentence.split(' '):
                wordCounter += 1
                try:
                    trainingVec.append(vocabDict1[word].encode('utf-8'))
                except:
                    trainingVec.append("<unk>")

                if wordCounter >= int(vplace)-1:
                    break

            # sampleList : 23   290,300,12,5,105
            sampleList.append(verbDict[verb] + '\t' + ','.join(trainingVec) + '\n')
            trainingVec = []
            wordCounter = 0

        counter += 1
        if counter%step_size == 0:
            print "CreateVector:", counter
            h.writelines(sampleList)
            sampleList = []

    print "CreateVector:", counter
    h.writelines(sampleList)
    h.close()

    f = open('data/verbDict_' + filename + '.json', 'w')
    json.dump(verbDict, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f.close()


def CreateVector_Hist(filename, useWord, verbDictSize, removeVerb):
    verbDictName = filename
    vocabDictName = filename
    stopListName = filename

    f = open('data/allVerbDict_' + verbDictName + '.json', 'r')
    allVerbDict = json.load(f)
    f.close()
    g = open('data/vocabDict_' + vocabDictName + '.json', 'r')
    vocabDict = json.load(g)
    g.close()

    counter = 0
    verbDict = {}
    print "allVerbDict Size :", len(allVerbDict)
    print "verbDict"
    for key, value in sorted(allVerbDict.items(), key=lambda x: int(x[1]), reverse=True):
        if counter < removeVerb:
            counter += 1
            continue
        elif counter < verbDictSize + removeVerb:
            verbDict[key.encode('utf-8')] = str(counter-removeVerb)
            print key, counter
            counter += 1
        else:
            break

    vocabDict1 = {}
    print "vocabDict"
    for key, value in sorted(vocabDict.items()):
        print key, value
        vocabDict1[value.encode('utf-8')] = key.encode('utf-8')

    h = open('data/vectorData_hist_uw' + str(useWord) + '_' + filename + '.csv', 'w')

    trainingVec = []
    sampleList = []
    wordCounter = 0
    counter = 0

    for line in open('data/trainingData_' + filename + '.csv', 'r'):

        _, vplace, verb, sentence = line.split('\t')

        if useWord < int(vplace) and verb in verbDict:
            for word in sentence.split(' '):
                wordCounter += 1
                try:
                    trainingVec.append(vocabDict1[word].encode('utf-8'))
                except:
                    trainingVec.append("<unk>")

                if wordCounter >= useWord:
                    break

            # sampleList : 10    23    290,300,12,5,105
            sampleList.append(vplace + '\t' + verbDict[verb] + '\t' + ','.join(trainingVec) + '\n')
            trainingVec = []
            wordCounter = 0

        counter += 1
        if counter%step_size == 0:
            print "CreateVector:", counter
            h.writelines(sampleList)
            sampleList = []

    print "CreateVector:", counter
    h.writelines(sampleList)
    h.close()

    f = open('data/verbDict_' + filename + '.json', 'w')
    json.dump(verbDict, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f.close()


def CreateVector_Hist_fullword(filename, minWord, verbDictSize, removeVerb):
    verbDictName = filename
    vocabDictName = filename
    stopListName = filename

    f = open('data/allVerbDict_' + verbDictName + '.json', 'r')
    allVerbDict = json.load(f)
    f.close()
    g = open('data/vocabDict_' + vocabDictName + '.json', 'r')
    vocabDict = json.load(g)
    g.close()

    counter = 0
    verbDict = {}
    print "allVerbDict Size :", len(allVerbDict)
    print "verbDict"
    for key, value in sorted(allVerbDict.items(), key=lambda x: int(x[1]), reverse=True):
        if counter < removeVerb:
            counter += 1
            continue
        elif counter < verbDictSize + removeVerb:
            verbDict[key.encode('utf-8')] = str(counter-removeVerb)
            print key, counter
            counter += 1
        else:
            break

    vocabDict1 = {}
    print "vocabDict"
    for key, value in sorted(vocabDict.items()):
        print key, value
        vocabDict1[value.encode('utf-8')] = key.encode('utf-8')

    h = open('data/vectorData_hist_fullword_' + filename + '.csv', 'w')

    trainingVec = []
    sampleList = []
    wordCounter = 0
    counter = 0

    counter += 1
    if counter % step_size == 0:
        print "CreateVector:", counter
        h.writelines(sampleList)
        sampleList = []

    for line in open('data/trainingData_' + filename + '.csv', 'r'):

        _, vplace, verb, sentence = line.split('\t')

        if minWord < int(vplace) and verb in verbDict:
            for word in sentence.split(' '):
                wordCounter += 1
                try:
                    trainingVec.append(vocabDict1[word].encode('utf-8'))
                except:
                    trainingVec.append("<unk>")

                if wordCounter >= int(vplace) - 1:
                    break

            # sampleList : 10    23    290,300,12,5,105
            sampleList.append(vplace + '\t' + verbDict[verb] + '\t' + ','.join(trainingVec) + '\n')
            trainingVec = []
            wordCounter = 0

        counter += 1
        if counter%step_size == 0:
            print "CreateVector:", counter
            h.writelines(sampleList)
            sampleList = []


    print "CreateVector:", counter
    h.writelines(sampleList)
    h.close()

    f = open('data/verbDict_' + filename + '.json', 'w')
    json.dump(verbDict, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f.close()


def main(filename, useWord):
    CreateVector(filename, useWord)


if __name__ == '__main__':
    filename = "ans_1"
    useWord = 10
    main(filename, useWord)