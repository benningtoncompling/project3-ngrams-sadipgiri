from math import log10

def unigrams_counts_dictionary(unigrams):
    '''
        Task: count unique unigrams
        Approach:
            1. loop through all unigrams
                a. if that unigram is not in dict: add it
                b. else: give its value 1
            2. return the dict
    '''
    dct = {}
    for i in unigrams:
        if i in dct:
            dct[i] += 1
        else:
            dct[i] = 1
    return dct

def unigrams_list(sentence_list):
    '''
        Task: to get list of all unigrams (or words/tokens) from the given text

        Approach:
            take in list of sentences
            create temporary list for each sentence:
                1. first get the list of that sentence using .split()
                2. add <s> at the beginning and </s> at the end
            finally, return list of words
    '''
    lst = []
    for i in sentence_list:
        temp_lst = ['<s>'] + i.lower().split() + ['</s>']
        lst += temp_lst
    return lst

def unigrams_write_format(unigrams):
    '''
        Task: create one whole sentence with \n to write in the output file
        Approach:
            1. get unigrams dictionary with their counts
            2. using helper_sort_dictionary() from first project to sort the dict into sorted tuples
            3. find probability of that unigram = count(unigram)/total_unigrams
            4. log10(above_prob)
            5. using .join() to return final sentence with \n at the end of all the sentences
    '''
    unigrams_dict = unigrams_counts_dictionary(unigrams)
    lst = []
    total_unigrams = len(unigrams)
    for i in helper_sort_dictionary(unigrams_dict):
        temp_unigram_prob = i[1]/total_unigrams
        temp_log10 = log10(temp_unigram_prob)
        lst.append('{0} {1} {2} {3}\n'.format(i[1],temp_unigram_prob,temp_log10,i[0]))
    return ''.join(lst)

def helper_sort_dictionary(dct):
    '''
        using list comprehension to loop through each item of dictionary and 
        return sorted list of tuples
    '''
    return [(i, dct[i]) for i in sorted(dct, key=dct.get, reverse=True)]

if __name__ == '__main__':
    print(unigrams_write_format(unigrams_counts_dictionary(['<s>', 'i', 'endeavoured', 'in', 'this', 'ghostly', 'little', 'book', ',', 'to', 'raise', 'the', 'ghost', 'of', 'an', 'idea', ',', 'which', 'shall', 'not', 'put', 'my', 'readers', 'out', 'of', 'humour', 'with', 'themselves', ',', 'with', 'each', 'other', ',', 'with', 'the', 'season', ',', 'or', 'with', 'me', '.', '</s>', '<s>', 'may', 'it', 'haunt', 'their', 'houses', 'pleasantly', ',', 'and', 'no', 'one', 'wish', 'to', 'lay', 'it', '.', '</s>', '<s>', 'their', 'faithful', 'friend', 'and', 'servant', ',', 'c.', 'd.', 'december', ',', '.', '</s>'])))
    