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

def get_results(query):

    test = query
    response = tfidf.transform([test])

    print response

    RESULTS_ARRAY = []

    cosine_similarities = linear_kernel(response, tfs).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-10:-1]
    for i in related_docs_indices:
            if cosine_similarities[i] > 0:
                RESULTS_ARRAY.append({"candidate": token_dict.keys()[i].split('.')[0],
                                        "cosine": cosine_similarities[i]})
                # print "%-50s %.4f" % (token_dict.keys()[i].split('.')[0],cosine_similarities[i])

    return RESULTS_ARRAY

def main():
    while True:

        test = raw_input("Query> ")
        response = tfidf.transform([test])

        print response
        cosine_similarities = linear_kernel(response, tfs).flatten()
        related_docs_indices = cosine_similarities.argsort()[:-10:-1]
        for i in related_docs_indices:
                if cosine_similarities[i] > 0:
                    print "%-50s %.4f" % (token_dict.keys()[i].split('.')[0],cosine_similarities[i])

if __name__ == '__main__':
    main()