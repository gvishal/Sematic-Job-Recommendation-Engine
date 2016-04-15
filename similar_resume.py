"""Author: Harshendra"""

import nltk
import string
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.stem.porter import PorterStemmer

path = '/home/vg/work/IIITH/Sematic-Job-Recommendation-Engine/data/txts'
token_dict = {}
stemmer = PorterStemmer()

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item).lower())
    return stemmed

def tokenize(text):
    
    #tokens = nltk.word_tokenize(text)
    tokens = text.split(' ')
    #stems = stem_tokens(tokens, stemmer)
    return tokens

for subdir, dirs, files in os.walk(path):
    for file in files:
        file_path = subdir + os.path.sep + file
        shakes = open(file_path, 'r')
        text = shakes.read()
        lowers = text.lower()
        #no_punctuation = lowers.translate(None, string.punctuation)
        #print string.punctuation
        delimeters = ":,;()\"\'\$-%\.{|}"
        for ch in list(delimeters):
            if ch in lowers:
                lowers = lowers.replace(ch," ")
        
        #print lowers
        
        token_dict[file] = lowers
        
#this can take some time
tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
tfs = tfidf.fit_transform(token_dict.values())
print tfs.shape



while True:
    file_path = raw_input("file path> ")

    with open(file_path) as d:
        text = d.read()
        lowers = text.lower()
        #no_punctuation = lowers.translate(None, string.punctuation)
        #print string.punctuation
        delimeters = ":,;()\"\'\$-%\.{|}"
        for ch in list(delimeters):
            if ch in lowers:
                lowers = lowers.replace(ch," ")

        test = lowers

    response = tfidf.transform([test])

    cosine_similarities = linear_kernel(response, tfs).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-10:-1]
    print 'Similar resumes'
    for i in related_docs_indices:
        print '%-50s %.4f' % (token_dict.keys()[i].split('.')[0],cosine_similarities[i])

