"""Author: Harshendra"""

import nltk
import string
import os
import json
from pprint import pprint
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.stem.porter import PorterStemmer
import numpy as np

path = '/home/vg/work/IIITH/Sematic-Job-Recommendation-Engine/data/jsons'
token_dict = {}

skills_dict = {}
projects_dict = {}
cgpa_dict = {}
time_dict = {}

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
      
        with open(file_path) as d:
             data = json.load(d)

        #print file_path,data.keys()
        
    
        try:
            if type(data['cgpa']) == list:
                cgpa_dict[file] = 0
            else:
                cgpa_dict[file] = data['cgpa']
        except KeyError:
            cgpa_dict[file] = 0
 

        try:
            time_dict[file] = data['time']['aux'] + data['time']['direct']
        except KeyError:
            time_dict[file] = 0
        
        try:
            text = data['skills']
        except KeyError:
            text = ""
        
        
        lowers = text.lower()
        #no_punctuation = lowers.translate(None, string.punctuation)
        #print string.punctuation
        delimeters = ":,;()\"\'\$-%\.{|}"
        for ch in list(delimeters):
            if ch in lowers:
                lowers = lowers.replace(ch," ")
        
        #print lowers
        
        skills_dict[file] = lowers
        
   
        try:
            text = data['projects']

        except KeyError:
            text = ""

       
        lowers = text.lower()
        #no_punctuation = lowers.translate(None, string.punctuation)
        #print string.punctuation
        delimeters = ":,;()\"\'\$-%\.{|}"
        for ch in list(delimeters):
            if ch in lowers:
                lowers = lowers.replace(ch," ")
        
       
        
        projects_dict[file] = lowers
        
        
#this can take some time
tfidf_skills = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
tfs_skills = tfidf_skills.fit_transform(skills_dict.values())

tfidf_projects = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
tfs_projects = tfidf_projects.fit_transform(projects_dict.values())

print cgpa_dict

while True:

    #test = "jdbc acm icpc machine learning"
    test = raw_input("Query> ")

    response = tfidf_skills.transform([test])

    print 'Resumes matching skills'
    cosine_similarities = linear_kernel(response, tfs_skills).flatten()
    cosine_similarities = np.array([i*80+cg*0.1+du*0.1 for i,cg,du in \
            zip(cosine_similarities,cgpa_dict.values(),time_dict.values())])

    related_docs_indices = cosine_similarities.argsort()[:-10:-1]
    for i in related_docs_indices:
        if cosine_similarities[i] > 0:
            print "%-50s %.4f" % (skills_dict.keys()[i].split('.')[0],cosine_similarities[i])

    response = tfidf_projects.transform([test])
            
    print 'Resumes matching projects'
    cosine_similarities = linear_kernel(response, tfs_projects).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-10:-1]
    for i in related_docs_indices:
        if cosine_similarities[i] > 0:
            print "%-50s %.4f" % (skills_dict.keys()[i].split('.')[0],cosine_similarities[i])

