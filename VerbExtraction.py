# coding: UTF-8
import re
import json
import time
import codecs

step_size = 5000

class Morph:
    def __init__(self, surface, base, pos, pos1, mainVerb):
        self.surface = surface
        self.base = base
        self.pos = pos
        self.pos1 = pos1
        self.mainVerb = mainVerb


def convertToTrainingData(morphs_list, useBase):
    # morphクラスのリストのリストをtrainigDataに変換する．
    # useBase(flag)で基本形を使うかどうかを選択
    # Falseなら基本形は使わない

    counter = 0
    trainingData = []
    sentence = []
    mainVerb = ''
    placeOfMainVerb = 0
    for morphs in morphs_list:
        for morph in morphs:
            counter += 1
            if morph.mainVerb:
                mainVerb = morph.base
                placeOfMainVerb = counter
            if not useBase or '*' in morph.base:
                sentence.append(morph.surface)
            else:
                sentence.append(morph.base)
        if mainVerb and '*' not in mainVerb:
            trainingData.append(str(len(morphs)) + '\t' + str(placeOfMainVerb) + '\t' + mainVerb + '\t' + ' '.join(sentence) + '\n')
        counter = 0
        sentence = []
        mainVerb = ''
        placeOfMainVerb = 0

    return trainingData


def convertToTrainingData_w2v(morphs_list, verbDict, useBase):
    # morphクラスのリストのリストをtrainigDataに変換する．
    # useBase(flag)で基本形を使うかどうかを選択
    # Falseなら基本形は使わない

    counter = 0
    temp_resource = []
    trainingData = []
    resource_list = []
    sentence = []
    mainVerb = ''
    placeOfMainVerb = 0
    for morphs in morphs_list:
        for morph in morphs:
            counter += 1
            if morph.mainVerb:
                mainVerb = morph.base
                placeOfMainVerb = counter
            if not useBase or '*' in morph.base:
                sentence.append(morph.surface)
            else:
                sentence.append(morph.base)

        if mainVerb and '*' not in mainVerb:
            if mainVerb.decode('utf-8') in verbDict:
                trainingData.append(str(len(morphs)) + '\t' + str(placeOfMainVerb) + '\t' + mainVerb + '\t' + ' '.join(sentence) + '\n')
            else:

                for morph in morphs:
                    if not (morph.pos == "助詞" or morph.pos == "助動詞" or morph.pos == "記号" or morph.pos == "感動詞"):
                        if not useBase or '*' in morph.base:
                            temp_resource.append(morph.surface)
                        else:
                            temp_resource.append(morph.base)

                resource_list.append(' '.join(temp_resource) + '\n')
                temp_resource = []

        counter = 0
        sentence = []
        mainVerb = ''
        placeOfMainVerb = 0

    return (trainingData, resource_list)


def extractVerb(filename):
    # 係り受け解析結果.cabochaからメインの動詞を抽出し，trainingData.csvを作成する．

    fi = open('data/verbDict_w2v_' + filename + '.json', 'r')
    verbDict = json.load(fi)
    fi.close()

    morphs_list = []
    morphs = []
    pattern = r'^\*'
    repattern = re.compile(pattern)
    mainVerb_flag = False
    counter = 0
    f = open('data/trainingData_' + filename + '.csv', 'w')
    for index, line in enumerate(open('data/' + filename + '.cabocha','r')):
        if repattern.search(line):
            elements = line.split(" ")
            try:
                dst = elements[2][:-1]
            except:
                continue
        elif "\t" in line:
            surface, other = line.split("\t")
            elements = other.split(",")
            if dst == '-1' and elements[0] == '動詞' and mainVerb_flag == False:
                if len(morphs) > 0:
                    if morphs[-1].pos1 == 'サ変接続':
                        morphs[-1].mainVerb = True
                        morph = Morph(surface, elements[6], elements[0], elements[1], False)
                    else:
                        morph = Morph(surface, elements[6], elements[0], elements[1], True)
                else:
                    # print "length is not enough"
                    continue
                mainVerb_flag = True

            else:
                morph = Morph(surface, elements[6], elements[0], elements[1], False)
            morphs.append(morph)


        elif "EOS" in line:
            if len(morphs) > 1:
                morphs_list.append(morphs)
                counter += 1
            morphs = []
            mainVerb_flag = False

            if counter%step_size == 0:
                print "extractVerb:" + str(counter)
                # morphクラスのリストのリストをtrainigDataに変換する．
                trainingData = convertToTrainingData(morphs_list, verbDict, useBase=True, deleteFunctionword=False)
                f.writelines(trainingData)
                morphs_list = []

    try:
        print "extractVerb:" + str(counter)
        # morphクラスのリストのリストをtrainigDataに変換する．
        trainingData = convertToTrainingData(morphs_list, verbDict, useBase=True, deleteFunctionword=False)
        f.writelines(trainingData)
        f.close()
    except:
        f.close()


def extractVerb_w2v(filename):
    # 係り受け解析結果.cabochaからメインの動詞を抽出し，trainingData.csvを作成する．
    fi = open('data/verbDict_w2v_' + filename + '.json', 'r')
    verbDict = json.load(fi)
    fi.close()
    useBase = False
    morphs_list = []
    morphs = []
    pattern = r'^\*'
    repattern = re.compile(pattern)
    mainVerb_flag = False
    counter = 0
    f1 = open('data/trainingData_w2v_' + filename + '.tsv', 'w')
    f2 = open('data/resouce_w2v_' + filename + '.txt', 'w')

    for index, line in enumerate(open('data/' + filename + '.cabocha','r')):
        if repattern.search(line):
            elements = line.split(" ")
            try:
                dst = elements[2][:-1]
            except:
                continue
        elif "\t" in line:
            surface, other = line.split("\t")
            elements = other.split(",")
            if dst == '-1' and elements[0] == '動詞' and mainVerb_flag == False:
                if len(morphs) > 0:
                    if morphs[-1].pos1 == 'サ変接続':
                        morphs[-1].mainVerb = True
                        morph = Morph(surface, elements[6], elements[0], elements[1], False)
                    else:
                        morph = Morph(surface, elements[6], elements[0], elements[1], True)
                else:
                    # print "length is not enough"
                    continue
                mainVerb_flag = True

            else:
                morph = Morph(surface, elements[6], elements[0], elements[1], False)
            morphs.append(morph)


        elif "EOS" in line:
            if len(morphs) > 1:
                morphs_list.append(morphs)
                counter += 1
            morphs = []
            mainVerb_flag = False

            if counter%step_size == 0:
                print "extractVerb:" + str(counter)
                # morphクラスのリストのリストをtrainigDataに変換する．
                trainingData, resource = convertToTrainingData_w2v(morphs_list, verbDict, useBase)
                f1.writelines(trainingData)
                f2.writelines(resource)
                morphs_list = []

    try:
        print "extractVerb:" + str(counter)
        # morphクラスのリストのリストをtrainigDataに変換する．
        trainingData, resource = convertToTrainingData_w2v(morphs_list, verbDict, useBase)
        f1.writelines(trainingData)
        f2.writelines(resource)
        f1.close()
        f2.close()
    except:
        f1.close()
        f2.close()


# def createResource_w2v(filename):
#
#
#     fo1 = open('data/trainingData_w2v_' + filename + '.tsv', 'w')
#     fo2 = open('data/resource_w2v_' + filename + '.txt', 'w')
#     trainingData_list = []
#     resource_list = []
#     for i, line in enumerate(open("data/trainingData_all_w2v_" + filename + ".tsv", "r")):
#         _, vplace, verb, sentence = line.split('\t')
#         if verb.decode('utf-8') in verbDict:
#             trainingData_list.append(line)
#         else:
#             resource_list.append(sentence)
#
#         if (i+1)%step_size == 0:
#             print "createResource:", i+1
#             fo1.writelines(trainingData_list)
#             fo2.writelines(resource_list)
#             trainingData_list = []
#             resource_list = []
#
#     print "createResource:", i + 1
#     fo1.writelines(trainingData_list)
#     fo2.writelines(resource_list)
#     fo1.close()
#     fo2.close()


def createVerbDict(filename, verbDictSize):
    # trainingData.csvから動詞の個数をカウントし，動詞辞書を.json形式で作成する．
    allVerbDict = {}
    counter = 0
    useword = 15
    for line in open('data/trainingData_' + filename + '.csv', 'r'):
        _, vplace, mainVerb, _ = line.split("\t")
        if vplace > useword:
            try:
                allVerbDict[mainVerb] += 1
            except:
                allVerbDict[mainVerb] = 1
        counter += 1
        if counter%step_size == 0:
            print "createVerbDict:" + str(counter)
    print "createVerbDict:" + str(counter)
    counter = 0
    under100 = 0
    over100 = 0
    for key, value in sorted(allVerbDict.items(), key=lambda x:x[1], reverse=True):
        print key, ":", value
        counter += 1
        if counter >= verbDictSize:
            over100 += value
        else:
            under100 += value
    print "under100 = ", under100
    print "over100 = ", over100

    # f = open('data/allVerbDict' + filename + '.json', 'w')
    f = open('data/allVerbDict_w2v_' + filename + '.json', 'w')
    json.dump(allVerbDict, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f.close()


def allVerbDict2VerbDict(filename, dictSize=100):
    fi = codecs.open('data/allVerbDict_w2v_' + filename + '.json', 'r', 'utf-8')
    allVerbDict = json.load(fi)
    fi.close()
    verbDict = {}
    counter = 0
    for key, value in sorted(allVerbDict.items(), key=lambda x:x[1], reverse=True)[7:]:
        print type(key.encode('utf-8')), ":", value

        verbDict[key.encode("utf-8")] = str(counter)
        counter += 1
        if counter >= dictSize:
            break

    print verbDict
    fo = open('data/verbDict_w2v_' + filename + '.json', 'w')
    json.dump(verbDict, fo, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    fo.close()


def removeNoise(filename):
    f = open('data/trainingData_' + filename + '.csv', 'w')
    counter = 0
    trainingData = []
    delete_flag = False
    for line in open('data/trainingData_noise_' + filename + '.csv', 'r'):
        if '*' in line:
            delete_flag = True
            continue
        if delete_flag:
            delete_flag = False
            continue
        counter += 1
        trainingData.append(line)
        if counter % step_size == 0:
            print "removeNoise:" + str(counter)
            f.writelines(trainingData)
            trainingData = []
    print "removeNoise:" + str(counter)
    f.writelines(trainingData)
    f.close()


def main(filename):
    # filenameで指定された.cabochaのファイルからtrainingData.csvとその動詞辞書verbDict.jsonを作成する．
    # 所要時間を計算する
    start = time.time()
    # 係り受け解析結果.cabochaからメインの動詞を抽出し，trainingData.csvを作成する．
    extractVerb(filename)

    # trainingData.csvから動詞の個数をカウントし，動詞辞書を.json形式で作成する．
    createVerbDict(filename)
    print filename + "has done"
    elapsed_time = time.time() - start
    print "elapsed_time : %s [sec]" % elapsed_time
    print "elapsed_time : %s [min]" % (elapsed_time / 60)
    print "elapsed_time : %s [h]" % (elapsed_time / 3600)

if __name__ == '__main__':
    filename = ""
    #main(filename)
    # createVerbDict("ans_1", 100)
    # allVerbDict2VerbDict(filename)
    # extractVerb_w2v(filename)
    extractVerb_w2v(filename)