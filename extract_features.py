"""Features"""

import sys
import os
import json
import string

stopwords = set()   
with open('stopwords.txt', 'r') as f:
  for line in f:
    line = line.strip()
    stopwords.add(line)

from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost:9000')
printable = set(string.printable)

WINDOW_SIZE = 20

def get_time(text, section):
    output = nlp.annotate(text, properties={
      'annotators': 'tokenize,ssplit,pos,lemma,ner',
      'outputFormat': 'json'
      })

    get_time_context(output, section)
    return
    # print output
    # time_tokens = []
    # for s in output['sentences']:
    #     for token in s['tokens']:
    #         if token['ner'] in ['DATE', 'TIME', 'DURATION', 'SET']:
    #             time_tokens.append(token)

    # print time_tokens

def get_time_context(output, section):
    """Extract all sentences which have any time context"""
    time_contexts = []

    json.dump(output, open("./data/sample_ner/test_nlp_" + section + ".json", 'w'))

    # if section not in ['experience']:
    #     return

    for s in output['sentences']:
        time_token_present = False
        ignore = False
        time_value = []
        content = []
        aux_content = []

        for token in s['tokens']:
            if token['ner'] in ['DATE', 'TIME', 'DURATION', 'SET']:
                # print token
                time_token_present = True
                if 'normalizedNER' in token:
                    time_value.append(token['normalizedNER'])
                time_value.append(token['word'])
            if token['word'] in ['monsoon']:
                time_token_present = True
                time_value.append('monsoon')

        # If sentence has time token then weigh it.
        for token in s['tokens']:
            word = token['word'].lower()
            if word in stopwords:
                continue
            content.append(word)
            if word.find('@') != -1 or word.find('http') != -1:
                ignore = True

        if time_token_present:
            time_contexts.append({'time_value': time_value,
                                    'content': content, 'aux_content': []})
        elif not ignore:
            n = len(time_contexts)
            if n:
                time_contexts[n-1]['aux_content'].append(content)

    print time_contexts


def get_time_groups(time_tokens):
    time_groups = []

    time_group = []
    prev_time = -1
    for time_token in time_tokens:
        pass

def main():
    jsonpath = "./data/jsons/"  

    for json_file in os.listdir(jsonpath):
        current = os.path.join(jsonpath, json_file)
        current = '/home/vg/work/IIITH/Sematic-Job-Recommendation-Engine/data/jsons/201203005_BhavanaGannu.pdf.html.json'
        print current

        if not os.path.isfile(current):
            continue

        fp = open(current, 'rb')

        json_content = json.load(fp)

        if 'sections' in json_content.keys():
            for section in json_content['sections']:
                if section not in ['experience']:
                    continue
                get_time(json_content['sections'][section])

        for section in json_content:
            print section
            if section not in ['experience']:
                continue
            s = json_content[section]
            s = filter(lambda x: x in printable, s)
            get_time(s, section)

        break


if __name__ == '__main__':
    main()