#!/usr/bin/env python3

'''
    build_ngram_model.py - Python3 file that takes in an input file and 
    outputs a file with the probabilities for each unigram, bigram, and trigram of the input text.

    Author: Sadip Giri (sadipgiri@bennington.edu)
    Date: 04/02/2019
'''

import sys

from unigrams import unigrams_write_format, unigrams_list
from bigrams import bigrams_write_format, bigrams_list
from trigrams import trigrams_write_format, trigrams_list

def ngram_model_level_1(input_file_name, output_file_name):
    '''
        Task: find unigrams, bigrams, trigrams->count, probabilities and write to a file
        Approach:
            1. open the input_file and read unigrams, bigrams, trigrams
            2. open the output-file to write above uni,bi & tri things
            3. counts, probabilities and grams are found respectively in their separate python3 files 
                sothat it would be easier to debug as well as scale it in future!
                also, describtion of each functions are present in their respective function definations!
    '''
    with open(input_file_name, 'r') as in_file:
        sentences_list = in_file.read().splitlines()
        words = unigrams_list(sentences_list)
        bigrams = bigrams_list(sentences_list)
        trigrams = trigrams_list(sentences_list)

    with open(output_file_name, 'w') as out_file:
        data_counts_list = []
        for i in [1,2,3]:
            counts_dict = count_grams(words,bigrams,trigrams,i)
            data_counts_list.append('ngram {0}: type={1} token={2}\n'.format(i,counts_dict['types_count'],counts_dict['tokens_count']))
        out_file.write('\data\ \n')
        out_file.write(''.join(data_counts_list))
        # better to write once as a sentence than one by one which takes ample time!!!

        out_file.write('\n')
        out_file.write('\\1-grams: \n')
        out_file.write(unigrams_write_format(words))

        out_file.write('\n')
        out_file.write('\\2-grams: \n')
        out_file.write(bigrams_write_format(bigrams))
        
        out_file.write('\n')
        out_file.write('\\3-grams: \n')
        out_file.write(trigrams_write_format(trigrams,bigrams))

        out_file.write('\n')
        out_file.write('\end\ ')
    return

def count_grams(words,bigrams,trigrams,ngram):
    '''
        Task: count types(unique words) and words/tokens according to given ngram value.

        Approach:
            use set() data structure to make a list of words unique and then count
            depending on the given ngram value
            e.g. ngram = 1 => count unigrams
    '''
    if ngram == 1:
        return {'types_count':len(set(words)),'tokens_count':len(words)}
    if ngram == 2:
        return {'types_count':len(set(bigrams)),'tokens_count':len(bigrams)}
    if ngram == 3:
        return {'types_count':len(set(trigrams)),'tokens_count':len(trigrams)}
    return

if __name__ == '__main__':
    args_list = sys.argv   
    ngram_model_level_1(args_list[1],args_list[2])

