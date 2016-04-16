#!/usr/bin/python
import sys
import os
import json
import string
from unidecode import unidecode

printable = set(string.printable)

section_names = {
                'professional experience':'experience',
                'work experience':'experience',
                'experience':'experience',
                'industry experience':'experience',
                'experience intern': 'experience',
                'education':'education',
                'education background':'education',
                'academics':'education',
                'academic record':'education',
                'academic details':'education',
                'skills':'skills',
                'technical skills':'skills',
                'technologies worked with':'skills',
                'achievements':'achievements',
                'academic achievements':'achievements',
                'scholastic achievements':'achievements',   
                'projects':'projects',
                'major projects':'projects',
                'minor projects':'projects',
                'other projects':'projects',
                'project and publications':'projects',
                'publications':'projects',
                'areas of interest':'interest',
                'skill set':'skills',
                'skills and interest':'skills',
                'academic projects':'projects',
                'computer skills':'skills',
                'personal information':'personal',
                'personal details':'personal',
                'relevant courses':'courses',
                'relevant course work':'courses',
                'relevant courses undertaken':'courses',
                'selected coursework':'courses',
                'research oriented work':'research',
                'publications':'research',
                'extra curricular':'interests',
                'extra-curricular':'interests',
                'interests':'interests',
                'other activities':'interests',
                'notable philanthropic projects':'interests',
                'other achievements':'interests',
                'miscellaneous':'interests',
                'technical and personal skills':'skills'
                }

dump={}
data=""

path = sys.argv[1]

newdir = path + "/../infoboxes/"

d = os.path.dirname(newdir)

if not os.path.exists(d):
    os.makedirs(d)

jsonpath=path+"/../jsons/"  

j = os.path.dirname(jsonpath)

if not os.path.exists(j):
    os.makedirs(j)

# go till first section

def replace_chars(line):
    replacements = {
        '\xe2\x80\x99': ' ',
        '\xe2\x80\x93': '-'
    }
    for rep in replacements:
        print rep
        line.replace(rep, replacements[rep])
    return line

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

def write_to_file(json_file, data = {}):
    fp = open(json_file, 'r')

    json_content = json.load(fp)

    fp.close()

    json_content.update(data)
    # print json_content

    fp = open(json_file, 'w')
    json.dump(json_content, fp)
    fp.close()

for file in os.listdir(path):

    current=os.path.join(path,file)
    # current = '/home/vg/work/IIITH/Sematic-Job-Recommendation-Engine/data/txts/201156221_RadhaManisha.pdf.html'
    current = '/home/vg/work/IIITH/Sematic-Job-Recommendation-Engine/data/txts/201405626_HaseebAhmed.pdf.html'
    if os.path.isfile(current):
        f=open(current,'rb')

        w=open(d+"/"+str(file),'wb')
        
        first=1
        field=""

        print 'Writing file: ' + newdir+str(file)

        for line in f:
            # print line
            line = remove_non_ascii(line)
            line = filter(lambda x: x in printable, line)
            line = line.strip()
            
            line = ' '.join([s for s in line.split(' ')])

            # line = "".join([s for s in line.strip().splitlines(True) if s.strip("\r\n").strip()])

            if not line or line.isspace():
                continue
                
            # print line

            section = line.lower().replace(":","").replace(".","") # remove delimeters


            if section in section_names.keys():
    
                if first: 
                    first=0
    #           elif section_names[section]==field: continue
                elif section in dump : 
                    continue
                else: 
                    dump[field]=data; data="";    

                w.write("========================================\n")
                w.write("Start of " + section_names[section]+"\n")
                field=section_names[section]

            else:
                w.write(line)
                data+=line

        if field not in dump:
            dump[field]=data        ## last section

        print 'Dumping json: ' + newdir+str(file)+".json\n\n"

        write_to_file(j+"/"+str(file)+".json", dump)
        # json.dump(dump, open(j+"/"+str(file)+".json",'wb'))

        f.close()
        w.close()
        dump.clear()
    # break