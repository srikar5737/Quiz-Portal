import keyboard
import time
import sys
import sqlite3
import pandas as pd
import os
def export_database():
	conn1 = sqlite3.connect('project1_quiz_cs384.db',isolation_level=None,detect_types=sqlite3.PARSE_COLNAMES)
	db_df = pd.read_sql_query("SELECT * FROM project1_marks",conn1)
	db_df.to_csv('database.csv',index=False)
	df2 = pd.read_csv('database.csv')
	for i in range(len(df2['roll'])):
		x=df2.loc[i]
		q_no=x['quiz_num'][1:]
		file = 'quiz'+q_no+'.csv'
		if os.path.exists(file)==False:
			df3 = pd.DataFrame([['Roll','total_marks']])
			df3.to_csv(file,mode='a+',index=False,header=False)
		df4 = pd.DataFrame([[x['roll'],x['total_marks']]])
		df4.to_csv(file,mode='a+',index=False,header=False)

conn = sqlite3.connect('project1_quiz_cs384.db')
c = conn.cursor()
c.execute("SELECT * FROM project1_marks")
lst = c.fetchall()
for x in lst:
	print(x)
