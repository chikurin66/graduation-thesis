# coding: UTF-8

from gensim.models import word2vec
import logging
import numpy as np


def train(filename):

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    sentences = word2vec.LineSentence("data/resource_w2v_" + filename + ".txt")
    # model = word2vec.Word2Vec(sentences,
    #                           sg=1,
    #                           size=200,
    #                           min_count=1,
    #                           window=10,
    #                           hs=1,
    #                           negative=0)
    model = word2vec.Word2Vec(sentences,
        sg=1,
        size=200,
        min_count=1,
        window=10,
        hs=1,
        negative=1)
    model.save("data/w2v_ng1" + filename + ".model")


def similar(filename, w):
    model = word2vec.Word2Vec.load("data/w2v_" + filename + ".model")
    # print model[w]
    # results = model.most_similar(positive=[w], negative=u"", topn=10)
    # results = model.most_similar(positive=w, topn=10)
    # ライオン　ー　猫　＋　犬　＝　オオカミ？
    # 王様　ー　男　＋　女　＝　女王

    for v in [u"死ぬ", u"消える"]:
        print v
        print cos_sim(model[v], model[u"隠れる"])
        print cos_sim(model[v], model[u"無くなる"])
        print cos_sim(model[v], model[u"亡くなる"])
        print cos_sim(model[v], model[u"旅立つ"])
        print cos_sim(model[v], model[u"果てる"])
        print cos_sim(model[v], model[u"没する"])
        print ""


    # for result in results:
        # print result[0], '\t', result[1]


def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


if __name__ == '__main__':
    # train("neko")
    # similar("neko", unicode("書生", "utf-8"))
    # train("ans_1")
    similar("ans_1", u"")