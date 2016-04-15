import sys
import os
import json
import string
import datetime
import re
from unidecode import unidecode
# from decimal import Decimal

printable = set(string.printable)

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

stopwords = set()   
with open('stopwords.txt', 'r') as f:
  for line in f:
    line = line.strip()
    stopwords.add(line)

def write_to_file(json_file, data = {}):
    fp = open(json_file, 'r')

    json_content = json.load(fp)

    fp.close()

    json_content.update(data)
    # print json_content

    fp = open(json_file, 'w')
    json.dump(json_content, fp)
    fp.close()

def iterate_over_files():
    jsonpath = "./data/jsons/"
    timepath = "./data/time/"
    namepath = "./data/names/"

    for file_name in os.listdir(jsonpath):
        # print file_name
        json_file = os.path.join(jsonpath, file_name)
        time_file = os.path.join(timepath, file_name)
        name_file = os.path.join(namepath, file_name)
        # json_file = '/home/vg/work/IIITH/Sematic-Job-Recommendation-Engine/data/jsons/201203005_BhavanaGannu.pdf.html.json'
        # json_file = '/home/vg/work/IIITH/Sematic-Job-Recommendation-Engine/data/jsons/201201043_RaviTejaGovinduluri.pdf.html.json'
        print json_file
        # print time_file

        if not os.path.isfile(json_file):
            continue

        if not os.path.isfile(time_file):
            continue

        # print 'here'
        direct_months, aux_months = read_time_context(time_file)
        cgpa = get_cgpa(json_file)
        if len(cgpa):
            cgpa = cgpa[0]
        else:
            cgpa = 0

        print direct_months, aux_months, cgpa

        name = ''
        name_file = name_file[:name_file.find('html.json')] + 'txt.name'
        if not os.path.isfile(name_file):
            name_file = name_file[:name_file.find('txt.name')] + 'html.name'
            if not os.path.isfile(name_file):
                continue

        name_fp = open(name_file, 'r')
        for line in name_fp:
            line = line.strip()
            name = remove_non_ascii(line)
            name = filter(lambda x: x in printable, name)
            name = name.strip()
        if len(name) > 50:
            name = name[:50]
        print name
        # continue

        data = {"time": {"direct": direct_months, "aux": aux_months},
                "cgpa": cgpa, "name": name}

        write_to_file(json_file, data)

def main():
	pass

if __name__ == '__main__':
	main()