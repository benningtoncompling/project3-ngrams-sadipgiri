#!/usr/bin/env python3

'''
    Unigram:
        Generate a random number from 0.0 to 1.0, and begin to count up the
        probabilities for the unigrams. When you reach the unigram whose probability sends
        the probability total above the random number, add that unigram to the sentence.
        Repeat.
        Sentences should begin with <s> and end with </s>, and not have any <s>s or
        </s>s between the start and end.
'''

'''
    Credit: 
        Sophia suggested me to create bigram and trigram dictionaries to tackle the problem
        which makes sense and is also faster!
'''

import sys
import random

args_list = sys.argv
input_file = args_list[1]
output_file = args_list[2]

def unigenerate_gram(detail_sentences):
    '''
        Task: randomly return unigram when cumulative frequency is bigger than randomly generated number.

        Approach:
            1. set the counter
            2. randomly generate the number between 0 and 1
            3. go through unigram sentences from model file
            4. return the probability from that sentence.
    '''
    counter = 0
    random_num = random.random()
    for i in detail_sentences:
        temp_prob = float(i.split()[1])
        counter += temp_prob
        if counter > random_num:
            return i.split()[3]
    return

# with open('dickens_model.txt', 'r') as in_file:
#     sentences = in_file.read().splitlines()

with open(input_file, 'r') as in_file:
    sentences = in_file.read().splitlines()


# to read the uni, bi and tri grams model and referencing using indexes using .index() python helper function.
unigram_index = sentences.index('\\1-grams:') 
bigram_index = sentences.index('\\2-grams:')
trigram_index = sentences.index('\\3-grams:')

def num_unigrams_sentences(num):
    '''
        Task: generate sentence using unigram probability list

        Approach:  
            Use helper function unigenerate_gram() to generate one unigram each time until the end of sentence </s> is seen.
            plus start of sentence <s> is added.
    '''
    lst = []
    for i in range(num):
        temp_sentence = '<s>'
        temp_generated_word = unigenerate_gram(sentences[unigram_index+1: bigram_index - 1])
        while '</s>' not in temp_generated_word:
            if temp_generated_word is not '<s>':
                temp_sentence = temp_sentence + ' ' + temp_generated_word
                temp_generated_word = unigenerate_gram(sentences[unigram_index+1: bigram_index - 1])
        temp_sentence += ' </s>'
        lst.append(temp_sentence + '\n')
    return ''.join(lst)

def create_bigram_dict():
    '''
        Task: create bigram dictionary using the model file
        Approach:
            1. read all the sentences from the file
            2. find the index of bigram list \2_gram using .index() function
            3. finally, return the bigram dict defined earlier.
    '''
    bigram_dict = {}
    for i in sentences[bigram_index+1: trigram_index - 1]:
        temp_list = i.split()
        if temp_list[3] not in bigram_dict:
            bigram_dict[temp_list[3]] = {temp_list[4]: temp_list[1]}
        else:
            bigram_dict[temp_list[3]][temp_list[4]] = temp_list[1]
    return bigram_dict

def create_trigram_dict():
    '''
        Task: create trigram dictionary
        Approach: same as bigram dict approach
    '''
    trigram_dict = {}
    for i in sentences[trigram_index+1: len(sentences) - 2]:
        temp_list = i.split()
        if ' '.join(temp_list[3:5]) not in trigram_dict:
            trigram_dict[' '.join(temp_list[3:5])] = {temp_list[5]: temp_list[1]}
        else:
            trigram_dict[' '.join(temp_list[3:5])][temp_list[5]] = temp_list[1]
    return trigram_dict

# memoization
bigram_dict = create_bigram_dict()
trigram_dict = create_trigram_dict()

def num_bigrams_sentences(bigram_dict, num=5):
    '''
        Task: Generate given sentences using bigram model
        Approach: 
            1. create temp sentence list and also generate random number
            2. set the counter then loop through all second words starting with <s>
            3. do same think 
    '''
    lst = []
    for i in range(num):
        temp_lst = ['<s>'] # for starting with <s>
        while '</s>' not in temp_lst:
            random_num = random.random()
            counter = 0
            previous_word = temp_lst[-1] # at first, previous word will be <s>
            for j in bigram_dict[previous_word].keys():
                temp_prob = float(bigram_dict[previous_word][j])
                counter += temp_prob
                if counter > random_num:
                    temp_lst.append(j)
                    break
        lst.append(' '.join(temp_lst) + '\n')
    return ''.join(lst)

def helper_start_trigram(bigram_dict):
    '''
        Task: initialize the list starting with <s> -> same as bigram starting but for trigram!
        Apporach: Same as bigram approach!
    '''
    temp_lst = ['<s>'] # for each sentence starting with <s>
    random_num = random.random()
    counter = 0
    temp_second_words_list = bigram_dict['<s>'].keys()
    for j in temp_second_words_list:
        temp_prob = float(bigram_dict['<s>'][j])
        counter += temp_prob
        if counter > random_num:
            temp_lst.append(j)
            break
    return temp_lst

def num_trigrams_sentences(trigram_dict, bigram_dict, num=5):
    '''
        Task: To generate sentences using trigram model
        Approach: Same as bigram sentences technique!
    '''
    lst = []
    for i in range(num):
        temp_lst = helper_start_trigram(bigram_dict)
        while '</s>' not in temp_lst:
            random_num = random.random()
            counter = 0
            previous_bigram = '{0} {1}'.format(temp_lst[-2],temp_lst[-1])
            for j in trigram_dict[previous_bigram]:
                temp_prob = float(trigram_dict[previous_bigram][j])
                counter += temp_prob
                if counter > random_num:
                    temp_lst.append(j)
                    break
        lst.append(' '.join(temp_lst) + '\n')
    return ''.join(lst)

with open(output_file, 'w') as out_file:
    out_file.write('Generated Unigram, Bigram and Trigram Sentences \n')
    out_file.write('\n')

    out_file.write('Unigram Generated Sentences \n')
    out_file.write(num_unigrams_sentences(num=5))
    out_file.write('\n')

    out_file.write('Bigram Generated Sentences \n')
    out_file.write(num_bigrams_sentences(bigram_dict=bigram_dict, num=5))
    out_file.write('\n')

    out_file.write('Trigram Generated Sentences \n')
    out_file.write(num_trigrams_sentences(trigram_dict=trigram_dict,bigram_dict=bigram_dict,num=5))

'''
# Testing Purposes:

print('-----5 Unigram Sentences Generated-----')
print(num_unigrams_sentences(5))
print('')
print('-----5 Bigram Sentences Generated-----')
print(' '.join(num_bigrams_sentences(bigram_dict)))
print('')
print('-----5 Trigram Sentences Generated-----')
print(' '.join(num_trigrams_sentences(trigram_dict,bigram_dict)))
print('')
'''

