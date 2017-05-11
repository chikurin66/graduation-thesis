#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def main():
    print "hello"
    df_flights = sns.load_dataset('flights')
    print df_flights.head(5)
    df_flights_pivot = pd.pivot_table(data=df_flights, values='passengers', columns='year', index='month', aggfunc=np.mean)
    sns.heatmap(df_flights_pivot)
    plt.show()

def matrix(filename):
    heatmap_mat = np.zeros((10,10))

    f = open("data/output/" + filename + ".txt", 'r')
    lines = f.readlines()
    f.close()
    index = 0

    n2i = dict()

    labels = list()
    for line in lines[5:15]:
        print line,
        v, n = line.split(' ')

        n2i[int(n)] = index

        labels.append(unicode(v,"utf-8"))
        index += 1

    counter = 0
    data = list()
    for line in lines[23:]:
        a, b = line.rstrip('\n').split('\t')
        data.append([int(float(a.rstrip(' '))), int(float(b))])
        counter += 1
        if counter >= 10000:
            break

    for pred, corr in data:
        heatmap_mat[n2i[corr]][n2i[pred]] += 1

    return (heatmap_mat, labels)


# 正方行列と X および Y のラベルの行列を渡す
def draw_heatmap(filename, data, row_labels, column_labels):
    # 描画する
    fig, ax = plt.subplots()
    heatmap = ax.pcolor(data)

    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)

    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            color = 'black'
            if data[y, x] > 280:
                color = 'white'
            plt.text(x + 0.5, y + 0.5, '%d' % int(data[y, x]),
                     horizontalalignment='center',
                     verticalalignment='center',
                     color=color
                     )

    ax.invert_yaxis()
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.set_xticklabels(row_labels, minor=False)
    ax.set_yticklabels(column_labels, minor=False)
    plt.xlabel(u"分類されたクラス")
    plt.ylabel(u"本当のクラス")
    plt.savefig('data/output/heatmap_' + filename + '.png')
    plt.show()
    return heatmap

if __name__ == '__main__':
    # main()
    filename = "1_14_heatmap4"
    heatmap = np.zeros((10,10))
    heatmap, labels = matrix(filename)
    # labels = [u"a", u"b", u"c", u"d", u"e", u"f", u"g", u"h", u"i", u"j" ]
    draw_heatmap(filename, heatmap, labels, labels)