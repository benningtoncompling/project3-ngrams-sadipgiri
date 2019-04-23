#!/usr/bin/env python3

'''
    ngram_perplexity python3 program to calculate perplexity of the model comparing with the given test file.
    Author: Sadip Giri (sadipgiri@bennington.edu)
    Date: 9th April, 2019
'''

from unigrams import unigrams_counts_dictionary
from trigrams import trigrams_makeup
from math import log10
import sys

# according to Justin's definition of executing the perplexity
args_list = sys.argv
input_file = args_list[1]
lambda1 = float(args_list[2])
lambda2 = float(args_list[3])
lambda3 = float(args_list[4])
test_file = args_list[5]
output_file = args_list[6]


#input_file='dickens_model.txt'
#test_file='dickens_text.txt'

with open(input_file,'r') as in_file:
    sentences = in_file.read().splitlines()

unigram_index = sentences.index('\\1-grams:') 
bigram_index = sentences.index('\\2-grams:')
trigram_index = sentences.index('\\3-grams:')

total_number_of_words = 0
total_number_of_unknown_words = 0

def create_bigram_dict(sentences):
    '''
        Created bigram dict but log probs this time -> same as generate bigram apporach as shown earlier!
    '''
    bigram_dict = {}
    for i in sentences[bigram_index+1: trigram_index - 1]:
        temp_list = i.split()
        if temp_list[3] not in bigram_dict:
            bigram_dict[temp_list[3]] = {temp_list[4]: temp_list[1]}
        else:
            bigram_dict[temp_list[3]][temp_list[4]] = temp_list[1]
    return bigram_dict

def create_trigram_dict(sentences):
    '''
        Created trigram dict but log probs this time -> same as generate trigram apporach as shown earlier!
    '''
    trigram_dict = {}
    for i in sentences[trigram_index+1: len(sentences) - 2]:
        temp_list = i.split()
        if ' '.join(temp_list[3:5]) not in trigram_dict:
            trigram_dict[' '.join(temp_list[3:5])] = {temp_list[5]: temp_list[1]}
        else:
            trigram_dict[' '.join(temp_list[3:5])][temp_list[5]] = temp_list[1]
    return trigram_dict

def create_unigram_dict(sentences):
    '''
        Also, creating unigram dict with log probs reading the model file.
    '''
    unigram_dict = {}
    for i in sentences[unigram_index+1: bigram_index - 1]:
        temp_list = i.split()
        unigram_dict[temp_list[3]] = temp_list[1]
    return unigram_dict

unigram_dict = create_unigram_dict(sentences)
bigram_dict = create_bigram_dict(sentences)
trigram_dict = create_trigram_dict(sentences)

def calculate_perplexity(lambda1, lambda2, lambda3, test_file):
    '''
        for each sentence in the test data file:
            add the number of words in the sentence (excluding <s> and </s>) to the total number of words
            for each word(i) in the sentence (excluding <s>, but including </s>:
                if the word(i) is unknown, increment an unknown word counter and 
                    continue
                Calculate the interpolated log-probability of the trigram as below:
                    log( P(word(i) | word(i-2) word (i-1)))
                Add this log-prob to a running total
        divide the negative sum of the log-probs by the total number of words added to the number of sentences minus the number of unknown words.
        Raise this value to the power of 10
    '''
    total_words = 0
    unknown_words = 0
    total_log_prob = 1
    
    with open(test_file, 'r') as test_file:
        test_sentences = test_file.read().splitlines()
    
    total_num_sentences = len(test_sentences)

    for temp_sentence in test_sentences:
        total_words += len(temp_sentence.split())
        unknown_words += helper_for_unknown_words(temp_sentence, unigram_dict)
        total_log_prob += interpolate_log_prob_sentence(temp_sentence, lambda1, lambda2, lambda3)
    return 10**((-total_log_prob)/(total_words + total_num_sentences - unknown_words))

def interpolate_log_prob_sentence(sentence, lambda1, lambda2, lambda3, unigram_dict=unigram_dict, bigram_dict=bigram_dict, trigram_dict=trigram_dict):
    '''
        Task: calculate interpolate log prob for a sentence
    '''
    words_in_sentence = ['<s>'] + sentence.lower().split() + ['</s>']
    trigrams_list = trigrams_makeup(words_in_sentence)
    temp1_prob = 0
    temp2_prob = 0
    
    # at first need to find for first <s> and first word interpolate log prob i.e. log(lambda1*p(w1) + lambda2*p(w1|<s>) + lambda3*p(w1|<s>))
    if words_in_sentence[1] in unigram_dict:
        temp1_prob = lambda1*float(unigram_dict['<s>'])
        if words_in_sentence[1] in bigram_dict['<s>']:
            temp2_prob = (lambda2 + lambda3)*float(bigram_dict['<s>'][words_in_sentence[1]])
    # fixing log math domain error:
    if temp1_prob + temp2_prob > 0:
        temp_prob = log10(temp1_prob + temp2_prob)
    else:
        temp_prob = 0

    for i in trigrams_list:
        temp_lamdba1_prob = 0
        temp_lamdba2_prob = 0
        temp_lamdba3_prob = 0
        if i[2] in unigram_dict:
            temp_lamdba1_prob = float(unigram_dict[i[2]]) 
            if i[1] in unigram_dict and i[1] in bigram_dict and i[2] in bigram_dict[i[1]]:
                temp_lamdba2_prob = float(bigram_dict[i[1]][i[2]])
                if i[0] in unigram_dict and '{0} {1}'.format(i[0],i[1]) in trigram_dict and i[2] in trigram_dict['{0} {1}'.format(i[0],i[1])]:
                    temp_lamdba3_prob = float(trigram_dict['{0} {1}'.format(i[0],i[1])][i[2]])
        # fixing log math domain error with negative value:
        if temp_lamdba1_prob + temp_lamdba2_prob + temp_lamdba3_prob > 0:
            temp_prob += log10(temp_lamdba1_prob + temp_lamdba2_prob + temp_lamdba3_prob)
    return temp_prob
    
def helper_for_unknown_words(sentence, dct):
    '''
        Task: to calculate # of unknown words
    '''
    num = 0
    for i in sentence.lower().split():
        if i not in dct:
            num += 1
    return num

# write to output file according to Justin's format
with open(output_file, 'w') as out_file:
    out_file.write('Lambda1(Unigram Weight) Lambda2(Bigram Weight) Lambda3(Trigram Weight) Perplexity \n')
    write_format = '{0} {1} {2} {3} \n'.format(lambda1,lambda2,lambda3,calculate_perplexity(lambda1,lambda2,lambda3,test_file))
    out_file.write(write_format)
'''
if __name__ == '__main__':
    # print(trigrams_makeup(['a','b']))
    #sentence = 'There are not many people—and as it is desirable that a story-teller and a story-reader should establish a mutual understanding as soon as possible , I beg it to be noticed that I confine this observation neither to young people nor to little people , but extend it to all conditions of people : little and big , young and old : yet growing up , or already growing down again—there are not , I say , many people who would care to sleep in a church .'
    #sentence1 = 'But it applies to Night .'
    #print(interpolate_log_prob_sentence(sentence1.lower(), 0.1,0.1,0.8))
    #print(helper_for_unknown_words(sentence, unigram_dict))
    print(calculate_perplexity(0.6,0.3,0.1,test_file='dickens_test.txt'))
'''
    
