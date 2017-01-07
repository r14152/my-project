#s=['aaa.json.1','ddd.json.3','hasd.json.12','asjad.json.2']
#s=s.split(',')
#print s
import os
import sqlite3

conn = sqlite3.connect('test.db')
path=os.path.expanduser('~/sem6/se2/dataFile')
s=os.listdir(path)
a=[]
for i in s:
    i=i.split('.')
    i[len(i)-1]=int(i[len(i)-1])
    a.append(i)
   
sorted_list = sorted(a, key=lambda x:x[2])
#print a
#print sorted_list
a=[]
for i in sorted_list:
     i[len(i)-1]=str(i[len(i)-1])
for i in sorted_list:
    a.append('.'.join(i))
print a
for i in a:
	lst =[]
	priority =int(i.split('.')[-1])
	print priority
	finalPath = path+'/'+i
	fileName = i
	lst.append(priority)
	lst.append(fileName)
	lst.append(finalPath)
	print fileName
	conn.execute('insert into tempDb values(?,?,?);',lst)
	conn.commit()
	#k= os.stat(path+'/'+i).st_mtime
    #print k
conn.commit()
