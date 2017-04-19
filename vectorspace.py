# Scot Freysinger
# scotfrey

import sys
import os
from preprocess import *
from operator import itemgetter
from math import log10

# idf = log10(N/df) where df is the # of documents that contain the word
# tf-idf weight is tf*idf

# relevant = score != 0
# recall = retrieved/(retrieved + relevant)
# precision = retrieved/(retrieved + not relevant)

# second weighting system is binary term independence

# inverted_index = {token1: {docid1: w1, docid2: w2, ...}, ...}
def indexDocument(tokenized_content, inverted_index, doc_id):
    token_freqs = {}
    max_freq = 0.
    for token in tokenized_content:
        if token_freqs.has_key(token):
            token_freqs[token] = token_freqs[token] + 1
        else:
            token_freqs[token] = 1
        if token_freqs[token] > max_freq:
            max_freq = token_freqs[token]
        # calculate tf weight
        for token in token_freqs.keys():
            token_freqs[token] = float(token_freqs[token])/float(max_freq)
            if inverted_index.has_key(token):
                inverted_index[token][doc_id] = token_freqs[token]
            else:
                inverted_index[token] = {doc_id: token_freqs[token]}
    return token_freqs

def retrieveDocuments(query, inverted_index, document_frequencies):
    # find all doc_ids to perform a similarity test on
    doc_ids = set()
    query_frequencies = {}
    max_freq = 0
    for token in query:
        if inverted_index.has_key(token):
            doc_ids.update(inverted_index[token].keys())
        if query_frequencies.has_key(token):
            query_frequencies[token] = query_frequencies[token] + 1
        else:
            query_frequencies[token] = 1
        if query_frequencies[token] > max_freq:
            max_freq = query_frequencies[token]

    token_weights = {}
    for token in query_frequencies.keys():
        # calculate tf score
        tf_weight = float(query_frequencies[token])/float(max_freq)

        #calculate idf
        N = 1400 #TODO edit this once we know
        if document_frequencies.has_key(token):
            idf_weight = log10(N/document_frequencies[token])
            token_weights[token] = tf_weight * idf_weight
        else:
            token_weights[token] = 0

    # calculate similarity between query and documnents
    similarity_scores = {} # key = doc_id, value = score
    for doc_id in doc_ids:
        score = 0.
        #calculate similarity scores
        for token in token_weights.keys():
            if inverted_index.has_key(token) and inverted_index[token].has_key(doc_id):
                score += token_weights[token] * inverted_index[token][doc_id]

        similarity_scores[doc_id] = score
    # print(str(sorted(similarity_scores.items(), key=itemgetter(1), reverse=True)))

    return similarity_scores


# assume that query is already preprocessed
def vsm(tokenized_subreddits):
    # build inverted_index
    index = {}
    token_freqs = {}
    N = 0
    for subreddit in tokenized_subreddits.keys():
        print(subreddit + ' ' + str(N))
        N += 1
        doc_token_freq = indexDocument(tokenized_subreddits[subreddit], index, subreddit)
        # find the number of documents a word appears in
        for token in doc_token_freq:
            if token_freqs.has_key(token):
                token_freqs[token] = token_freqs[token] + 1
            else:
                token_freqs[token] = 1

    # calc and store length of each document?
    #calc idf weights and multiply
    for token, frequency in token_freqs.items():
        idf_weight = log10(N/frequency)
        for doc_id in index[token].keys():
            index[token][doc_id] = index[token][doc_id] * idf_weight

    #similarity_scores = retrieveDocuments(query, index, token_freqs)
    return index, token_freqs
