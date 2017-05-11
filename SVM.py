#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import json
from sklearn import cross_validation
from sklearn import svm
from sklearn.externals import joblib
from sklearn import decomposition
import random
import time
import Histogram
import GridSearch
from gensim.models import word2vec

def getDictSize(dictName, filename):
    g = open('data/' + dictName + '_' + filename + '.json', 'r')
    Dict = json.load(g)
    g.close()
    print dictName, "Size =", len(Dict)
    return len(Dict)


def createTrainingVec(filename, useWord, sampleSize):
    vocabSize = getDictSize(dictName="VocabDict", filename=filename)
    training_data = np.zeros((sampleSize, vocabSize))
    training_labels = np.zeros(sampleSize)
    counter = 0
    for line in open('data/vectorData_uw' + str(useWord) + '_' + filename + '.csv', 'r'):
        label, facts = line.split('\t')
        training_labels[counter] = label
        fact_list = facts.split(',')
        for x in fact_list:
            try:
                training_data[counter, int(x)] += 1
            except:
                continue
        counter += 1
        if counter >= sampleSize:
            break
    return (training_data, training_labels)


def createTrainingVec_Equal(filename, useWord, sampleSize, n_class):

    vocabSize = getDictSize(dictName="vocabDict", filename=filename)
    training_data = np.zeros((sampleSize, vocabSize))
    training_labels = np.zeros(sampleSize)
    counter = 0
    f = open('data/verbDict_' + filename + '.json', 'r')
    verbDict = json.load(f)
    f.close()
    verbSize = len(verbDict)
    print "n_class :", n_class
    verb_list = random.sample(verbDict, n_class)

    newVerbDict = {}
    for verb in verb_list:
        print verb.encode('utf-8'), verbDict[verb]
        newVerbDict[verb] = verbDict[verb]

    n_each = sampleSize / n_class
    temp_line = []
    if sampleSize%n_class == 0:
        # newVerbDictからn_each個のサンプルをラインごとにとってくる
        for key, value in sorted(newVerbDict.items(), key=lambda x:int(x[1]), reverse=False):
            for line in open('data/vectorData_uw' + str(useWord) + '_' + filename + '.csv', 'r'):
                label, elems = line.split('\t')
                if int(label) == int(value.encode('utf-8')):
                    temp_line.append(line)
                    counter += 1
                    if counter >= n_each:
                        counter = 0
                        noVerb_flag = False
                        break
                noVerb_flag = True
            if noVerb_flag:
                print "There is no enough samples in corpora :", key.encode('utf-8')
                print "counter :", counter
                print "go ot vectorData_ans_0.csv"
                for line in open('data/vectorData_uw' + str(useWord) + '_' + "ans_0" + '.csv', 'r'):
                    label, elems = line.split('\t')
                    if int(label) == int(value.encode('utf-8')):
                        temp_line.append(line)
                        counter += 1
                        if counter >= n_each:
                            counter = 0
                            noVerb_flag = False
                            break
                    noVerb_flag = True
                if noVerb_flag:
                    print "There is no enough samples in second corpora :", key.encode('utf-8')
                    print "counter :", counter
                    return ([None], [None])
                    # コーパスにn_each個の対応する動詞のサンプルがなかった場合の処理をかく必要あり

        random.shuffle(temp_line)
        sen_counter = 0
        for line in temp_line:
            label, elems = line.split('\t')
            training_labels[sen_counter] = label
            elem_list = elems.split(',')
            for x in elem_list:
                try:
                    training_data[sen_counter, int(x)] += 1
                except:
                    continue
            sen_counter += 1

        return (training_data, training_labels)
    else:
        print "error : warikirenai"
        return None


def createTrainingVec_Equal_verbFixed(filename, useWord, sampleSize, n_class, test_size):
    f = open('data/vocabDict_' + filename + '.json', 'r')
    vocab_i2w = json.load(f)
    f.close()

    vocabSize = getDictSize(dictName="vocabDict", filename=filename)
    training_data = np.zeros((sampleSize, vocabSize))
    training_labels = np.zeros(sampleSize)
    verb_size = 10
    test_data = np.zeros((test_size*verb_size, vocabSize))
    test_labels = np.zeros(test_size*verb_size)


    counter = 0
    f = open('data/verbDict_' + filename + '.json', 'r')
    verbDict = json.load(f)
    f.close()
    verb_i2w = dict()
    for key, value in verbDict.items():
        verb_i2w[value] = key

    verbSize = len(verbDict)
    print "n_class :", n_class
    #verb_list = random.sample(verbDict, n_class)
    verb_list = [u"削除",u"言える",u"答える",u"表示",u"待つ",u"消える",u"送る",u"すぎる",u"つける",u"とる"]
    newVerbDict = {}
    for verb in verb_list:
        print verb.encode('utf-8'), verbDict[verb]
        newVerbDict[verb] = verbDict[verb]

    n_each = sampleSize / n_class
    temp_line = []
    test_temp = []
    if sampleSize%n_class == 0:
        # newVerbDictからn_each個のサンプルをラインごとにとってくる
        for key, value in sorted(newVerbDict.items(), key=lambda x:int(x[1]), reverse=False):
            for line in open('data/vectorData_uw' + str(useWord) + '_' + filename + '.csv', 'r'):
                label, elems = line.split('\t')
                if int(label) == int(value.encode('utf-8')):
                    if counter < n_each:
                        temp_line.append(line)
                    elif n_each <= counter and counter < n_each + test_size:
                        test_temp.append(line)
                    counter += 1
                    if counter >= n_each + test_size:
                        counter = 0
                        noVerb_flag = False
                        break
                noVerb_flag = True
            if noVerb_flag:
                print "There is no enough samples in corpora :", key.encode('utf-8')
                print "counter :", counter
                print "go ot vectorData_ans_0.csv"
                for line in open('data/vectorData_uw' + str(useWord) + '_' + "ans_0" + '.csv', 'r'):
                    label, elems = line.split('\t')
                    if int(label) == int(value.encode('utf-8')):
                        temp_line.append(line)
                        counter += 1
                        if counter >= n_each:
                            counter = 0
                            noVerb_flag = False
                            break
                    noVerb_flag = True
                if noVerb_flag:
                    print "There is no enough samples in second corpora :", key.encode('utf-8')
                    print "counter :", counter
                    return ([None], [None])
                    # コーパスにn_each個の対応する動詞のサンプルがなかった場合の処理をかく必要あり

        print "aaa", len(temp_line), len(test_temp)
        random.shuffle(temp_line)
        sen_counter = 0
        for line in temp_line:
            label, elems = line.split('\t')
            training_labels[sen_counter] = label
            elem_list = elems.split(',')
            for x in elem_list:
                try:
                    training_data[sen_counter, int(x)] += 1
                except:
                    continue
            sen_counter += 1

        print "bbb"
        sen_counter = 0
        for line in test_temp:
            label, elems = line.split('\t')
            test_labels[sen_counter] = label
            elem_list = elems.split(',')
            for x in elem_list:
                try:
                    test_data[sen_counter, int(x)] += 1
                except:
                    continue
            sen_counter += 1


        for line in test_temp:
            label, elems = line.split('\t')
            print verb_i2w[label], "|",
            elem_list = elems.split(',')
            for x in elem_list:
                try:
                    print vocab_i2w[str(int(x))],
                except:
                    print x,
            print ""

        return (training_data, training_labels, test_data, test_labels)
    else:
        print "error : warikirenai"
        return None


def createTrainingVec_Equal_Hist_verbFixed(filename, useWord, sampleSize, n_class, test_size):
    loadfilename = 'data/vectorData_hist_uw' + str(useWord) + '_' + filename + '.csv'
    f = open('data/vocabDict_' + filename + '.json', 'r')
    vocab_i2w = json.load(f)
    f.close()

    vocabSize = getDictSize(dictName="vocabDict", filename=filename)
    training_data = np.zeros((sampleSize, vocabSize))
    training_labels = np.zeros(sampleSize)
    verb_size = 10
    test_data = np.zeros((test_size*verb_size, vocabSize))
    test_labels = np.zeros(test_size*verb_size)
    test_vplace = np.zeros(test_size*verb_size)

    counter = 0
    f = open('data/verbDict_' + filename + '.json', 'r')
    verbDict = json.load(f)
    f.close()
    verb_i2w = dict()
    for key, value in verbDict.items():
        verb_i2w[value] = key

    verbSize = len(verbDict)
    print "n_class :", n_class
    #verb_list = random.sample(verbDict, n_class)
    verb_list = [u"削除",u"言える",u"答える",u"表示",u"待つ",u"消える",u"送る",u"すぎる",u"つける",u"とる"]
    newVerbDict = {}
    for verb in verb_list:
        print verb.encode('utf-8'), verbDict[verb]
        newVerbDict[verb] = verbDict[verb]

    n_each = sampleSize / n_class
    temp_line = []
    test_temp = []
    aligned_verb_list = []
    if sampleSize%n_class == 0:
        # newVerbDictからn_each個のサンプルをラインごとにとってくる
        for key, value in sorted(newVerbDict.items(), key=lambda x:int(x[1]), reverse=False):
            aligned_verb_list.append(key.encode('utf-8'))
            for line in open(loadfilename, 'r'):
                vplace, label, elems = line.split('\t')
                if int(label) == int(value.encode('utf-8')):
                    if counter < n_each:
                        temp_line.append(line)
                    elif n_each <= counter and counter < n_each + test_size:
                        test_temp.append(line)
                    counter += 1
                    if counter >= n_each + test_size:
                        counter = 0
                        noVerb_flag = False
                        break
                noVerb_flag = True
            if noVerb_flag:
                print "There is no enough samples in corpora :", key.encode('utf-8')
                print "counter :", counter
                print "go ot vectorData_ans_0.csv"
                for line in open('data/vectorData_uw' + str(useWord) + '_' + "ans_0" + '.csv', 'r'):
                    label, elems = line.split('\t')
                    if int(label) == int(value.encode('utf-8')):
                        temp_line.append(line)
                        counter += 1
                        if counter >= n_each:
                            counter = 0
                            noVerb_flag = False
                            break
                    noVerb_flag = True
                if noVerb_flag:
                    print "There is no enough samples in second corpora :", key.encode('utf-8')
                    print "counter :", counter
                    return ([None], [None])
                    # コーパスにn_each個の対応する動詞のサンプルがなかった場合の処理をかく必要あり

        print "aaaa", len(temp_line), len(test_temp)
        random.shuffle(temp_line)
        sen_counter = 0
        for line in temp_line:
            vplace, label, elems = line.split('\t')
            training_labels[sen_counter] = label
            elem_list = elems.split(',')
            for x in elem_list:
                try:
                    training_data[sen_counter, int(x)] += 1
                except:
                    continue
            sen_counter += 1

        print "bbbb"
        sen_counter = 0
        for line in test_temp:
            vplace, label, elems = line.split('\t')
            test_vplace[sen_counter] = vplace
            test_labels[sen_counter] = label
            elem_list = elems.split(',')
            for x in elem_list:
                try:
                    test_data[sen_counter, int(x)] += 1
                except:
                    continue
            sen_counter += 1

        print "cccc"
        print len(test_temp), len(test_vplace)
        for line, vplace in zip(test_temp, list(test_vplace)):
            vplace, label, elems = line.split('\t')
            print verb_i2w[label], "|", vplace, "|",
            elem_list = elems.split(',')
            for x in elem_list:
                try:
                    print vocab_i2w[str(int(x))],
                except:
                    print x,
            print ""

        print "dddd"
        return (training_data, training_labels, test_data, test_labels, test_vplace, aligned_verb_list)
    else:
        print "error : warikirenai"
        return None


def createTrainingVec_Equal_Hist(filename, useWord, sampleSize, n_class, opt):

    if opt == "hist":
        loadfilename = 'data/vectorData_hist_uw' + str(useWord) + '_' + filename + '.csv'
    elif opt == "hist_all":
        loadfilename = 'data/vectorData_hist_fullword_' + filename + '.csv'
    else:
        print "what is opt?"
        print opt

    vocabSize = getDictSize(dictName="vocabDict", filename=filename)
    training_data = np.zeros((sampleSize, vocabSize))
    training_labels = np.zeros(sampleSize)
    vplace_lists = np.zeros(sampleSize)
    counter = 0
    f = open('data/verbDict_' + filename + '.json', 'r')
    verbDict = json.load(f)
    f.close()

    if sampleSize >= 250000:
        out_list_5000 = [u'くださる', u'迷う', u'質問', u'悩む', u'おねがい', u'助かる',
                         u'おしえる', u'貸す', u'お待ち', u'頂ける', u'アドバイス', u'住む']  # コーパスに5,000文無い動詞のリスト
        for outverb in out_list_5000:
            del verbDict[outverb]  # これらの動詞を辞書から削除

    print "n_class :", n_class
    verb_list = random.sample(verbDict, n_class)

    newVerbDict = {}
    for verb in verb_list:
        print verb.encode('utf-8'), verbDict[verb]
        newVerbDict[verb] = verbDict[verb]

    n_each = sampleSize / n_class
    temp_line = []
    if sampleSize%n_class == 0:
        # newVerbDictからn_each個のサンプルをラインごとにとってくる
        for key, value in sorted(newVerbDict.items(), key=lambda x:int(x[1]), reverse=False):
            for line in open(loadfilename, 'r'):
                vplace, label, elems = line.split('\t')
                if int(label) == int(value.encode('utf-8')):
                    temp_line.append(line)
                    counter += 1
                    if counter >= n_each:
                        counter = 0
                        noVerb_flag = False
                        break
                noVerb_flag = True
            if noVerb_flag:
                print "There is no enough samples in corpora :", key.encode('utf-8')
                print "counter :", counter
                return ([None], [None])
                # コーパスにn_each個の対応する動詞のサンプルがなかった場合の処理をかく必要あり
        random.shuffle(temp_line)
        sen_counter = 0
        for line in temp_line:
            vplace, label, elems = line.split('\t')
            vplace_lists[sen_counter] = vplace
            training_labels[sen_counter] = label
            elem_list = elems.split(',')
            for x in elem_list:
                try:
                    training_data[sen_counter, int(x)] += 1
                except:
                    continue
            sen_counter += 1

        return (training_data, training_labels, vplace_lists)
    else:
        print "error : warikirenai"
        return None


def DimensionReduction(filename, vector_list, reducedDim):
    print "PCA starts"
    print "reduced dimension :", reducedDim
    start = time.time()
    pca = decomposition.PCA(reducedDim)
    result = pca.fit_transform(vector_list)
    np.savetxt("data/reducedVec_" + filename + "_dim" + str(reducedDim) + ".csv", result, delimiter=",")
    elapsed_time = time.time() - start
    print "PCA finish : %s [min]" % (elapsed_time / 60)
    return result


def main(filename, n_folds, useWord, sampleSize, reducedDim, opt, n_class, kernel, vecName, gridsearch):
    if vecName == "new":
        iter_flag = True
        # trainingData & trainingLabels 作成
        print "opt :", opt
        if opt == "equal":
            while iter_flag:
                training_data, training_labels = createTrainingVec_Equal(filename, useWord, sampleSize, n_class)
                if len(training_labels) > 1:
                    iter_flag = False
        elif opt == "hist":
            while iter_flag:
                try:
                    training_data, training_labels, vplace_lists = createTrainingVec_Equal_Hist(filename, useWord, sampleSize, n_class, opt)
                except:
                    continue
                if len(training_labels) > 1:
                    iter_flag = False
        elif opt == "hist_all":
            while iter_flag:
                try:
                    training_data, training_labels, vplace_lists = createTrainingVec_Equal_Hist(filename, useWord, sampleSize, n_class, opt)
                except:
                    continue
                if len(training_labels) > 1:
                    iter_flag = False
        else:
            training_data, training_labels = createTrainingVec(filename, useWord, sampleSize)
        print "sample size :", len(training_labels)

        # for x in training_labels:
        #     print x
        # return True

        # PCAを用いた次元削減
        training_data = DimensionReduction(filename, training_data, reducedDim)

        np.savetxt("data/v20000rd100nc100_data.csv", training_data, delimiter=",")
        np.savetxt("data/v20000rd100nc100_labels.csv", training_labels, delimiter=",")

    elif vecName == "v20000rd100nc100":
        training_data = np.loadtxt("data/v20000rd100nc100_data.csv", delimiter=",")
        training_labels = np.loadtxt("data/v20000rd100nc100_labels.csv", delimiter=",")


    if gridsearch:
        print "GridSearch starts"
        GridSearch.Gridsearch(training_data, training_labels)

    else:
        # K-分割交差検証
        kfold = cross_validation.KFold(len(training_data), n_folds=n_folds)
        results = np.array([])
        confirmation = []
        counter = 0
        for training, test in kfold:
            counter += 1
            print counter, "folds    ",
            # 教師データで　SVM を学習する
            clf = svm.SVC(kernel=kernel)
            clf.fit(training_data[training], training_labels[training])

            # テストデータを使った検証
            answers = clf.predict(training_data[test])
            # ラベルデータと一致しているか調べる
            are_correct = answers == training_labels[test]
            results = np.r_[results, are_correct]

            pre = np.c_[answers, training_labels[test]]
            confirmation.append(pre)

        print ""
        print('カーネル: {kernel}'.format(kernel=kernel))
        correct = np.sum(results)
        N = len(training_data)
        percent = (float(correct) / N) * 100
        print('正答率: {percent:.2f}% ({correct}/{all})'.format(
            correct=correct,
            all=len(training_data),
            percent=percent,
        ))

    if "hist" in opt:

        for i, x in enumerate(vplace_lists):
            vplace_lists[i] = int(float(useWord)*100/float(vplace_lists[i]))
        vplace_lists_corr = np.zeros(len(vplace_lists))
        for i, x in enumerate(results):
            if x == 1:
                vplace_lists_corr[i] = vplace_lists[i]
        vplace_lists_corr.sort()
        while True:
            vplace_lists_corr = np.delete(vplace_lists_corr, 0)
            if vplace_lists_corr[0] > 0:
                break
        Histogram.Histogram(filename, vplace_lists, vplace_lists_corr)

    # print results
    # print "prediction, correct"
    # for x in confirmation:
    #      for y in x:
    #          print y[0], "\t", y[1]

    joblib.dump(clf, 'data/SVM/SVM_' + filename + '_' + str(n_folds) + 'folds' + '_clf_' + kernel + '_rd' + str(reducedDim) + '_nClass' + str(n_class))


def createTrainingVec_w2v(filename, useWord, sampleSize, opt, n_class):
    training_data = np.zeros((sampleSize, 200))
    training_labels = np.zeros(sampleSize)
    # w2vモデルの読み込み
    model = word2vec.Word2Vec.load("data/w2v_ng1" + filename + ".model")

    f = open('data/verbDict_w2v_' + filename + '.json', 'r')
    verbDict = json.load(f)
    f.close()

    if sampleSize >= 250000:
        out_list_5000 = [u'くださる', u'迷う', u'質問', u'悩む', u'おねがい', u'助かる',
                         u'おしえる', u'貸す', u'お待ち', u'頂ける', u'アドバイス', u'住む']  # コーパスに5,000文無い動詞のリスト
        for outverb in out_list_5000:
            del verbDict[outverb]  # これらの動詞を辞書から削除

    print "n_class :", n_class
    # n_classの数だけ候補になる動詞をランダムで取得
    verb_list = random.sample(verbDict, n_class)

    newVerbDict = {}
    for verb in verb_list:
        print verb.encode('utf-8'), verbDict[verb]
        newVerbDict[verb] = verbDict[verb]

    n_each = sampleSize / n_class
    temp_line = []
    counter = 0
    noVerb_flag = True
    labelnum = 0
    counter_l = 0
    temp_training_data = []
    vplace_list = []
    for key, value in sorted(newVerbDict.items(), key=lambda x: int(x[1]), reverse=False):
        # print value.encode('utf-8'), labelnum
        for line in open("data/trainingData_w2v_" + filename + ".tsv", 'r'):
            _, vplace, verb, sentence = line.split('\t')
            if verb == key.encode('utf-8') and useWord < int(vplace):
                if counter < n_each:
                    vplace_list.append(vplace)
                    temp_line.append(sentence)
                    training_labels[counter_l] = labelnum
                    counter_l += 1
                else:
                    counter = 0
                    noVerb_flag = False
                    break
                counter += 1
            noVerb_flag = True
        if noVerb_flag:
            print "there isn't this verb in corpus: verb ", value.encode('utf-8')
            return (None, None)
        print key.encode('utf-8'),
        labelnum += 1
    print ""

    counter_s = 0
    counter_w = 0
    for sentence in temp_line:
        temp_training_data = np.zeros(200)
        for word in sentence.split(" "):

            # 今回はただの和
            try:
                temp_training_data += model[unicode(word, 'utf-8')]
                counter_w += 1
            except:
                # print word, " is not in the dictionary."
                counter_w += 1

            if opt == "all_w2v":
                if counter_w >= int(vplace_list[counter_s])-1:
                    counter_w = 0
                    break
            else:
                if counter_w >= useWord:
                    counter_w = 0
                    break

        training_data[counter_s] = temp_training_data
        counter_s += 1


    shuffle_matrix = np.c_[training_data, training_labels]
    np.random.shuffle(shuffle_matrix)
    for i in range(len(shuffle_matrix)):
        training_data[i] = shuffle_matrix[i][:200]
        training_labels[i] = shuffle_matrix[i][200]


    return (training_data, training_labels)


def w2vSVM(filename, n_folds, useWord, sampleSize, opt, n_class, kernel):

    training_data = np.zeros((sampleSize, 200))
    training_labels = np.zeros(sampleSize)
    iter_flag = True

    # コーパスに述語動詞に対応する文が十分にない時の対処
    while iter_flag:
        training_data, training_labels = createTrainingVec_w2v(filename, useWord, sampleSize, opt, n_class)
        if len(training_labels) > 1:
            iter_flag = False


    # K-分割交差検証
    kfold = cross_validation.KFold(len(training_data), n_folds=n_folds)
    results = np.array([])
    confirmation = []
    counter = 0
    for training, test in kfold:
        counter += 1
        print counter, "folds    ",
        # 教師データで　SVM を学習する
        clf = svm.SVC(kernel=kernel)
        clf.fit(training_data[training], training_labels[training])

        # テストデータを使った検証
        answers = clf.predict(training_data[test])
        # ラベルデータと一致しているか調べる
        are_correct = answers == training_labels[test]
        results = np.r_[results, are_correct]

        pre = np.c_[answers, training_labels[test]]
        confirmation.append(pre)

    print ""
    print('カーネル: {kernel}'.format(kernel=kernel))
    correct = np.sum(results)
    N = len(training_data)
    percent = (float(correct) / N) * 100
    print('正答率: {percent:.2f}% ({correct}/{all})'.format(
        correct=correct,
        all=len(training_data),
        percent=percent,
    ))


def test(filename, useWord, sampleSize, reducedDim, opt, n_class, kernel):
    #verb_Fixedを使う

    test_size = 1000
    iter_flag = True
    if opt == "equal":
        while iter_flag:
            training_data, training_labels, test_data, test_labels = createTrainingVec_Equal_verbFixed(filename, useWord, sampleSize, n_class, test_size)
            if len(training_labels) > 1:
                iter_flag = False

    elif opt == "hist":
        while iter_flag:
            training_data, training_labels, test_data, test_labels, vplace_lists, verb_list = createTrainingVec_Equal_Hist_verbFixed(filename, useWord, sampleSize, n_class, test_size)
            if len(training_labels) > 1:
                iter_flag = False
    else:
        print "What is opt?"

    forPCA = np.r_[training_data, test_data]
    forPCA = DimensionReduction(filename, forPCA, reducedDim)
    training_data = forPCA[:len(training_data)]
    test_data = forPCA[len(training_data):]
    print "size", len(training_data), len(test_data)

    np.savetxt("data/v20000rd100nc100_data.csv", training_data, delimiter=",")
    np.savetxt("data/v20000rd100nc100_labels.csv", training_labels, delimiter=",")

    results = np.array([])
    confirmation = []

    # 教師データで　SVM を学習する
    clf = svm.SVC(kernel=kernel)
    clf.fit(training_data, training_labels)

    # テストデータを使った検証
    answers = clf.predict(test_data)
    # ラベルデータと一致しているか調べる
    results = answers == test_labels

    pre = np.c_[answers, test_labels]
    confirmation.append(pre)

    print ""
    print('カーネル: {kernel}'.format(kernel=kernel))

    correct = np.sum(results)
    N = len(test_data)
    percent = (float(correct) / N) * 100
    print('正答率: {percent:.2f}% ({correct}/{all})'.format(
        correct=correct,
        all=N,
        percent=percent,
    ))


    print results
    print "prediction, correct"
    for x in confirmation:
        for y in x:
            print y[0], "\t", y[1]

    joblib.dump(clf, 'data/SVM/SVM_' + filename + '_verbFixed' + '_clf_' + kernel + '_rd' + str(reducedDim) + '_nClass' + str(n_class))

    if opt == "hist":
        a = 0
        b = test_size
        for verb in verb_list:
            print verb
            vplace_lists_p = vplace_lists[a:b]
            results_p = results[a:b]
            for i, x in enumerate(vplace_lists_p):
                vplace_lists_p[i] = int(float(useWord) * 100 / float(vplace_lists_p[i]))
            vplace_lists_corr = np.zeros(len(vplace_lists_p))
            for i, x in enumerate(results_p):
                if x == 1:
                    vplace_lists_corr[i] = vplace_lists_p[i]
            vplace_lists_corr.sort()
            while True:
                vplace_lists_corr = np.delete(vplace_lists_corr, 0)
                if vplace_lists_corr[0] > 0:
                    break
            Histogram.Histogram(filename, vplace_lists_p, vplace_lists_corr)
            a += test_size
            b += test_size


if __name__ == '__main__':
    main(filename="ans_1", n_folds=5, sampleSize=100000, reducedDim=50, opt="equal", n_class=100)