# coding: UTF-8

from gensim.models import word2vec
import logging


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
    print model[w]
    results = model.most_similar(positive=[w, u"女"], negative=u"男", topn=10)
    # results = model.most_similar(positive=w, topn=10)
    # ライオン　ー　猫　＋　犬　＝　オオカミ？
    # 王様　ー　男　＋　女　＝　女王

    for result in results:
        print result[0], '\t', result[1]


if __name__ == '__main__':
    # train("neko")
    # similar("neko", unicode("書生", "utf-8"))
    # train("ans_1")
    similar("ans_1", u"王様")