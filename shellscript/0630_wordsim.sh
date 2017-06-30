#!bin/sh

for ng in 0 5 1
do
    for mc in 1 5 10
    do
        for sz in 100 200 400 800 
        do
            python Spearman.py sg1_sz${sz}_mc${mc}_wd10_hs1_ng${ng}_ans_1 | tee -a data/output/0630_w2v_sim_2.txt
        done
    done
done

