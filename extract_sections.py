#!/usr/bin/python
import sys
import os
import json

section_names = {
                'professional experience':'experience',
                'work experience':'experience',
                'experience':'experience',
                'industry experience':'experience',
                'education':'education',
                'education background':'education',
                'skills':'skills',
                'technical skills':'skills',
                'achievements':'achievements',
                'academic achievements':'achievements',
                'projects':'projects',
                'major projects':'projects',
                'minor projects':'projects',
                'project and publications':'projects',
                'publications':'projects',
                'areas of interest':'interest',
                'skill set':'skills',
                'skills and interest':'skills',
                'academic projects':'projects',
                'computer skills':'skills',
                'personal information':'personal',
                'personal details':'personal'
                }

dump={}
field=""
data=""

path=sys.argv[1]

newdir=path+"/../infoboxes/"

d = os.path.dirname(newdir)

if not os.path.exists(d):
	os.makedirs(d)

jsonpath=path+"/../jsons/"	

j = os.path.dirname(jsonpath)

if not os.path.exists(j):
	os.makedirs(j)

# go till first section

for file in os.listdir(path):

	current=os.path.join(path,file)

	if os.path.isfile(current):
		f=open(current,'rb')

		w=open(d+"/"+str(file),'wb')
		
		first=1

		print 'Writing file: ' + newdir+"/"+str(file)

		for line in f:
		    section = line.lstrip().rstrip().lower().replace(":","").replace(".","") # remove delimeters

		    if section in section_names.keys():
	
			if first: first=0

			else: dump[field]=data; data="";

			w.write("========================================\n")
			w.write("Start of " + section_names[section]+"\n")
			field=section_names[section]

		    else:
			w.write(line[:-1]+"\n")
			data+=line[:-1]+"\n"

		dump[field]=data		## last section

		print 'Dumping json: ' + newdir+"/"+str(file)+".json\n\n"

		json.dump(dump,open(j+"/"+str(file)+".json",'wb'))

		f.close()
		w.close()
		dump.clear()



