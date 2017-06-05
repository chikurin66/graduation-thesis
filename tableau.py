# -*- coding: utf-8 -*-
import numpy as np , pandas as pd
from collections import OrderedDict
import json
import string


def read_file(inFile, rightCol):
    #両カルムありのcsv
    z = pd.read_csv(inFile, encoding='utf-8', delimiter='\t', header=None)
    #右側のカラムだけのcsv
    zz = pd.read_csv(rightCol, encoding='utf-8', delimiter='\t', header=None)
    return z, zz


def output_file(z, outFile):
    # outFile = input('input output file name->')
    z.to_csv(outFile, index=False)


def sigmoid():
    sigm = {}
    y_value = [-6.0 + i / 2 for i in range(0,25)]
    for i in y_value:
        sigm[i] = 1/(1+np.exp(-i))
    return sigm


def make_file(inFile, rightCol, outFile):
    height = 50
    df, cluster2 = read_file(inFile,  rightCol)
    cluster1=[]
    for i in range(0, len(df)):
        a=df.ix[i,0]
        if not a in cluster1:
            cluster1.append(a)

    index1,index2 = {},{}
    for i in range(len(cluster2)):
        index2[cluster2.ix[i,0]] = height*(1/2+i)/len(cluster2)
    for i in range(len(cluster1)):
        index1[cluster1[i]] = height*(1/2+i)/len(cluster1)
    out = []
    """
    for i in range(0,len(index)):

        bin_1, bin_2 = height/len(index) , height/len(cluster_2)
        s,g = index[df.ix[i,0]][0], index[df.ix[i,0]][1]
        print(bin_1,bin_2)
        for j in range(s,s+g):
            start ,goal = bin_1/2 + i * bin_1 , bin_2/2 + (j-s)*bin_2
            out.append([df.ix[i,0], start , goal , df.ix[j,1] ,df.ix[i,2]])
    """

    for i in range(len(df)):
        start, goal = index1[df.ix[i, 0]], index2[df.ix[i, 1]]
        out.append([df.ix[i, 0], start, goal, df.ix[i, 1], df.ix[i, 2]])

    print(len(out))
    sigm = sigmoid()
    output = []
    for i in range(0,len(out)):
        ss,gg = out[i][1],out[i][2]
        for j in sigm.keys():
            if ss <= gg:
                tmp = sigm[j] *(gg - ss) + ss
            else:
                tmp = sigm[-j] * (ss - gg) + gg
            output.append([out[i][0], j, tmp, out[i][3], out[i][4]])
    output_df = pd.DataFrame(output, columns=['Easy', 'Y', 'Curve', 'Difficult', 'Thickness'])
    output_file(output_df, outFile)


def make_first_tsv():
    f1 = open('data/aggregatedDict_e2d.json', 'r')
    agg_e2d = json.loads(f1.read(), 'utf-8')
    f1.close()

    line_list = list()
    for key, value in agg_e2d.items():
        for v in value:
            line = key + "\t" + v + "\t" + "1\n"
            line_list.append(line.encode('utf-8'))

    fo = open('data/input_tableau.tsv', 'w')

    fo.writelines(line_list)
    fo.close()


def make_rightCol():
    f1 = open('data/aggregatedDict_d2e.json', 'r')
    agg_d2e = json.loads(f1.read(), 'utf-8')
    f1.close()
    line_list = list()
    for key in agg_d2e.keys():
        line_list.append(key.encode('utf-8') + '\n')

    fo = open('data/rightCol.csv', 'w')
    # fo.writelines(line_list)

    fo.writelines(line_list)
    fo.close()


if __name__ == "__main__":
    # python3で使うとうまくいく

    # make_first_tsv()
    # make_rightCol()
    make_file(inFile='data/input_tableau.tsv', rightCol="data/rightCol.csv", outFile=u"data/output_tableau.csv")
