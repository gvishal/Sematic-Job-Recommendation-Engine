import nltk
import string
import os
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.stem.porter import PorterStemmer

path = '/home/vg/work/IIITH/Sematic-Job-Recommendation-Engine/data/txts'
json_path = '/home/vg/work/IIITH/Sematic-Job-Recommendation-Engine/data/jsons/'
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

summary_dict = {}

def read_data_from_json(fields = ['cgpa', 'summary']):

    for file_name in os.listdir(json_path):
        json_file = os.path.join(json_path, file_name)
        print json_file

        if not os.path.isfile(json_file):
            continue

        fp = open(json_file, 'r')
        json_content = json.load(fp)

        data = {}
        for field in fields:
            if field in json_content:
                data[field] = json_content[field]

        summary_dict[file_name] = data

read_data_from_json()
# print summary_dict

def get_results(query):

    test = query
    response = tfidf.transform([test])

    print 'response: ', response

    RESULTS_ARRAY = []

    cosine_similarities = linear_kernel(response, tfs).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-10:-1]
    for i in related_docs_indices:
        if cosine_similarities[i] > 0:
            file_name = token_dict.keys()[i].split('.')[0] + '.pdf.html.json'
            data = {}
            data = summary_dict[file_name]
            data.update({"candidate": token_dict.keys()[i].split('.')[0],
                            "cosine": cosine_similarities[i]})
            # data = {"candidate": token_dict.keys()[i].split('.')[0],
            #                 "cosine": cosine_similarities[i]}

            RESULTS_ARRAY.append(data)
            # print "%-50s %.4f" % (token_dict.keys()[i].split('.')[0],cosine_similarities[i])

    # print RESULTS_ARRAY
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
                # print token_dict.keys()[i]
                print "%-50s %.4f" % (token_dict.keys()[i].split('.')[0],cosine_similarities[i])

if __name__ == '__main__':
    main()