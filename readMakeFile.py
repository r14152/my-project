#!/usr/bin/python

def getAllList(line):
	lst=[]
	lst = line.split(' ')
	strng = lst[0].split(':')
	if '.o' not in strng:
		return lst[1:]
	return lst

fileName="Makefile2"
lstOfC =[]
lstOfO =[]
lstFinal=[]
gccLst=[]
tokenVarDependO=[]
flag=1
fp = open(fileName,"r")
for line in fp:
	if len(line)>0:
		if '.c' in line and ':' in line and '.o' in line:
			tokenVarDependO.append(line.split(':')[0])
			print line.split(':')
		if 'gcc' in line and '.c' not in line:
			gccLst =getAllList(line)
		if ':' in line and flag ==1:
			lstFinal = getAllList(line)
		if len(lstFinal)>0:
			flag=0	
		lst = line.split(' ')
		if lst[0] == '\tgcc' and '-c' in lst:
			for i in lst:
				if ".c" in i:
					lstOfC.append(i)
				if ".o" in i:
					lstOfO.append(i[:-1])
'''
#print "lstOfC :",lstOfC
#print "lstOfO :",lstOfO
#print "lstOfFinal :",lstFinal
if sorted(lstOfO) !=sorted(lstFinal):
	print "Invalid"
else:
	print "Valid"
print "gccLst :",gccLst 
print "tokenVar",tokenVar
'''
