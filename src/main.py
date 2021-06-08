# -*- coding: utf-8 -*-
# @Time    : 2021.5.2
# @Author  : Aman

import os
import time as t
from MapReduce import MapReduce
from MultiProcess import Processor
import pickle

def main():
    text_file = "../data/news_tensite_xml.dat"
    # text_file1 = "../data/news_tensite_xml.smarty.dat"
    stp_wds = "../cn_stopwords.txt"
    workers_num = 32  # num of multiprocers
    # chunksize = 6
    vocab_size = 50000

    START_TIME = t.time()

    P = Processor(stp_wds)

    mapper = MapReduce(P.file_to_words, P.count_words, workers_num)
    indexes, mapping_time, reformatting_time, reducing_time = mapper(inputs=[text_file])

    indexes.sort(key=lambda x : x[1])
    indexes.reverse()
    indexes = indexes[:vocab_size]
    print(f"Total_indexes: {min(len(indexes), vocab_size)}")
    # print(list(indexes)[0], list(indexes)[1], list(indexes)[2])

    # K = 20  # num of top words
    # print(f"\nTOP {K} WORDS BY FREQUENCY\n")
    # top_k = indexes[:K]
    # longest = max(len(word) for word, count, _ in top_k)
    # for word, count, _ in top_k:
    #     print('%-*s: %5s' % (longest+1, word, count))
    
    END_TIME = t.time()

    print("\nMapping time = {} s".format(mapping_time))
    print("Reformatting time = {} s".format(reformatting_time))
    print("Reducing time = {} s".format(reducing_time))
    print("Total running time = {:2f} s".format(END_TIME - START_TIME))

    save_path = '../data/index_all.pkl'
    f = open(save_path, 'wb')
    pickle.dump(indexes, f)
    f.close()
    print(f"Indexes saved to file {save_path}")


if __name__ == '__main__' :
    main()