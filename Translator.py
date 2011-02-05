# -*- coding: utf-8 -*
'''         Hare Krsna           '''
''' om namo Bhagavate Vasudevaya '''
#to find dictonary entries in the given ver
'''
   find the dictonary matches in the MW dictonary

   and NITAI VEDA and Glossary

'''
#function to sort the list according to the index

def add_index_tag(in_list,in_string):
    length = len(in_list)
    out_list = in_list
    for i in range(length):
        entry = out_list[i]
        index = str(in_string.index(entry[0:len(entry)-1]))
        out_list[i] = index.rjust(3,'0')+entry
    out_list.sort()
    return out_list
def refine_list(in_list):
    out_list = in_list
    i=0
    while 1:
        if i>=len(out_list):
            break
        if len(out_list[i])<7:
            out_list[i]=' '
        i+=1
    return out_list

#Input string
string_to_translate = raw_input(':>')
#string converted to words
string_to_translate=string_to_translate.replace('-',' ')
string_to_translate=string_to_translate.replace('|',' ')
words = string_to_translate.split()

#an output list with the string is initialized
listed=[]

#the monier williams sanskrit - english dictonary was loaded to list
FILE = open('_MW.txt', 'r')
lines = FILE.readlines()
FILE.close()

#each dictonary word is searched in the given string, is found, added to list
for line in lines:
    if len(line)>1:
        if string_to_translate.find(line[0:len(line)-1])>-1:
            listed.append(line)

#the given list is not regular but is with all the dictonary matches listed
listed = add_index_tag(listed, string_to_translate)
listed = refine_list(listed)
length = len(listed)
for i in range(length):
    entry = listed[i]
    listed[i] = entry[3:len(entry)]

# print the matches sorted
lines = []
for word in words:
    tmp_list = []
    out_format=''
    for one in listed:
        if word.find(one[0:len(one)-1])>-1 and len(one)>2:
            tmp_list.append(one[0:len(one)-1]+' ')
    for once in tmp_list:
        if len(word)==(len(once)-1):
            tmp_list = []
            tmp_list.append(once)
    line = word+'::\t'+out_format.join(tmp_list)
    print line
    lines.append(line)
#write lines to file
FILE = open('iText.txt','w')
FILE.writelines(string_to_translate)
FILE.writelines(lines)
FILE.close()
