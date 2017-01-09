import zlib
import gzip
import os
import hashlib
import sqlite3,tarfile
#create one database which store the md5sum code
#and the file name for storing that thing

#file which return the md5sum value of the given file
def hashKeyGen(fileName,blocksize):
	hasher = hashlib.md5()
	path =(os.getcwd()+'/'+fileName)
	print path	
	data =gzip.open(path,"rb")
	buf = data.read(blocksize)
	while(len(buf)>0):
		hasher.update(buf)
		buf = data.read(blocksize)
	data.close()
	#tarfile.close()
	return hasher.hexdigest()
	
#this function is going to return the key and create the 
#tar.gz
def compressFile(data,fileName):
	lst=[]
	compressData = zlib.compress(data)
	f_out = gzip.open(fileName+'.gz',"wb")
	f_out.write(compressData)
	fileName +='.gz'
	lst.append(hashKeyGen(fileName,65556))
	lst.append(fileName)
	return lst

#read the database and concat all string

def fileCompres(keyStamp):
	conn = sqlite3.connect('tempDb.db')
	cur = conn.cursor()
	#temporary table later taken from configuration file with try and catch
	cur.execute("select fileName from aaa order by priority;")
	result = cur.fetchall()
	#result=cur.execute("select * from details,aaa where 
						#details.fileName=aaa.fileName and aaa.timeDetails>keyStamp")	
	#cur.execute("drop table")
	print result
	for i in result:
		fileName1 = str(i[0])
		cur.execute("select * from details where details.fileName='"+fileName1+"';");
		res = cur.fetchall()
		#conn.close()
		data=""
		for row in res:
			for uniqueData in row:
				if type(uniqueData) != int:
					data +=uniqueData+" "
				else:
					data +=str(uniqueData)
			data +=' $ '
		tempFile =fileName1
		uniQueCode = compressFile(data,tempFile)
		key = uniQueCode[0]
		fileName = uniQueCode[1]
		conn.execute('''create table if not exists storeDb(key str,finalData blob);''')
		if os.path.exists(os.getcwd()+'/'+fileName):
				print "come"
				with open(os.getcwd()+'/'+fileName,'rb') as fileData:
					ablob = fileData.read()
					sql = '''insert into storeDb values(?,?);'''
					cur.execute(sql,[key,sqlite3.Binary(ablob)])
					conn.commit()
				#dbNew.close()
				fileData.close()
		#conn.close()
fileCompres(14152)
