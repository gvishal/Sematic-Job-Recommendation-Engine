#!/usr/bin/python
import sys
import os
import json
import string
import re

EMAIL_REGEX = '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}'
PHONE_REGEX = '(([(]?\+[0-9]{1,3}[)]?[- ]?)?[0-9]{10})'
 
def get_match(regex, text):
    # print 'text', text
    return re.compile(regex).findall(text)

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

def get_details():
    jsonpath = "./data/jsons/"
    infobox = "./data/infoboxes/"
    txtpath = "./data/txts/"

    for file_name in os.listdir(jsonpath):
        # print file_name
        json_file = os.path.join(jsonpath, file_name)
        txt_file = os.path.join(txtpath, file_name[:file_name.find('.json')])

        print json_file
        # print time_file

        if not os.path.isfile(json_file):
            continue
        if not os.path.isfile(txt_file):
            continue

        fp = open(txt_file, 'r')
        
        text = ''
        for line in fp:
            text += line

        email = get_match(EMAIL_REGEX, text)
        phone = get_match(PHONE_REGEX, text)

        if email:
            email = email[0]
        if phone:
            phone = phone[0][0]
        print email, phone


        data = {"phone": phone, "email": email}

        write_to_file(json_file, data)

def generate_infobox():
    jsonpath = "./data/jsons/"
    infobox = "./data/infoboxes/"
    txtpath = "./data/txts/"

    get_details()
    # return

    for file_name in os.listdir(jsonpath):
        # print file_name
        json_file = os.path.join(jsonpath, file_name)
        info_file = os.path.join(infobox, file_name[:file_name.find('.json')])

        print info_file
        print json_file

        # if not os.path.isfile(json_file):
        #     continue
        # if not os.path.isfile(info_file):
        #     continue

        fp = open(json_file, 'r')
        json_content = json.load(fp)

        fp.close()
        fp = open(info_file, 'w')

        print json_content

        for section in json_content:
            if section in ['summary', 'phone', 'email', 'name', 'cgpa']:
                fp.write('\n-----------------------------\n')
                fp.write(section.upper())
                fp.write('\n')
                if section == 'cgpa' and json_content[section] < 5:
                    fp.write(str(7.2))
                else:
                    fp.write(str(json_content[section]))

        fp.close()
        
def main():
    generate_infobox()

if __name__ == '__main__':
    main()