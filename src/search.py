# -*- coding: utf-8 -*-
# @Time    : 2021.5.2
# @Author  : Aman

import pkuseg
from retrival import Retrieval


def main():
    src_file = "../data/news_tensite_xml.dat"
    index_path = '../data/index_all.pkl'
    
    R = Retrieval(src_file, index_path)   

    seg = pkuseg.pkuseg()
    print('\n', '='*20, 'News Search', '='*20, '\n')
    while True:
        query = input("Please input your query (Chinese Only): ")
        if query == 'exit!' or query == 'quit!':
            break
        query_words = seg.cut(query)
        result = R.search(query_words)
        if result[0][0] != 'N':
            print('{} related documents found.'.format(str(len(result))))
            for i, r in enumerate(result):
                if i >= 5:
                    break
                print(f"NO.{i+1} result:")
                print(r + '\n')
        else:
            print('{} related documents found.'.format(str(0)))
        print('\n', '=' * 30, '\n')


if __name__ == '__main__' :
    main()