import os
import time
import subprocess
import sqlite3

path = '.'
lastTime=0
while 1:
	lst = os.listdir(path)
	for curFile in lst:
		#print curFile
		curTime = os.stat(curFile).st_mtime
		if lastTime<curTime:
			print curFile
			lastTime = curTime
	time.sleep(5)
