# import nltk
from math import log10
from bigrams import bigrams_counts_dictionary, bigrams_list

def trigrams_list(sentence_list):
    '''
        Task: to get list of all trigrams

        Approach:
            Same as unigrams_list but creating trigrams
    '''
    lst = []
    for i in sentence_list:
        # lst += list(nltk.trigrams(['<s>'] + i.lower().split() + ['</s>']))
        lst += trigrams_makeup(['<s>'] + i.lower().split() + ['</s>']) # not using nltk
    return lst

def trigrams_count_dictionary(trigrams_tuples_list):
    '''
        Task: create trigrams dictionary with their couts

        Approach:
            same as unigrams_dict_counting
            Could use .count() but it takes forever!
    '''
    trigrams_counts = {}
    for i in trigrams_tuples_list:
        if i not in trigrams_counts:
            trigrams_counts[i] = 1
        else:
            trigrams_counts[i] += 1
    return trigrams_counts
        

def trigrams_write_format(trigrams, bigrams):
    '''
        Task: 
            final sentence with \n to write once as whole in output_file using .join()
                since: writing one by one would take forever!
        
        Approach:
            same as bigrams writing approach with some changes such as:
                1. P(tn|tn-2 tn-1) = C(tn-2 tn-1 tn)/C(tn-2 tn-1) i.e. trigrams_count/bigrams_count
                2. sorting using tuples of trigrams and their counts just like in bigrams
    '''
    trigrams_dict = trigrams_count_dictionary(trigrams)
    bigrams_dict = bigrams_counts_dictionary(bigrams)
    lst = []
    tuples_lst = []
    for i in set(trigrams):
        temp_tuple = (' '.join(i),trigrams_dict[i])
        tuples_lst.append(temp_tuple)
    tuples_lst.sort(key=lambda x: x[1],reverse=True) # using sort() function with lambda() to sort by second value of the tuple i.e. x[1] 

    for i in tuples_lst:
        temp_tuple = tuple(i[0].split())
        temp_trigram_prob = i[1]/bigrams_dict[temp_tuple[0]][temp_tuple[1]]
        temp_log10 = log10(temp_trigram_prob)
        lst.append('{0} {1} {2} {3}\n'.format(i[1],temp_trigram_prob,temp_log10,i[0]))
    return ''.join(lst)

# creating own nltk.trigrams() function.
def trigrams_makeup(words):
    '''
        To return list of trigrams tuples when list of tokens given
    '''
    lst = []
    for i in range(len(words)):
        lst.append(tuple(words[i:i+3]))
    return lst[:len(lst) - 2]

if __name__ == '__main__':
    # tri_lst = list(nltk.trigrams(['<s>', 'i', 'endeavoured', 'in', 'this', 'ghostly', 'little', 'book', ',', 'to', 'raise', 'the', 'ghost', 'of', 'an', 'idea', ',', 'which', 'shall', 'not', 'put', 'my', 'readers', 'out', 'of', 'humour', 'with', 'themselves', ',', 'with', 'each', 'other', ',', 'with', 'the', 'season', ',', 'or', 'with', 'me', '.', '</s>', '<s>', 'may', 'it', 'haunt', 'their', 'houses', 'pleasantly', ',', 'and', 'no', 'one', 'wish', 'to', 'lay', 'it', '.', '</s>', '<s>', 'their', 'faithful', 'friend', 'and', 'servant', ',', 'c.', 'd.', 'december', ',', '.', '</s>']))
    # #print(lst)
    # bi_lst = list(nltk.bigrams(['<s>', 'i', 'endeavoured', 'in', 'this', 'ghostly', 'little', 'book', ',', 'to', 'raise', 'the', 'ghost', 'of', 'an', 'idea', ',', 'which', 'shall', 'not', 'put', 'my', 'readers', 'out', 'of', 'humour', 'with', 'themselves', ',', 'with', 'each', 'other', ',', 'with', 'the', 'season', ',', 'or', 'with', 'me', '.', '</s>', '<s>', 'may', 'it', 'haunt', 'their', 'houses', 'pleasantly', ',', 'and', 'no', 'one', 'wish', 'to', 'lay', 'it', '.', '</s>', '<s>', 'their', 'faithful', 'friend', 'and', 'servant', ',', 'c.', 'd.', 'december', ',', '.', '</s>']))
    # # st = trigrams_write_format(tri_lst,bi_lst)
    tri_lst = list(trigrams_makeup(['s','a','d','i','p','s','a','d']))
    # bi_lst = list(nltk.bigrams(['s','a','d','i','p','s','a','d']))
    # # st = trigrams_write_format(tri_lst,bi_lst)
    t = trigrams_count_dictionary(tri_lst)
    print(t)
    # print(trigrams_write_format(tri_lst,bi_lst))
    #print(trigrams_makeup(['s','a','d','i','p','s','a','d']))
