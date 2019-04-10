# import nltk
from math import log10

# note this is counting bigrams for each sentence rather than whole thing
def bigrams_list(sentence_list):
    '''
        Task: to get list of all bigrams

        Approach:
            Same as unigrams_list but creating bigrams
    '''
    lst = []
    for i in sentence_list:
        # lst += list(nltk.bigrams(['<s>'] + i.lower().split() + ['</s>']))
        lst += bigrams_makeup(['<s>'] + i.lower().split() + ['</s>']) # using my own instead nltk's
    return lst

def bigrams_counts_dictionary(bigrams_tuples_list):
    '''
        takes in list of bigrams tuples
        creates dictionary with counts for bigrams
        e.g. [('the', 'cat'), ('cat', 'was'), ('was', 'the'), ('the', 'cute'), ('cute', '.')] ->
            -> {'the': {'cat': 1, 'cute': 1}, 'cat': {'was': 1}, 'was': {'the': 1}, 'cute': {'.': 1}}
    '''
    bigrams_counts = {}
    for i,j in bigrams_tuples_list:
        if i not in bigrams_counts:
            bigrams_counts[i] = {}
        if j not in bigrams_counts[i]:
            bigrams_counts[i][j] = 1
        else:
            bigrams_counts[i][j] += 1
    return bigrams_counts

def bigrams_write_format(bigrams):
    '''
        Task: create one sentence with \n to write in the output_file
        Approach:
            1. create bigrams_dict
            2. sort using list of tuples with bigrams and their counts
            3. loop through sorted tuples and count bigrams
            4. count occurence of the first word of bigram tuple using sum() function within bigram_dict[fir_wrd].values()
            5. finally, return final sentence adding \n at each end of sentence and joining everything using .join() function
    '''
    bigrams_dict = bigrams_counts_dictionary(bigrams)
    lst = []
    tuples_lst = []
    for i in set(bigrams):
        temp_tuple = (' '.join(i),bigrams_dict[i[0]][i[1]])
        tuples_lst.append(temp_tuple)
    tuples_lst.sort(key=lambda x: x[1],reverse=True) # using sort() function with lambda() to sort by second value of the tuple 

    for i in tuples_lst:
        temp_tuple = tuple(i[0].split())
        temp_count_of_first_word_of_tuple = sum(bigrams_dict[temp_tuple[0]].values())
        temp_bigram_prob = i[1]/temp_count_of_first_word_of_tuple
        temp_log10 = log10(temp_bigram_prob)
        lst.append('{0} {1} {2} {3}\n'.format(i[1],temp_bigram_prob,temp_log10,i[0]))
    return ''.join(lst)

def bigrams_makeup(words):
    '''
        Task: create list of bigrams tuples
        Approach:
            1. create a tuple of first and second word
            2. loop according and append to the list
            3. finally return the bigrams tuples
    '''
    new_lst = []
    for i in range(len(words)):
        new_lst.append(tuple(words[i:i+2]))
    return new_lst[:len(new_lst) - 1]

if __name__ == '__main__':
    lst = list(nltk.bigrams(['<s>', 'i', 'endeavoured', 'in', 'this', 'ghostly', 'little', 'book', ',', 'to', 'raise', 'the', 'ghost', 'of', 'an', 'idea', ',', 'which', 'shall', 'not', 'put', 'my', 'readers', 'out', 'of', 'humour', 'with', 'themselves', ',', 'with', 'each', 'other', ',', 'with', 'the', 'season', ',', 'or', 'with', 'me', '.', '</s>', '<s>', 'may', 'it', 'haunt', 'their', 'houses', 'pleasantly', ',', 'and', 'no', 'one', 'wish', 'to', 'lay', 'it', '.', '</s>', '<s>', 'their', 'faithful', 'friend', 'and', 'servant', ',', 'c.', 'd.', 'december', ',', '.', '</s>']))
    #print(lst)
    #st = bigrams_write_format(lst)
    #print(st)
    slt = bigrams_makeup(['<s>', 'i', 'endeavoured', 'in', 'this', 'ghostly', 'little', 'book', ',', 'to', 'raise', 'the', 'ghost', 'of', 'an', 'idea', ',', 'which', 'shall', 'not', 'put', 'my', 'readers', 'out', 'of', 'humour', 'with', 'themselves', ',', 'with', 'each', 'other', ',', 'with', 'the', 'season', ',', 'or', 'with', 'me', '.', '</s>', '<s>', 'may', 'it', 'haunt', 'their', 'houses', 'pleasantly', ',', 'and', 'no', 'one', 'wish', 'to', 'lay', 'it', '.', '</s>', '<s>', 'their', 'faithful', 'friend', 'and', 'servant', ',', 'c.', 'd.', 'december', ',', '.', '</s>'])
    print(lst == slt)
