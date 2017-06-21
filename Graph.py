#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from graphviz import Digraph
import networkx as nx
import codecs


def makeDiGraph(edge_list):
    color = ["white", "#F5BCA9", "#FE642E", "#DF3A01", "#B43104", "#61210B"]

    with codecs.open('data/goiDict.json', 'r', 'utf-8') as f:
        goiDict = json.load(f)

    G = Digraph(format='svg')
    # 属性(attribute)の設定: nodeの形をcircleに
    G.attr('node', shape='circle', style="filled")

    for edge in edge_list:
        for node in edge:
            if node in goiDict:
                if goiDict[node] == 6:
                    fc = "white"
                else:
                    fc = "black"
                G.node(node, fillcolor=color[goiDict[node]-1], fontcolor=fc)
            else:
                print node
    for edge in edge_list:
        # 係り受け元->係り受け先
        G.edge(edge[1], edge[0])

    rank_set = set()
    rank_list = []
    for i in range(len(color)):
        for edge in edge_list:
            for node in edge:
                if node in goiDict and goiDict[node]-1 == i:
                    rank_set.add(node)
        rank_list.append(list(rank_set))
        rank_set = set()

    for rs in rank_list:
        G.body.append(u"{{rank=same; " + u"; ".join(rs) + u";}}")

    print G.source
    G.render('data/goiGraph_rank.gv', view=True)


def makeGEXF(edge_list):

    G = nx.DiGraph()
    # G.add_node(u"spam")
    # G.add_edge(u"あ", u"い")
    # G.add_node(u"漢字")
    # G.add_node(u"字")
    for edge in edge_list:
        G.add_edge(edge[0], edge[1])
        for e in edge:
            G.node[e]['viz'] = {'size': 50,
                                'color': {'r': 150, 'g': 150, 'b': 150}}

    # Add VIZ extension for GEXF writer.
    # G.node["spam"]['viz'] = {'size': 10,
    #                          'color': {'r': 255, 'g': 0, 'b': 0},
    #                          'position': {'x': 0, 'y': 0}}
    # G.node["c"]['viz'] = {'size': 10,
    #                          'color': {'r': 255, 'g': 0, 'b': 0},
    #                          'position': {'x': 0, 'y': 0}}
    # G.node["a"]['viz'] = {'size': 10,
    #                     'color': {'r': 0, 'g': 255, 'b': 0},
    #                     'position': {'x': 100, 'y': 100}}
    # G.node["b"]['viz'] = {'size': 10,
    #                     'color': {'r': 0, 'g': 0, 'b': 255},
    #                     'position': {'x': 200, 'y': 200}}

    nx.write_gexf(G, "data/goi.gexf")


if __name__ == '__main__':
    edge_list = []
    opt = "e2d"
    f = open('data/aggregatedDict_' + opt + '.json', 'r')
    agg_dict = json.load(f)
    f.close()
    mc = 2  # Minimum count
    for key, value in agg_dict.items():
        if len(value) < mc:
            continue
        for v in value:
            if key != v:
                edge_list.append([key, v])

    makeDiGraph(edge_list)
    # makeGEXF(edge_list)
