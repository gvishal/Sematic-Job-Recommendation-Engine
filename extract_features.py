"""Features"""

import sys
import os
import json
import string
import datetime
import re

stopwords = set()   
with open('stopwords.txt', 'r') as f:
  for line in f:
    line = line.strip()
    stopwords.add(line)

from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost:9000')
printable = set(string.printable)

WINDOW_SIZE = 20

# def get_time(text, section):
#     output = nlp.annotate(text, properties={
#       'annotators': 'tokenize,ssplit,pos,lemma,ner',
#       'outputFormat': 'json'
#       })

#     get_time_context(output, section)
#     return
    # print output
    # time_tokens = []
    # for s in output['sentences']:
    #     for token in s['tokens']:
    #         if token['ner'] in ['DATE', 'TIME', 'DURATION', 'SET']:
    #             time_tokens.append(token)

    # print time_tokens

def get_time_context(text, section):
    """Extract all sentences which have any time context"""
    output = nlp.annotate(text, properties={
      'annotators': 'tokenize,ssplit,pos,lemma,ner',
      'outputFormat': 'json'
      })
    time_contexts = []

    json.dump(output, open("./data/sample_ner/test_nlp_" + section + ".json", 'w'))

    # if section not in ['experience']:
    #     return

    for s in output['sentences']:
        time_token_present = False
        ignore = False
        time_value = set()
        content = []
        aux_content = []

        for token in s['tokens']:
            if token['ner'] in ['DATE', 'TIME', 'DURATION', 'SET']:
                # print token
                time_token_present = True
                if 'normalizedNER' in token:
                    time_value.add(token['normalizedNER'])
                time_value.add(token['word'].lower())

            if token['word'] in ['monsoon']:
                time_token_present = True
                time_value.add('monsoon')

        # If sentence has time token then weigh it.
        for token in s['tokens']:
            word = token['word'].lower()
            if word in stopwords:
                continue
            content.append(word)
            if word.find('@') != -1 or word.find('http') != -1:
                ignore = True

        if time_token_present:
            time_contexts.append({'time_value': list(time_value),
                                    'content': content, 'aux_content': []})
        elif not ignore:
            n = len(time_contexts)
            if n:
                time_contexts[n-1]['aux_content'].append(content)

    return time_contexts

def year_month_range(start_date, end_date):
    '''
    start_date: datetime.date(2015, 9, 1) or datetime.datetime
    end_date: datetime.date(2016, 3, 1) or datetime.datetime
    return: datetime.date list of 201509, 201510, 201511, 201512, 201601, 201602
    '''
    start, end = start_date.strftime('%Y%m'), end_date.strftime('%Y%m')
    assert len(start) == 6 and len(end) == 6
    start, end = int(start), int(end)

    year_month_list = []
    while start < end:
        year, month = divmod(start, 100)
        if month == 13:
            start += 88  # 201513 + 88 = 201601
            continue
        year_month_list.append(datetime.date(year, month, 1))

        start += 1
    return year_month_list

def month_str_to_num(string):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
         'may':5,
         'jun':6,
         'jul':7,
         'aug':8,
         'sep':9,
         'oct':10,
         'nov':11,
         'dec':12
        }
    s = string.strip()[:3].lower()

    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')

DATE_REGEXES = [
'^(1[0-2]|0[1-9]|\d)(\/|-)(20\d{2}|19\d{2}|0(?!0)\d|[1-9]\d)$',#month-year
'^(20\d{2}|19\d{2}|0(?!0)\d|[1-9]\d)(\/|-)(1[0-2]|0[1-9]|\d)$',#year-month
'^(XX\d{2})(\/|-)(1[0-2]|0[1-9]|\d)$' #XXYR-month
]

YEAR_REGEX = '^(20\d{2}|19\d{2}|0(?!0)\d|[1-9]\d)(\/|-)(20\d{2}|19\d{2}|0(?!0)\d|[1-9]\d)$' #year-year

MONTH_REGEX = '(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|(nov|dec)(?:ember)?)'

def get_match(regex, text):
    # print 'text', text
    return re.compile(regex).findall(text)

def process_time_contexts(time_contexts):
    """Process all extracted time contexts
    Assign one unit for each month
    """
    total_time = 0

    times = []
    for time_context in time_contexts:
        time_values = time_context['time_value']
        start_month = ''
        end_month = ''
        start_date = ''
        end_date = ''

        # print time_values
        years_present = False
        for time_value in time_values:
            for regex in DATE_REGEXES:
                date = get_match(regex, str(time_value))
                if len(date):
                    years_present = True
                    break

        for time_value in time_values:
            if 'summer' in time_value:
                start_month = 'may'
                end_month = 'july'
                start_date = datetime.date(2015, 05, 1)
                end_date = datetime.date(2015, 8, 1)
                break

            # 2 years
            if 'P2Y' in time_value:
                start_date = datetime.date(2015, 05, 1)
                end_date = datetime.date(2017, 05, 1)
                break                

            # print time_value
            date = ''
            year = ''
            month = ''
            for i, regex in enumerate(DATE_REGEXES):
                date = get_match(regex, str(time_value))
                if len(date):
                    if i == 0:
                        year = date[0][2]
                        month = date[0][0]
                    elif i == 1:
                        year = date[0][0]
                        month = date[0][2]
                    elif i == 2:
                        year = '20' + date[0][0][2:]
                        month = date[0][2]
                    break

            if date:
                # print date, int(month)
                if not start_date:
                    start_date = datetime.date(int(year), int(month), 1)
                elif not end_date:
                    end_date = datetime.date(int(year), int(month), 1)
                    break
            
            if not years_present:
                month = get_match(MONTH_REGEX, time_value.lower())
                if len(month):
                    month = month[0][0]
                    # print 'month: ', month
                    if not start_month:
                        start_month = month
                        start_date = datetime.date(2015, month_str_to_num(month), 1)
                    elif not end_month:
                        end_month = month
                        end_date = datetime.date(2015, month_str_to_num(month), 1)
                        break

                year = get_match(YEAR_REGEX, time_value)
                if len(year):
                    start_date = datetime.date(2015, 01, 1)
                    end_date = datetime.date(2016, 01, 1)
                    break

        total_months = []
        # print 'sd: ', start_date, 'ed: ', end_date
        if start_date and end_date:
            if start_date > end_date:
                start_date, end_date = end_date, start_date
            total_months =  year_month_range(start_date, end_date)
        # print total_months
        total_months = len(total_months)
        # print 'months: ', total_months
        total_time += total_months

    aux_time = 0
    if len(time_contexts) and not total_time:
        aux_time = len(time_contexts)*3
        # print 0

    print 'total_time: ', total_time, aux_time
    return total_time, aux_time


def get_time_groups(time_tokens):
    time_groups = []

    time_group = []
    prev_time = -1
    for time_token in time_tokens:
        pass

def write_time_contexts():
    jsonpath = "./data/jsons/"  

    for json_file in os.listdir(jsonpath):
        current = os.path.join(jsonpath, json_file)
        # current = '/home/vg/work/IIITH/Sematic-Job-Recommendation-Engine/data/jsons/201203005_BhavanaGannu.pdf.html.json'
        # current = '/home/vg/work/IIITH/Sematic-Job-Recommendation-Engine/data/jsons/201156221_RadhaManisha.pdf.html.json'
        print current

        if not os.path.isfile(current):
            continue

        fp = open(current, 'rb')

        json_content = json.load(fp)
        time_contexts = []

        if 'sections' in json_content.keys():
            for section in json_content['sections']:
                if section not in ['experience']:
                    continue
                time_contexts = get_time_context(json_content['sections'][section])

        for section in json_content:
            # print section
            if section not in ['experience']:
                continue
            s = json_content[section]
            s = filter(lambda x: x in printable, s)
            time_contexts = get_time_context(s, section)

        # print time_contexts
        json.dump(time_contexts, open("./data/time/" + json_file, 'w'))

def write_time_context(json_file):
    jsonpath = "./data/jsons/"  

    current = os.path.join(jsonpath, json_file)

    if not os.path.isfile(current):
        return

    fp = open(current, 'rb')

    json_content = json.load(fp)
    time_contexts = []

    if 'sections' in json_content.keys():
        for section in json_content['sections']:
            if section not in ['experience']:
                continue
            time_contexts = get_time_context(json_content['sections'][section])

    for section in json_content:
        # print section
        if section not in ['experience']:
            continue
        s = json_content[section]
        s = filter(lambda x: x in printable, s)
        time_contexts = get_time_context(s, section)

    # print time_contexts
    json.dump(time_contexts, open("./data/time/" + json_file, 'w'))

def read_time_contexts():
    jsonpath = "./data/time/"  

    for json_file in os.listdir(jsonpath):
        current = os.path.join(jsonpath, json_file)
        # current = '/home/vg/work/IIITH/Sematic-Job-Recommendation-Engine/data/jsons/201203005_BhavanaGannu.pdf.html.json'
        # current = '/home/vg/work/IIITH/Sematic-Job-Recommendation-Engine/data/jsons/201201043_RaviTejaGovinduluri.pdf.html.json'
        print current

        if not os.path.isfile(current):
            continue

        fp = open(current, 'r')

        json_content = json.load(fp)
        time_contexts = json_content

        # print time_contexts
        # print 'time_contexts: ', len(time_contexts)
        process_time_contexts(time_contexts)
        # json.dump(time_contexts, open("./data/time/" + json_file, 'w'))
        # break

def read_time_context(json_file):
    jsonpath = "./data/time/"  

    current = os.path.join(jsonpath, json_file)
    print current

    if not os.path.isfile(current):
        return

    fp = open(current, 'r')

    json_content = json.load(fp)
    time_contexts = json_content

    # print time_contexts
    # print 'time_contexts: ', len(time_contexts)
    process_time_contexts(time_contexts)
    # json.dump(time_contexts, open("./data/time/" + json_file, 'w'))
    # break 

CGPA_REGEXS = [
'(\d(?:\.\d+)?|10|10.0|10.00)(?:\/(?:10(?:\.\d+)?))',
'(\d(?:\.\d+)?|10|10.0|10.00)'
]

def get_cgpa_occ(s):
    regex1 = []
    regex2 = []

    regex1 = get_match(CGPA_REGEXS[0], s)
    if not len(regex1):
        new_s = s.lower().find('cgpa')
        if new_s == -1:
            new_s = s.lower().find('gpa')

        if new_s == -1:
            return ''

        s_new = s[new_s:new_s + 20]

        regex2 = get_match(CGPA_REGEXS[1], s_new)

        if not regex2:
            s_new = s[new_s:new_s + 80]

            regex2 = get_match(CGPA_REGEXS[1], s_new)

    cgpas = regex1 + regex2
    print regex1, regex2
    return cgpas

def get_cgpa(file_path):
    if not os.path.isfile(file_path):
        return

    fp = open(file_path, 'r')

    json_content = json.load(fp)

    cgpas = []
    if 'sections' in json_content.keys():
        for section in json_content['sections']:
            if section not in ['education']:
                continue
            s = json_content['sections'][section]
            cgpas = get_cgpa_occ(s)

    for section in json_content:
        # print section
        if section not in ['education']:
            continue
        s = json_content[section]
        s = filter(lambda x: x in printable, s)

        cgpas = get_cgpa_occ(s)

    print cgpas
    new_cgpas = []
    for cgpa in cgpas:
        # print cgpa
        if len(cgpa):
            new_cgpas.append(float(cgpa[0]))

    print new_cgpas
    return new_cgpas

def iterate_over_files():
    jsonpath = "./data/jsons/"  

    for json_file in os.listdir(jsonpath):
        current = os.path.join(jsonpath, json_file)
        # current = '/home/vg/work/IIITH/Sematic-Job-Recommendation-Engine/data/jsons/201203005_BhavanaGannu.pdf.html.json'
        # current = '/home/vg/work/IIITH/Sematic-Job-Recommendation-Engine/data/jsons/201201043_RaviTejaGovinduluri.pdf.html.json'
        print current

        # if not os.path.isfile(current):
        #     continue

        # fp = open(current, 'r')

        get_cgpa(current)

def main():
    # write_time_contexts()
    # read_time_contexts()

    base = '/home/vg/work/IIITH/Sematic-Job-Recommendation-Engine/data/jsons/'
    end = '201405626_HaseebAhmed.pdf.html.json'
    current = base + end

    current = '/home/vg/work/IIITH/Sematic-Job-Recommendation-Engine/data/jsons/201002140_ChanakyaAalla.pdf.html.json'

    get_cgpa(current)
    iterate_over_files()
    # write_time_context(end)
    # read_time_context(end)

if __name__ == '__main__':
    main()