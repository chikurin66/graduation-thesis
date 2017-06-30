# !/usr/bin/python
# coding:utf8
# Reference Page: 
#   en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient

import sys
import csv
import collections
import numpy as np
from gensim.models import word2vec
import MeCab



# -------Spearman function------------
# ρ = 1 - [(6 * ∑D^2) / (N^3 - N) ]
# D = the difference between ranks
def normal_spearman(tuple_list, N):
    return 1 - ((6 * sum([(rank_a - rank_b) ** 2 for rank_a, rank_b in tuple_list])) / float(N ** 3 - N))


# T = (N^3 - N - Σ(t^3 - t) ) / 12
def sigma(counter, N, sigma_sum=0):
    for rank, num in sorted(counter.items(), key=lambda x: -x[1]):
        if num == 1: break
        sigma_sum += num ** 3 - num
    return (N ** 3 - N - sigma_sum) / 12


# consider the same order 
# ρ = (Tx + Ty - ΣD^2) / (2 * √(Tx * Ty) )
# T = (N^3 - N - Σ(t^3 - t) ) / 12
def same_order_spearman(tuple_list, N):
    counter_a = collections.Counter(); counter_b = counter_a.copy()
    sum_d = 0
    for rank_a, rank_b in tuple_list:
       sum_d += (rank_a - rank_b) ** 2
       counter_a[rank_a] += 1; counter_b[rank_b] += 1
    ta = sigma(counter_a, N); tb = sigma(counter_b, N)
    if ta == 0 or tb == 0:
        return 0
    return (ta + tb - sum_d) / (2 * ((ta ** .5) * (tb ** .5) ) )


# if exist same_rank, change the rank to the average 
def change_rank_num(list_x):
    return [len([1 for rank in list_x if rank < x]) + \
        float(list_x.count(x) - 1) / 2 + 1 for x in list_x]

# -------------main-----------------
# tuple = (rank_a, rank_b)
def Spearman(tuple_list):
    list_length = len(tuple_list)
    ranks_a, ranks_b = zip(*tuple_list)
    pattern = 0
    if max(ranks_a) != list_length: ranks_a = change_rank_num(ranks_a)
    else: pattern += 1
    if max(ranks_b) != list_length: ranks_b = change_rank_num(ranks_b)
    else: pattern += 1
    if pattern == 2: return normal_spearman(tuple_list, list_length)
    else: return same_order_spearman(zip(ranks_a, ranks_b), list_length)


def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def get_w2v_similarity(key, model, show=False):
    # key = 動詞1,動詞2
    verbs = key.split(',')

    tagger = MeCab.Tagger('mecabrc')
    verb_pair = ["", ""]
    for i, verb in enumerate(verbs):
        result = tagger.parse(verb)
        for line in result.split('\n'):
            if "\t" in line:
                sur, others = line.split('\t')
                elems = others.split(',')
                if elems[0] == "動詞":
                    verb_pair[i] = elems[6]
                    break
                elif elems[1] == "サ変接続":
                    verb_pair[i] = elems[6]
                    break

    for i in range(2):
        verb_pair[i] = verb_pair[i].decode('utf-8')

        if show:
            if verb_pair[i] in model:
                print "Yes:", verb_pair[i], "(", verbs[i], ")"
            else:
                print "No :", verb_pair[i], "(", verbs[i], ")"
    if show:
        print " "

    if verb_pair[0] in model and verb_pair[1] in model:
        similarity = cos_sim(model[verb_pair[0]], model[verb_pair[1]]) * 10
        # print "   verb :", verb1, verb2
    else:
        similarity = 0
        # print "No verb :", verb1, verb2

    return similarity


# ---------------test---------------------
if __name__ == '__main__':
    #sample_tuple_list = [(1, 5), (2, 4), (3, 3), (4, 3), (5, 1)]
    #print ('--------Spearman-------')
    #print (Spearman(sample_tuple_list))

    try:
        modelName = sys.argv[1]
    except:
        modelName = "ans_1"
    print "model is", "w2v_" + modelName + ".model"
    model = word2vec.Word2Vec.load("data/w2v_" + modelName + ".model")
    l = list()
    # filename = sys.argv[1]
    filename = "data/score_verb.csv"
    with open(filename, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            key = row[0]+","+row[1]
            # csv内にあるコンピュータが出した類似度を一番最後になるようにしてください。
            # l.append((key, float(row[2]), float(row[-1])))
            l.append((key, float(row[2]), float(get_w2v_similarity(key, model=model, show=True))))

    w2rank_hum = dict()
    w2rank_w2v = dict()
    real_rank = 0
    score = 1000000000
    for rank, (key, hum_score, _) in enumerate(sorted(l, key=lambda x: -x[1])):
        if hum_score == score:
            w2rank_hum[key] = real_rank
        else:
            real_rank = rank + 1
            w2rank_hum[key] = real_rank
        score = hum_score
    real_rank = 0
    score = 10000000
    for rank, (key, _, w2v_score) in enumerate(sorted(l, key=lambda x: -x[2])):
        if w2v_score == score:
            w2rank_w2v[key] = real_rank
        else:
            real_rank = rank + 1 
            w2rank_w2v[key] = real_rank
        score = w2v_score

    tuple_list = []
    for key in w2rank_w2v.keys():
        tuple_list.append((w2rank_hum[key], w2rank_w2v[key]))
    # print(tuple_list)
    # print ('--------Spearman-------')
    print modelName
    print Spearman(tuple_list)
    print ""



