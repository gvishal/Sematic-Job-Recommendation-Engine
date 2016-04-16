import sys
import os
import json
import string
import datetime
import re
# from unidecode import unidecode

from summarizer import FrequencySummarizer


printable = set(string.printable)

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

stopwords = set()   
with open('stopwords.txt', 'r') as f:
  for line in f:
    line = line.strip()
    stopwords.add(line)


def get_summary(title, text):
    fs = FrequencySummarizer()
    # print '----------------------------------'
    # print title

    summary = []
    try:
        for s in fs.summarize(text, 2):
            summary.append(s)
    except:
        pass
        # print '*',s
    return summary

def write_to_file(json_file, data = {}):
    fp = open(json_file, 'r')

    json_content = json.load(fp)

    fp.close()

    for section in data:
        json_content[section] = data[section]
    # print json_content

    fp = open(json_file, 'w')
    json.dump(json_content, fp)
    fp.close()

def clean_summary(summary):
    # line = " ".join(s for s in summary)
    # line = " ".join([s for s in line.strip().splitlines(True) if s.strip("\r\n").strip()])
    # print line
    pass

def iterate_over_files():
    jsonpath = "./data/jsons/"

    for file_name in os.listdir(jsonpath):
        # print file_name
        json_file = os.path.join(jsonpath, file_name)

        print json_file
        # print time_file

        if not os.path.isfile(json_file):
            continue

        fp = open(json_file, 'r')
        json_content = json.load(fp)

        text = ''
        for section in json_content:
            if section in ['summary', 'cgpa', 'time']:
                continue
            # print json_content[section]
            text += str(json_content[section])

        # print text
        summary = get_summary(file_name, text)
        # print summary
        # clean_summary(summary)

        # break
        # continue

        data = {"summary": summary}

        write_to_file(json_file, data)

def main():
    iterate_over_files()

if __name__ == '__main__':
    main()