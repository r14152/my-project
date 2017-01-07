with open('./14140-ui-jsdfa.tgz','rb') as fileData:
	ablob = fileData.read()
#design database
conn = sqlite3.connect('./python/temp.db')
conn.execute('''create table if not exists storeDb(finalData blob);''')
with open('./14140-ui-jsdfa.tgz','rb') as fileData:
	ablob = fileData.read()
	sql = '''insert  into storeDb values(?);'''
	conn.execute(sql,[sqlite3.Binary(ablob)])
	conn.commit()
#write in the database
 sql = "select finalData from storeDb;"
 cur.execute(sql)
 data = cur.fetchone()
 with open('temp.tar.gz','wb') as output_file:
	output_file.write(data[0])


