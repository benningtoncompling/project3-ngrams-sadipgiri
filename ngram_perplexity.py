'''
    ngram_perplexity python3 program to calculate perplexity of the model comparing with the given test file.
    Author: Sadip Giri (sadipgiri@bennington.edu)
    Date: 9th April, 2019
'''

from unigrams import unigrams_counts_dictionary
from trigrams import trigrams_makeup

input_file='dickens_model.txt'

with open(input_file,'r') as in_file:
    sentences = in_file.read().splitlines()

unigram_index = sentences.index('\\1-grams:') 
bigram_index = sentences.index('\\2-grams:')
trigram_index = sentences.index('\\3-grams:')

def create_bigram_dict(sentences):
    '''
        Created bigram dict but log probs this time -> same as generate bigram apporach as shown earlier!
    '''
    bigram_dict = {}
    for i in sentences[bigram_index+1: trigram_index - 1]:
        temp_list = i.split()
        if temp_list[3] not in bigram_dict:
            bigram_dict[temp_list[3]] = {temp_list[4]: temp_list[2]}
        else:
            bigram_dict[temp_list[3]][temp_list[4]] = temp_list[2]
    return bigram_dict

def create_trigram_dict(sentences):
    '''
        Created trigram dict but log probs this time -> same as generate trigram apporach as shown earlier!
    '''
    trigram_dict = {}
    for i in sentences[trigram_index+1: len(sentences) - 2]:
        temp_list = i.split()
        if ' '.join(temp_list[3:5]) not in trigram_dict:
            trigram_dict[' '.join(temp_list[3:5])] = {temp_list[5]: temp_list[2]}
        else:
            trigram_dict[' '.join(temp_list[3:5])][temp_list[5]] = temp_list[2]
    return trigram_dict

def create_unigram_dict(sentences):
    '''
        Also, creating unigram dict with log probs reading the model file.
    '''
    unigram_dict = {}
    for i in sentences[unigram_index+1: bigram_index - 1]:
        temp_list = i.split()
        unigram_dict[temp_list[3]] = temp_list[2]
    return unigram_dict

def calculate_perplexity(lambda1, lambda2, lambda3, test_file='dickens_test.txt'):
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

    unigram_dict = create_unigram_dict(sentences)
    bigram_dict = create_bigram_dict(sentences)
    trigram_dict = create_trigram_dict(sentences)

    total_words = 0
    unknown_words = 0
    total_log_prob = 0
    
    with open(test_file, 'r') as test_file:
        test_sentences = test_file.read().splitlines()
    
    total_num_sentences = len(test_sentences)

    for temp_sentence in test_sentences:
        temp_sentence_list = temp_sentence.split() + ['</s>']
        total_words += len(temp_sentence_list)
        for word in temp_sentence_list:
            if word not in unigram_dict:
                unknown_words += 1
        temp_trigrams = trigrams_makeup(temp_sentence_list)
        total_log_prob += mult([interpolate_log_prob(i,lambda1,lambda2,lambda3, unigram_dict,bigram_dict,trigram_dict,len(unigram_dict)) for i in temp_trigrams])
    
    return 10**((-total_log_prob)/(total_words + total_num_sentences - unknown_words))

def interpolate_log_prob(trigram, lambda1, lambda2, lambda3, unigram_dict, bigram_dict, trigram_dict, total_num_words):
    '''
        Task: calculate interpolate log prob for one trigram!
        Approach:
            given: one trigram tuple
            interpolate_log_prob =  l1*P(Wn) + l2*P(Wn|Wn-1) + l3*P(Wn|Wn-2 Wn-1)
    '''
    tnminus2, tnminus1, tn = trigram
    if tn in unigram_dict:
        prob_1 = unigram_dict[tn]
    else:
        return 0
    if tnminus1 in bigram_dict:
        prob_2 = float(bigram_dict[tnminus1][tn])
    else:
        return 0
    if ' '.join([tnminus2, tnminus1]) in trigram_dict:
        prob_3 = float(trigram_dict[' '.join([tnminus2, tnminus1])][tn])
    else:
        return 0
    return lambda1*prob_1 + lambda2*prob_2 + lambda3*prob_3

def mult(lst):
    '''
        very simple helper function to multiply all probabilities in the list
    '''
    a = 1.0
    for i in lst:
        a *= float(i)
    return a

if __name__ == '__main__':
    print(calculate_perplexity(0.1,0.2,0.3))
    #print(interpolate_log_prob())
    #c=0
    #t = create_bigram_dict(sentences)
    #print(t.keys()[:5])
    #print(t.values()[:5])
    #print(t)
    