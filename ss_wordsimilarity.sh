#!bin/sh

for sz in 800
do
    for mc in 1
    do
        for ng in 0
        do
            python Spearman.py sg1_sz${sz}_mc${mc}_wd10_hs1_ng${ng}_ans_1
        done
    done
done

