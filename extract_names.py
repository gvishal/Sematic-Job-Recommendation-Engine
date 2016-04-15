import os
import sys
from unidecode import unidecode
import string
printable = set(string.printable)
# from nltk.tag import StanfordNERTagger

# st=StanfordNERTagger("./classifiers/english.all.3class.distsim.crf.ser.gz", path_to_jar="./stanford-ner.jar")

from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost:9000')

path = sys.argv[1]

spath = path + '/../names/'

d = os.path.dirname(spath)

if not os.path.exists(d):
    os.makedirs(d)

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

for file in os.listdir(path):

    current=os.path.join(path,file)

    if os.path.isfile(current):
        data=open(current,'rb')

        w=open(d+"/"+str(file)+".name",'wb')

        print "\n\nProcessing file: " + file

        count=0
        flag=0

        for line in data:
            # print line
            if(line.isspace()): continue
            elif count==5 or flag: break
            else: count+=1

            line = line.lstrip().rstrip()
            # line = remove_non_ascii(line)
            # line = filter(lambda x: x in printable, line)

            output = nlp.annotate(line, properties={
              'annotators': 'tokenize,ssplit,pos,lemma,ner',
              'outputFormat': 'json'
              })

            # print 'output: ', output
            tagged = []
            for sentence in output['sentences']:
                for token in sentence['tokens']:
                    tagged.append((token['originalText'], token['ner']))

            # print tagged

            name = []
            for (el1,el2) in tagged:
                if el2 == u'PERSON':
                    print "Name identified: "+ el1
                    name.append(el1)
                    flag+=1

            full_name = ' '.join(n for n in name)
            print 'full_name: ', full_name
            w.write(full_name + '\n')
