# -*- coding: utf-8 -*-
# @Time    : 2021.5.2
# @Author  : Aman

import os
import re
import string
import multiprocessing
import pkuseg


class Processor():
    def __init__(self, stopwords_f):
        self.stopwords = self.load_stopwords(stopwords_f)
        self.seg = pkuseg.pkuseg()

    def load_stopwords(self, fp):
        """Load stop words list
        """
        with open(fp, 'r') as f:
            stopwords = f.readlines()
        stopwords = [i.replace('\n','') for i in stopwords]
        return stopwords

    def is_all_chinese(self, strs):
        """Check if a string is all Chinese characters
        """
        for c in strs:
            if not '\u4e00' <= c <= '\u9fa5':
                return False
        return True

    def file_to_words(self, item):
        """Read a file and return a list of (word, occurances) values.
        """
        filename, size_of_chunk = item
        
        print(multiprocessing.current_process().name, 'reading', filename)

        PUNC = "！“”#$￥%&‘’（）*+，-。/：；<=>？@【\】^—·_`{|}~、"
        PUNC = str.maketrans(PUNC, ' ' * len(PUNC))
        res = []
        r_title = r'<contenttitle>(.*?)</contenttitle>'
        r_content = r'<content>(.*?)</content>'
        title = ''
        content = ''
        k = int(filename.split('_')[1].split('.')[0])  # the k-th chunk
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if '<contenttitle>' in line:
                    title = re.findall(r_title, line)
                elif '<content>' in line:
                    content = re.findall(r_content, line)
                    content_line = k * size_of_chunk + i  # save the line of content
                else:
                    continue
                if title and content:
                    # print(title, type(title))
                    text = str(title) + ' ' + str(content)
                    text = text.translate(PUNC)  # Strip punctuation
                    seg_list = self.seg.cut(line)
                    for word in seg_list:                      
                        if self.is_all_chinese(word) and word not in self.stopwords and len(word) > 1:
                            res.append((word, content_line))
                    title = ''
                    content = ''
        return res

    def count_words(self, item):
        """Convert the partitioned data for a word to a tuple (word, the number of occurances)
        """
        # print(item)
        word, occurances = item[0], len(item[1])
        return (word, occurances, item[1])
    
