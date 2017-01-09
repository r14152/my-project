import sys,sqlite3
import os,re
import json

with open('configuration.json') as fp1:
    data1 = json.load(fp1)
sleepTime=data1['sleepTime']
path=data1['path']
database=data1['database']
#print sleepTime,path,database

path=os.path.expanduser(path)
s=os.listdir(path)
'''
a=[]
for i in s:
    i=i.split('.')
    i[len(i)-1]=int(i[len(i)-1])
    a.append(i)
   
sorted_list = sorted(a, key=lambda x:x[2])
'''
#print a
#print sorted_list
a=[]
'''
for i in sorted_list:
     i[len(i)-1]=str(i[len(i)-1])
for i in sorted_list:
    a.append('.'.join(i))
print a
for i in a:
    #print path+'/'+i
    k= os.stat(path+'/'+i).st_mtime
    print k
'''


with open('demo2.json') as fp:
    data = json.load(fp)

dbName=database+'.db'
#print dbName
#sqlite3 demo2.db
conn = sqlite3.connect(dbName)
print "Opened database successfully";
cur=conn.cursor()
#conn.execute('''drop table details;''')
conn.execute(
'''CREATE TABLE details
       (firstName nvarchar(30) NOT NULL,
        middleName nvarchar(30),
        lastName nvarchar(30) NOT NULL,
        age nvarchar(3),
        streetAddress nvarchar(30) NOT NULL,
        state nvarchar(30) NOT NULL,
        city nvarchar(30) NOT NULL,
        postalCode nvarchar(6) NOT NULL, 
        type1 nvarchar(30),
        phNo1 nvarchar(15),
        type2 nvarchar(30),
        phNo2 nvarchar(15),
        type3 nvarchar(30),
        phNo3 nvarchar(15)
        );'''
)


print "Table created successfully";

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
     #(data['persons'][i]['age'])
     #q.append(data['persons'][i]['age'])
     for j in range(0,len(data['persons'][i]['phoneNumbers'])):
         q.append(data['persons'][i]['phoneNumbers'][j]['type'])
         q.append(data['persons'][i]['phoneNumbers'][j]['number'])
   
     q.append(data['persons'][i]['address']['streetAddress'])
     q.append(data['persons'][i]['address']['city'])
     q.append(data['persons'][i]['address']['state'])
     q.append(data['persons'][i]['address']['postalCode'])    
     cur.execute("insert into details values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",q);
print "data insert sucessfully"
#cur.execute("INSERT INTO details values('Sachin','Ishwar','Sendulkar','22','A304, Golden apartments','nupe','hm','411008')");
conn.commit()
cur.execute("select * from details");
result=cur.fetchall()
print result
conn.close()


conn = sqlite3.connect('tempDb_json.db')
print "Opened database successfully";
cur=conn.cursor()
#conn.execute('''drop table validInfo;''')
conn.execute(
'''CREATE TABLE validInfo
       (firstName nvarchar(30) NOT NULL,
        middleName nvarchar(30),
        lastName nvarchar(30) NOT NULL,
        age int(3),
        type1 nvarchar(30),
        phNo1 nvarchar(15),
        type2 nvarchar(30),
        phNo2 nvarchar(15),
        type3 nvarchar(30),
        phNo3 nvarchar(15),
        postalCode nvarchar(6) NOT NULL, 
        streetAddress nvarchar(30) NOT NULL,
        city nvarchar(30) NOT NULL,
        state nvarchar(30) NOT NULL
        );'''
)

for i in result:
    q=[]
    flag=0
    index=[0,2]
    for j in range(0,len(index)):
        chk=i[index[j]]
        if not re.match("[A-Za-z]*$",chk):
            print "Invalid lastName "+chk
            flag=1
            break
        else:
            q.insert(index[j],chk)
    if flag==1:
       continue
  
    index=[1,4,6,8]
    for j in range(0,len(index)):
        chk=i[index[j]]
        if chk!='':
            if not re.match("[A-Za-z]*$",chk):
                      print "Invalid  "+chk
                      flag=1
                      break
            else:
                      q.insert(index[j],chk)
        
        else:
            q.insert(index[j],'')
            
    if flag==1:
       continue

    chk=i[3]
    #print chk,index[j]
    if chk!='':
          if not re.match("[0-9]{2,3}$",chk):
                 print "Invalid  "+chk
                 #flag=1
                 continue
          else:
                 q.insert(3,int(chk))
        
    else:
          q.insert(3,'')
    
    index=[5,7,9]
    for j in range(0,len(index)):
        chk=i[index[j]]
        if chk!='':
             if re.match("[0-9]{3}[-]+[0-9-]{8}$",chk) or re.match("[0-9]{10}$",chk):
                      q.insert(index[j],chk)                
             else:
                      print "Invalid  "+chk
                      flag=1
                      break
                      
        
        else:
            q.insert(index[j],'')
            
    if flag==1:
       continue
    q.insert(10,i[10])
    index=[11,12]
    for j in range(0,len(index)):
        chk=i[index[j]]
        if not re.match("[A-Za-z]*$",chk):
            print "Invalid lastName "+chk
            flag=1
            break
        else:
            q.insert(index[j],chk)
    if flag==1:
       continue
    chk=i[13]
    if re.match("[0-9]{6}$",chk):
             q.insert(13,chk) 
    else:
            print "Invalid streetAddress "+chk
            continue 
        
            
    
    #print q    
    cur.execute("insert into validInfo values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",q);


print "Table created successfully";
conn.commit()
cur.execute("select * from validInfo");
result=cur.fetchall()
print result
conn.close()
