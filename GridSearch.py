#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from Heatmap import draw_heatmap
import datetime

def get_labels(sentence):
    sentences = sentence.split('\n')
    labels = list()
    for s in sentences[2:-3]:
         labels.append(s.split(' ')[8])
    return labels


def Gridsearch(training_data, training_labels):

    X_train, X_test, y_train, y_test = train_test_split(training_data, training_labels, test_size=0.2, random_state=0)

    print "X_train:", len(X_train), "    X_test:", len(X_test)

    # 最適化したいパラメータをリストで定義
    tuned_parameters = [
        {'C': [0.01, 0.1, 1, 10, 100, 1000], 'kernel': ['linear']},
        {'C': [0.01, 0.1, 1, 10, 100, 1000], 'kernel': ['rbf'], 'gamma': [0.1, 0.01, 0.001, 0.0001]},
        # {'C': [0.01, 0.1, 1, 10, 100, 1000], 'kernel': ['poly'], 'degree': [2, 3, 4, 5], 'gamma': [0.01, 0.001, 0.0001]},
        # {'C': [0.01, 0.1, 1, 10, 100, 1000], 'kernel': ['sigmoid'], 'gamma': [0.01, 0.001, 0.0001]}
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
    d = datetime.datetime.today()
    filename = "_".join(d.strftime("%x").split('/'))
    labels = get_labels(classification_report(y_true, y_pred))
    draw_heatmap(filename, confusion_matrix(y_true, y_pred), labels, labels)


if __name__ == '__main__':
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

    Gridsearch(training_data, training_labels)
