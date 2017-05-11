# coding: UTF-8


import Morphs
import VerbExtraction
import StopWord
import CreateVector
import SVM
import time
import datetime


def main(filename, stopWord, vocabSize, useWord, reducedDim, opt, sampleSize, n_class, kernel, vecName, gs):

    Morphs_flag = False
    VerbExtraction_flag = False
    StopWord_flag = False
    CreateVector_flag = False
    SVM_flag = False
    SVM_w2v_flag = True
    SVM_test_flag =False

    if Morphs_flag:
        # filename.tsv -> planeText.txt
        Morphs.PlaneText(filename)
        print "PlaneText has done."

        # planeText.txt -> filename.cabocha
        Morphs.Dependency(filename)
        print "Dependency has done."

    if VerbExtraction_flag:
        # filename.cabocha -> trainingData.csv
        VerbExtraction.extractVerb(filename)
        print "extractVerb has done."

        # trainingData.csv -> verbDict.json
        VerbExtraction.createVerbDict(filename, verbDictSize=100)
        print "createVerbDict has done."

    if StopWord_flag:
        # # dependency.cabocha (trainingData.csv) -> allWordDict.json
        # StopWord.extractAllWord(filename)
        # print "extractAllWord has done."

        # allWordDict.json -> stopList.txt
        StopWord.dictToStopwordList(filename, k=stopWord)
        print "dictToStopwordList has done."

        # allWordDict.json -> vocabDict.json
        StopWord.createVocabDict(filename, k=stopWord, vocabSize=vocabSize)
        print "createVocabDict has done."

        # StopWord.showDict(filename, dictName="verbDict", k=100, showAll=False)

    if CreateVector_flag:
        start = time.time()
        # trainingData.csv(+vocabDict.json +verbDict.json) -> vectorData.csv
        if opt == "equal":
            CreateVector.CreateVector(filename, useWord, verbDictSize=100, removeVerb=10)
        elif opt == "hist":
            CreateVector.CreateVector_Hist(filename, useWord, verbDictSize=100, removeVerb=10)
        elif opt =="hist_all":
            CreateVector.CreateVector_Hist_fullword(filename, useWord, verbDictSize=100, removeVerb=10)
        else:
            print "what is option?"
        elapsed_time = time.time() - start
        print "CreateVector has done : %s [min]" % (elapsed_time / 60)

    if SVM_flag:
        start = time.time()
        # vectorData.csv -> classify by SVM
        SVM.main(filename, n_folds=5, useWord=useWord, sampleSize=sampleSize, reducedDim=reducedDim, opt=opt, n_class=n_class, kernel=kernel, vecName=vecName, gridsearch=gs)
        elapsed_time = time.time() - start
        print "SVM has done : %s [min]" % (elapsed_time / 60)

    if SVM_w2v_flag:
        start = time.time()
        # vectorData.csv -> classify by SVM
        SVM.w2vSVM(filename, n_folds=5, useWord=useWord, sampleSize=sampleSize, opt=opt, n_class=n_class, kernel=kernel)
        elapsed_time = time.time() - start
        print "SVM has done : %s [min]" % (elapsed_time / 60)

    if SVM_test_flag:
        start = time.time()
        # vectorData.csv -> classify by SVM
        SVM.test(filename, useWord, sampleSize, reducedDim, opt, n_class, kernel)
        elapsed_time = time.time() - start
        print "SVM has done : %s [min]" % (elapsed_time / 60)


if __name__ == '__main__':

    # for x in [2, 5, 10, 20, 50, 100, 300, 500]:
    #     print "reducedDim =", x

    #     main(filename="ans_1", stopWord=10, vocabSize=20000, useWord=10, reducedDim=x, equal_flag=True, sampleSize=10000, n_class=2)
    #     print "\n"

    d = datetime.datetime.today()
    print d.strftime("%x %X"), "\n"

    # for rd in [2, 5, 10, 20, 50, 200, 500]:
    #     for n in [2, 5, 10, 50, 80]:
    #         for i in range(5):
    #             print "rd :", rd, "    n_class :", n, "    i :", i
    #             try:
    #                 main(filename="ans_1", stopWord=10, vocabSize=20000, useWord=10, reducedDim=rd, equal_flag=True, sampleSize=10000, n_class=n)
    #                 print "\n"
    #             except Exception as e:
    #                 print "An error happened :"
    #                 print e.message
    #                 print str(e), "\n"

    # rd = 100
    # # ほんとはもっと精度のいい条件でカーネルを比べたほうがいいかもしれん．
    # # 今回は時間がないのでこれまで
    # for n_class in [2, 50, 80]:
    #     for j in range(5):
    #         print "Kernel :", "linear", "    rd :", rd, "    n_class :", n_class, "    newVec(PCA)　j：", j
    #         try:
    #             main("ans_1", 10, 20000, 10, rd, True, 10000, n_class, kernel="linear", vecName="new")
    #             print "\n"
    #         except Exception as e:
    #             print "An error happened :"
    #             print e.message
    #             print str(e), "\n"
    #         print "\n"
    #         print "finish creating reduced dimension vector by PCA"
    #
    #         for knl in ["linear", "poly", "rbf", "sigmoid"]:
    #             for i in range(1):
    #                 try:
    #                     print "Kernel :", knl, "    rd :", rd, "    n_class :", n_class, "    i :", i
    #                     main("ans_1", 10, 20000, 10, rd, True, 10000, n_class, kernel=knl, vecName="v20000rd100nc100")
    #                     print "\n"
    #                 except Exception as e:
    #                     print "An error happened :"
    #                     print e.message
    #                     print str(e), "\n"

    # knl = "linear"
    # for rd in [2, 10, 50, 200]:
    #     for n_class in [2, 10, 50, 100]:
    #         for i in range(5):
    #             try:
    #                 print "Kernel :", knl, "    rd :", rd, "    n_class :", n_class, "    i :", i
    #                 main("ans_1", 10, 20000, 10, rd, True, 10000, n_class, kernel=knl, vecName="new")
    #                 print "\n"
    #             except Exception as e:
    #                 print "An error happened :"
    #                 print e.message
    #                 print str(e), "\n"

    # knl = "linear"
    #
    # for rd in [200]:
    #     for n_class in [10]:
    #         for i in range(1):
    #             try:
    #                 print "Kernel :", knl, "    rd :", rd, "    n_class :", n_class, "    i :", i
    #                 main("ans_1", 10, 20000, 10, rd, True, 10000, n_class, kernel=knl, vecName="new")
    #                 print "\n"
    #             except Exception as e:
    #                 print "An error happened :"
    #                 print e.message
    #                 print str(e), "\n"

    # rd = 100
    # n_class = 10
    # uw = 20
    # knl = "linear"
    # print "Kernel :", knl, "    rd :", rd, "    n_class :", n_class, "    uw :", uw
    # main("ans_0", 10, 20000, uw, rd, "equal", 10000, n_class, kernel=knl, vecName="new")

    # knl = "linear"
    # n_class = 10
    # for rd in [200]:
    #     for uw in [15]:
    #         for i in range(1):
    #             try:
    #                 print "Kernel :", knl, "    rd :", rd, "    n_class :", n_class, "    uw :", uw, "    i :", i
    #                 main("ans_1", 10, 20000, uw, rd, "hist ", 10000, n_class, kernel=knl, vecName="new")
    #                 print "\n"
    #             except Exception as e:
    #                 print "An error happened :"
    #                 print e.message
    #                 print str(e), "\n"

    # knl = "gridsearch"  # 意味ないが設定
    # rd = 200
    # n_class = 10
    # uw = 15
    # i = 0  # 意味ないが設定
    #
    # print "Kernel :", knl, "    rd :", rd, "    n_class :", n_class, "    uw :", uw, "    i :", i
    # main("ans_1", 10, 20000, uw, rd, "equal", 10000, n_class, kernel=knl, vecName="new", gs=True)
    # print "\n"

    # knl = "linear"
    # rd = 200
    # n_class = 10
    # uw = 15 #使う文章に関係するので必要
    # opt = "hist_all"
    # for i in range(5):
    #     try:
    #         print "Kernel:", knl, "    rd :", rd, "    n_class :", n_class, "    uw :", uw, "    opt :", opt, "    i :", i
    #         main("ans_1", 10, 20000, uw, rd, opt, 10000, n_class, kernel=knl, vecName="new", gs=False)
    #         print "\n"
    #     except Exception as e:
    #         print "An error happened :"
    #         print e.message
    #         print str(e), "\n"

    knl = "linear"
    rd = 200
    # n_class = 100
    uw = 15  # 使う文章に関係するので必要
    sampleSize = 10000

    opt = "all_w2v"
    for n_class in [100, 50]:
        for i in range(5):
            try:
                print "Kernel:", knl, "    rd :", rd, "    n_class :", n_class, "    uw :", uw, "    opt :", opt, "    i :", i
                main("ans_1", 10, 20000, uw, rd, opt, sampleSize, n_class, kernel=knl, vecName="new", gs=False)
                print "\n"
            except Exception as e:
                print "An error happened :"
                print e.message
                print str(e), "\n"

    opt = "no_all_w2v"
    for uw in [15]:
        for n_class in [100, 50]:
            for i in range(5):
                try:
                    print "Kernel:", knl, "    rd :", rd, "    n_class :", n_class, "    uw :", uw, "    opt :", opt, "    i :", i
                    main("ans_1", 10, 20000, uw, rd, opt, sampleSize, n_class, kernel=knl, vecName="new", gs=False)
                    print "\n"
                except Exception as e:
                    print "An error happened :"
                    print e.message
                    print str(e), "\n"

    d = datetime.datetime.today()
    print d.strftime("%x %X")
