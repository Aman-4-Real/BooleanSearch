# -*- coding: utf-8 -*-
# @Time    : 2021.5.2
# @Author  : Aman

import sys
import itertools as it
import collections
from timeit import default_timer as timer
import multiprocessing
import itertools

class MapReduce(object):
    
    def __init__(self, map_func, reduce_func, num_workers=None):
        self.map_func = map_func
        self.reduce_func = reduce_func
        self.pool = multiprocessing.Pool(num_workers)
        self.num_workers = num_workers
        # self.chunksize = chunksize
    
    def partition(self, mapped_values):
        """Gather the mapped data
        """
        partitioned_data = collections.defaultdict(list)
        for key, value in mapped_values:
            partitioned_data[key].append(value)
        return partitioned_data.items()
    
    def split_file(self, input_file):
        """Split a single big file into N chunks where N = num_workers
        """
        file_list = []        
        with open(input_file, 'r', encoding='GB18030', errors='ignore') as f_in:
            data = f_in.readlines()
            lines_num = len(data)
            size = lines_num // self.num_workers  # lines splitted in a chunk
            start = 0
            end = size
            w_path = "../data/"
            for i in range(lines_num//size):
                chunk_name = "chunk_" + str(i) + ".dat"
                with open(w_path + chunk_name, 'w', encoding='utf-8') as f_out:
                    f_out.write(''.join(data[start:end]))
                start = start + size
                end = end + size
                file_list.append("../data/chunk_" + str(i) + ".dat")
        
        print(f"File splitted into {self.num_workers} chunks.")
        return file_list, size

    def __call__(self, inputs):
        if not inputs:
            print("Error! No input files!")
            exit(1)
        
        print("Mapping...")
        start = timer()

        size_of_chunk = 0
        if len(inputs) == 1:
            file_list, size_of_chunk = self.split_file(inputs[0])
        else:
            file_list = inputs
        param = list(itertools.product(file_list, [size_of_chunk]))
        map_responses = self.pool.map(self.map_func, param)
        mapping_time = timer() - start
        # print(map_responses)
        print("Formatting...")

        start = timer()
        partitioned_data = self.partition(it.chain(*map_responses))
        # print(list(partitioned_data)[0], list(partitioned_data)[1])
        reformatting_time = timer() - start
        del map_responses

        print("Reducing...")

        start = timer()
        reduced_values = self.pool.map(self.reduce_func, partitioned_data)
        # print(list(reduced_values)[0], list(reduced_values)[1])
        reducing_time = timer() - start
        del partitioned_data

        return reduced_values, mapping_time, reformatting_time, reducing_time