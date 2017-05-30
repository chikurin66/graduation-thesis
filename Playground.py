#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import json
from sklearn import cross_validation
from sklearn import decomposition
import random
import time
import Histogram
from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import Heatmap
from scipy.sparse import lil_matrix, csr_matrix
from gensim.models import word2vec

def Gridsearch():
    # digits = datasets.load_digits()
    # n_samples = len(digits.images)  # 標本数 1797個
    # X = digits.images.reshape((n_samples, -1))  # 8x8の配列から64次元のベクトルに変換
    # y = digits.target  # 正解ラベル
    #
    # # データセットをトレーニング用とテスト用に2分割
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)
    #
    # print len(X_train)

    # Iris データセットを使う
    iris = datasets.load_iris()
    features = iris.data
    target = iris.target
    target_names = iris.target_names
    labels = target_names[target]

    # Petal length と Petal width を特徴量として取り出す
    setosa_petal_length = features[labels == 'setosa', 2]
    setosa_petal_width = features[labels == 'setosa', 3]
    setosa = np.c_[setosa_petal_length, setosa_petal_width]
    versicolor_petal_length = features[labels == 'versicolor', 2]
    versicolor_petal_width = features[labels == 'versicolor', 3]
    versicolor = np.c_[versicolor_petal_length, versicolor_petal_width]
    virginica_petal_length = features[labels == 'virginica', 2]
    virginica_petal_width = features[labels == 'virginica', 3]
    virginica = np.c_[virginica_petal_length, virginica_petal_width]

    # print setosa
    # setosa = np.c_[setosa, np.random.randn(len(setosa), 1)]
    # versicolor = np.c_[versicolor, np.random.randn(len(versicolor), 1)]
    # virginica = np.c_[virginica, np.random.randn(len(virginica), 1)]

    # 教師信号を作る
    training_data = np.r_[setosa, versicolor, virginica]
    training_labels = np.r_[
        np.zeros(len(setosa)),
        np.ones(len(versicolor)) * 1,
        np.ones(len(versicolor)) * 2,
    ]

    X_train, X_test, y_train, y_test = train_test_split(training_data, training_labels, test_size=0.5, random_state=0)

    print len(y_train)
    # 最適化したいパラメータをリストで定義
    tuned_parameters = [
        {'C': [0.01, 0.1, 1, 10, 100, 1000], 'kernel': ['linear']},
        {'C': [0.01, 0.1, 1, 10, 100, 1000], 'kernel': ['rbf'], 'gamma': [0.01, 0.001, 0.0001]},
        {'C': [0.01, 0.1, 1, 10, 100, 1000], 'kernel': ['poly'], 'degree': [2, 3, 4, 5], 'gamma': [0.01, 0.001, 0.0001]},
        {'C': [0.01, 0.1, 1, 10, 100, 1000], 'kernel': ['sigmoid'], 'gamma': [0.01, 0.001, 0.0001]}
    ]

    # 上で定義したパラメータを最適化
    score = 'accuracy'
    clf = GridSearchCV(
        SVC(),  # 識別器
        tuned_parameters,  # 最適化したいパラメータセット
        cv=5,  # 交差検定の回数
        scoring=score)  # モデルの評価関数の指定
    clf.fit(X_train, y_train)

    print "# Tuning hyper-parameters for %s" % score
    print ""
    print "Best parameters set found on development set: %s" % clf.best_params_
    print ""

    # それぞれのパラメータでの試行結果の表示
    print "Grid scores on development set:"
    print ""
    for params, mean_score, scores in clf.grid_scores_:
        print "%0.4f (+/-%0.03f) for %r" % (mean_score, scores.std() * 2, params)
    print ""

    # テストデータセットでの分類精度を表示
    print "The scores are computed on the full evaluation set."
    print ""
    y_true, y_pred = y_test, clf.predict(X_test)
    print classification_report(y_true, y_pred)

    print confusion_matrix(y_true, y_pred)  # クラスタリング結果を表示

    # # 評価関数を指定
    # scores = ['accuracy', 'precision', 'recall']
    # param_grid = tuned_parameters2
    # # 各評価関数ごとにグリッドサーチを行う
    # for score in scores:
    #     print score
    #     clf = GridSearchCV(SVC(C=1), param_grid, cv=5, scoring=score,
    #                        n_jobs=-1)  # n_jobs: 並列計算を行う（-1 とすれば使用PCで可能な最適数の並列処理を行う）
    #     clf.fit(X_train, y_train)
    #
    #     print clf.best_estimator_  # 最適なパラメータを表示
    #
    #     for params, mean_score, all_scores in clf.grid_scores_:
    #         print "{:.3f} (+/- {:.3f}) for {}".format(mean_score, all_scores.std() / 2, params)
    #
    #     # 最適なパラメータのモデルでクラスタリングを行う
    #     y_true, y_pred = y_test, clf.predict(X_test)
    #     print classification_report(y_true, y_pred)  # クラスタリング結果を表示
    #     print confusion_matrix(y_true, y_pred)  # クラスタリング結果を表示

    # # グラフを表示する
    # plt.autoscale()
    # plt.grid()
    # plt.show()


def main():
    return True


def loadMat():
    training_data = np.loadtxt("data/confusionMatEx.csv", delimiter=",")
    labels = [1,2,3,3,4,6,7,10,25,67]
    Heatmap.draw_heatmap("fixedCM_Ex", training_data, labels, labels)


def DimensionReduction(filename, vector_list, reducedDim):
    print "PCA starts"
    print "reduced dimension :", reducedDim
    start = time.time()

    pca = decomposition.SparsePCA(reducedDim)
    result = pca.fit_transform(vector_list)

    np.savetxt("data/reducedVec_" + filename + "_dim" + str(reducedDim) + ".csv", result, delimiter=",")
    elapsed_time = time.time() - start
    print "PCA finish : %s [min]" % (elapsed_time / 60)
    return result

def database():

    data_list = ()
    counter = 0
    for line in open("data/kishou.csv", 'r'):
        if counter >= 6:
            #print counter, line
            date, _, _, _, _, avgT, _, _, maxT, _, _, minT, _, _ = line.split(",")

            temp_data_list = date.split("/")
            if len(temp_data_list[1]) == 1:
                temp_data_list[1] = "0"+temp_data_list[1]
            if len(temp_data_list[2]) == 1:
                temp_data_list[2] = "0"+temp_data_list[2]

            print "-".join(temp_data_list), "00:00:00,", avgT
        counter += 1


if __name__ == '__main__':
    #Gridsearch()
    #loadMat()

    # # 疎行列bを用意する
    # matrix = lil_matrix((3, 3))
    # # 非ゼロ要素を設定する
    # matrix[1, 1] = 3
    # matrix[2, 0] = 4
    # matrix[2, 2] = 5
    #
    # # lil_matrixをcsr_matrixに変換する
    # matrix = matrix.tocsr()
    #
    # result = DimensionReduction("ans_1", matrix, 2)
    # print result
    # database()
    # start = time.time()
    # # vectorData.csv -> classify by SVM
    # counter = 0
    # f = open("data/trainingData_ans_1.csv", "r")
    # while True:
    #     counter += 1
    #     l = f.readline()
    #     if counter > 500000:
    #         break
    #
    # elapsed_time = time.time() - start
    # print "%s [sec]" % (elapsed_time)
    # f.close()
    #
    # start = time.time()
    # # vectorData.csv -> classify by SVM
    # counter = 0
    # for line in open("data/trainingData_ans_1.csv", "r"):
    #     counter += 1
    #     l = line
    #     if counter > 500000:
    #         break
    #
    # elapsed_time = time.time() - start
    # print "%s [sec]" % (elapsed_time)

    model = word2vec.Word2Vec.load("data/w2v_ng1ans_1.model")
    print type(model)
    print model.vector_size
