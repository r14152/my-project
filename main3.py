import sys,sqlite3
import os,re
import json,time

dbName='tempDb.db'
conn = sqlite3.connect(dbName)
cur=conn.cursor()

conn.execute(
        '''create table if not exists aaa(priority int,timeDetails double,fileName nvarchar(20) primary key); '''
)
conn.execute(
'''
CREATE TABLE if not exists details
(firstName nvarchar(30) NOT NULL,
middleName nvarchar(30),
lastName nvarchar(30) NOT NULL,
age nvarchar(3),
type1 nvarchar(30),
phNo1 nvarchar(15),
type2 nvarchar(30),
phNo2 nvarchar(15),
type3 nvarchar(30),
phNo3 nvarchar(15),
streetAddress nvarchar(30) NOT NULL,
city nvarchar(30) NOT NULL,
state nvarchar(30) NOT NULL,
postalCode nvarchar(6) NOT NULL,
fileName nvarchar(20),
FOREIGN KEY (fileName) REFERENCES aaa(fileName)
);

''')

print "Table created successfully";

def function1(lst,priorityValue):
        
        #dbName='tempDb.db'
        fName=lst[1]
        k= lst[3]
        print k
        with open(lst[2]) as fp:
                data = json.load(fp)
        #print data

        #print dbName
        #sqlite3 demo2.db
        #conn = sqlite3.connect(dbName)
        #print "Opened database successfully";
        #cur=conn.cursor()
        
        q=[lst[0],k,fName]
        #q.append(fName)
        print q
        cur.execute("insert into aaa values(?,?,?);",q)
        for i in range(0,len(data['persons'])):
                q=[]
                q.append(data['persons'][i]['firstName'])
                if data['persons'][i].has_key('middleName') :
                        q.append(data['persons'][i]['middleName'])
                else:
                        q.append('')
     
                q.append(data['persons'][i]['lastName'])
     
                if data['persons'][i].has_key('age'):
                        q.append(data['persons'][i]['age'])
                else:
                        q.append('')
                if not  data['persons'][i].has_key('phoneNumbers'):
                        q.append('','','','','','')
                else:
                        for j in range(0,len(data['persons'][i]['phoneNumbers'])):
                                q.append(data['persons'][i]['phoneNumbers'][j]['type'])
                                q.append(data['persons'][i]['phoneNumbers'][j]['number'])
   
                q.append(data['persons'][i]['address']['streetAddress'])
                q.append(data['persons'][i]['address']['city'])
                q.append(data['persons'][i]['address']['state'])
                q.append(data['persons'][i]['address']['postalCode'])
                q.append(fName)
                print q
                cur.execute("insert into details values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",q);
        print "data insert sucessfully"
        q=[fName]
        result=cur.execute("select * from details,aaa where details.fileName=aaa.fileName and aaa.timeDetails>="+str(priorityValue)+";")
        result=cur.fetchall()
        #print result




conn.execute('''drop table priorityTable;''')
conn.execute('''CREATE TABLE priorityTable(priority int not null,name nvarchar(20) not null,path nvarchar(50) not null, timeStamp double);''')
priorityValue =0  
while 1: 
	path=os.path.expanduser('~/sem6/se2/python/shruti')
	s=os.listdir(path)
	a=[]
        print s
	maxValue=0
	for i in s:
                if not os.path.exists(path+'/'+i):
                        continue
		k = os.stat(path+'/'+i).st_mtime
                print k,i
		if k>priorityValue:
                        #print "come"
			i=i.split('.')
			ch=(i[len(i)-1])
                        if re.match("([0-9]*$)",ch):
				i[len(i)-1]=int(i[len(i)-1])
				a.append(i)
				#print "ravi"
			if k>maxValue:
				maxValue = k
			#print "ravi",i,maxValue,priorityValue

	#print "resume ",priorityValue
	sorted_list = a
        print a
	#sorted_list = sorted(a, key=lambda x:x[2])
	#print a
	#print sorted_list
	a=[]
	for i in sorted_list:
		i[len(i)-1]=str(i[len(i)-1])
	#for i in sorted_list:
		a.append('.'.join(i))
	print a
	for i in a:
		lst =[]
		priority =int(i.split('.')[-1])
		#print priority
		finalPath = path+'/'+i
		fileName = i
		k= os.stat(path+'/'+i).st_mtime
		lst.append(priority)
		lst.append(fileName)
		lst.append(finalPath)
		lst.append(k)
		conn.execute('insert into priorityTable values(?,?,?,?);',lst)
                function1(lst,priorityValue)
	conn.commit()
        if maxValue>priorityValue:
		priorityValue = maxValue
        print priorityValue
        
	time.sleep(5)
        #conn.execute('''delete from aaa;''')
        #conn.execute('''delete from details;''')
		#print fileName
    #print k
#conn.commit()

