import sys,sqlite3
import os,re
import json
dbName='tempDb.db'
conn = sqlite3.connect(dbName)
print "Opened database successfully";
cur=conn.cursor()
#resl=cur.execute("select * from aaa,details order by priorityand aaa.fileName=details.fileName");
#print resl
cur.execute("select firstName,middleName,lastName,age,type1,phNo1,type2,phNo2,type3,phNo3,streetAddress,city,state,postalCode from details,aaa where aaa.fileName=details.fileName  order by priority;")
result=cur.fetchall()
print result
conn.close()


conn = sqlite3.connect('tempDb_json.db')
print "Opened database successfully";
cur=conn.cursor()
conn.execute('''drop table validInfo;''')
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
        streetAddress nvarchar(30) NOT NULL,
        city nvarchar(30) NOT NULL,
        state nvarchar(30) NOT NULL,
        postalCode nvarchar(6) NOT NULL
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
            print "Invalid postal code "+chk
            continue 
        
            
    
    #print q    
    cur.execute("insert into validInfo values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",q);


print "Table created successfully";
conn.commit()
cur.execute("select * from validInfo");
result=cur.fetchall()
print result
conn.close()
