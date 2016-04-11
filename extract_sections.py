#!/usr/bin/python
import sys

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

f = open(sys.argv[1],'r')


# go till first section

print 'Beginning'
for line in f:
    section = line.lstrip().rstrip().lower().replace(":","").replace(".","") # remove delimeters
    #section = section.split('.:(')[0].rstrip()
    #section = section.replace(".","")

    if section in section_names.keys():
        print '========================================'
        print 'Start of',section_names[section]
    else:
        print line[:-1]
