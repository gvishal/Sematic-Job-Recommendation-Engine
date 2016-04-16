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

fs = FrequencySummarizer()

def get_summary(title, text):
    print '----------------------------------'
    print title

    summary = []
    for s in fs.summarize(text, 2):
        summary.append(s)
        # print '*',s
    return summary

def write_to_file(json_file, data = {}):
    fp = open(json_file, 'r')

    json_content = json.load(fp)

    fp.close()

    json_content.update(data)
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
        # json_file = '/home/vg/work/IIITH/Sematic-Job-Recommendation-Engine/data/jsons/201203005_BhavanaGannu.pdf.html.json'
        # json_file = '/home/vg/work/IIITH/Sematic-Job-Recommendation-Engine/data/jsons/201201043_RaviTejaGovinduluri.pdf.html.json'
        print json_file
        # print time_file

        if not os.path.isfile(json_file):
            continue

        fp = open(json_file, 'r')
        json_content = json.load(fp)

        text = ''
        for section in json_content:
            # print json_content[section]
            text += str(json_content[section])

        summary = get_summary(file_name, text)
        # clean_summary(summary)

        # break
        # continue

        data = {"summary": summary}

        write_to_file(json_file, data)

def main():
    iterate_over_files()

if __name__ == '__main__':
    main()