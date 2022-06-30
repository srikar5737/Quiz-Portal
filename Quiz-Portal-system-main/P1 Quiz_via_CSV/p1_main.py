import os
import sqlite3
import hashlib
import pandas as pd
import multiprocessing
import threading
import time
import keyboard
from tkinter import *
def hash_password(password):
	encoded_password = hashlib.sha256(password.encode())
	hashed_password = encoded_password.hexdigest()
	return hashed_password

def countdown():
	global tim,l1,root
	while tim>0:
		time.sleep(1)
		l1.destroy()
		mins,secs=(tim//60,tim%60)
		st = str(mins)+':'+str(secs)
		l1 = Label(root,text=st)
		l1.place(x=40,y=0)
		root.update()
		tim-=1
	#print("Your time is up")
	root.destroy()
def unattempted():
	global user_choices
	unattempted_lst=[]
	for i in range(len(user_choices)):
		if int(user_choices[i])==-1:
			unattempted_lst.append(i+1)
	print("Unattempted questions list is")
	print(unattempted_lst)

def goto():
	global q_index
	#sys.stdin.flush()
	q_goto=int(input("Enter the question which you want to go\n"))
	q_index=q_goto-1

def finalSubmit():
	global p1,submit
	#sys.stdin.flush()
	k=input("Do you want to end the quiz\n")
	if k=='yes':
		submit=1
		return

def export_database():
	conn1 = sqlite3.connect('project1_quiz_cs384.db',isolation_level=None,detect_types=sqlite3.PARSE_COLNAMES)
	db_df = pd.read_sql_query("SELECT * FROM project1_marks",conn1)
	db_df.to_csv('./quiz_wise_responses/database.csv',index=False)
	df2 = pd.read_csv('./quiz_wise_responses/database.csv')
	for i in range(len(df2['roll'])):
		x=df2.loc[i]
		q_no=x['quiz_num'][1:]
		file = './quiz_wise_responses/'+'quiz'+q_no+'.csv'
		if os.path.exists(file)==False:
			df3 = pd.DataFrame([['Roll','total_marks']])
			df3.to_csv(file,mode='a+',index=False,header=False)
		df4 = pd.DataFrame([[x['roll'],x['total_marks']]])
		df4.to_csv(file,mode='a+',index=False,header=False)

def keyboard_shortcuts():
	shortcut1='ctrl+alt+u'
	keyboard.add_hotkey(shortcut1,unattempted)
	shortcut2='ctrl+alt+g'
	keyboard.add_hotkey(shortcut2,goto)
	shortcut3='ctrl+alt+f'
	keyboard.add_hotkey(shortcut3,finalSubmit)
	shortcut4 = 'ctrl+alt+e'
	keyboard.add_hotkey(shortcut4,export_database)

def register():
	conn = sqlite3.connect('project1_quiz_cs384.db')
	c = conn.cursor()
	name = input("Enter your name\n")
	roll = input("Enter your roll number\n")
	password = input("Enter your password\n")
	hashed_password = hash_password(password)
	whatsapp_number = input("Enter your whatsapp number\n")
	#print(name,roll,hashed_password,whatsapp_number)
	c.execute("INSERT INTO project1_registration VALUES (?,?,?,?)",(name,roll,hashed_password,whatsapp_number))
	conn.commit()
	print("Successfully registed!!")
	login()


def show_data():
	conn = sqlite3.connect('project1_quiz_cs384.db')
	c = conn.cursor()
	c.execute("SELECT * FROM project1_registration")
	lst = c.fetchall()
	for item in lst:
		print(item)

def get_time(df):
	lst=[]
	for x in df:
		lst.append(x)
	time=lst[len(lst)-1].split('=')
	s = ""
	for k in time[1]:
		if k.isdigit()==True:
			s+=k
		else:
			break
	ti = int(s)
	return ti

def fun_input():
	global user_response,user_choices
	global q_index,next_flag,submit
	print("Enter -1 if you don't want to attempt")
	user_response = input("Enter your option\n")
	if len(user_response)!=0 and user_response!='-1':
		user_choices[q_index]=user_response
		
	next_flag=input(("enter the question number which you want to go or press n to go to next question or type submit to submit the quiz\n"))
	if next_flag=='submit':
		submit=1
		return
	if next_flag.isdigit():
		q_index=int(next_flag)-1
	else:
		q_index+=1

def check():
	global username,quiz_num
	conn = sqlite3.connect('project1_quiz_cs384.db')
	c = conn.cursor()
	c.execute("SELECT * FROM project1_marks")
	lst = c.fetchall()
	flag=0
	for x in lst:
		if username in x and quiz_num in x:
			flag=1
			break
	if flag==1:
		return True
	return False


def enter_into_database():
	global username,quiz_num,score
	conn = sqlite3.connect('project1_quiz_cs384.db')
	c = conn.cursor()
	if check()==False:
		c.execute("INSERT INTO project1_marks VALUES (?,?,?)",(username,quiz_num,str(score)))
		conn.commit()
	else:
		c.execute("UPDATE project1_marks SET total_marks=(?) WHERE roll=(?) AND quiz_num=(?)",(str(score),username,quiz_num))
		conn.commit()
	print("The marks of the student have been entered into the database\n")

def quizwise_responses():
	global df,quiz_num,score,username,user_choices,correct_answers
	le = len(df['ques_no'])
	path = './quiz_wise_responses/'+quiz_num+'_'+username+'.csv'
	total_quiz_marks=0
	l=['ques_no','question','option1','option2','option3','option4','correct_option','marks_correct_ans','marks_wrong_ans','compulsory','marked_choice','Total','Legend']
	for i in range(le):		
		if os.path.exists(path)==False:
			df_temp = pd.DataFrame([l])
			df_temp.to_csv(path,mode='a+',index=False,header=False)
		v=df.loc[i]
		total_quiz_marks+=v['marks_correct_ans']
		m_c=user_choices[i]
		to=0
		if v['compulsory']=='y':
			to=1
		else:
			to=2
		if m_c==-1:
			m_c=0
		correct_str=""
		fl=0
		if int(user_choices[i])==int(correct_answers[i]) and int(user_choices[i])!=-1:
			correct_str="Correct Choices"
		elif (int(user_choices[i])!=int(correct_answers[i]) and int(user_choices[i])!=-1) or (int(user_choices[i])==-1 and v['compulsory']=='y') :	
			correct_str="Wrong Choices"
		elif int(user_choices[i])==-1:
			correct_str="Unattempted"
		df1 = pd.DataFrame([[v[l[0]],v[l[1]],v[l[2]],v[l[3]],v[l[4]],v[l[5]],v[l[6]],v[l[7]],v[l[8]],v[l[9]],m_c,to,correct_str]])
		df1.to_csv(path,mode='a+',index=False,header=False)
	lst1=['','','','','','','','','','','',score,'Marks Obtained']
	lst2=['','','','','','','','','','','',total_quiz_marks,'Total Quiz Marks']
	df2 = pd.DataFrame([lst1,lst2])
	df2.to_csv(path,mode='a+',index=False,header=False)

def quiz_questions():
	global q_index,df,root,over,next_flag
	global tim,p1,p2,score,submit,correct_answers
	correct_questions = 0
	wrong_questions = 0
	le = len(df['ques_no'])
	attempted=0
	correct_answers = []
	for i in range(le):
		v = df.loc[i]
		correct_answers.append(v['correct_option'])
	score=0
	global user_choices
	user_choices=[]
	user_choices=[-1 for i in range(le)]
	while tim>0 and q_index<le:
		row=df.loc[q_index]
		print('Question ',row['ques_no'],')',end=' ')
		print(row['question'],end='\n')
		print('Option 1) ',row['option1'],end='\n')
		print('Option 2) ',row['option2'],end='\n')
		print('Option 3) ',row['option3'],end='\n')
		print('Option 4) ',row['option4'],end='\n')
		global user_response
		submit=0
		fun_input()
		if submit==1:
			break
	
	print("quiz over",end='\n')
	try:
		p1.terminate()
	except:
		print("Process terminated\n")

	
	for i in range(le):
		temp=df.loc[i]
		if int(correct_answers[i])==int(user_choices[i]):
			score+=temp['marks_correct_ans']
			correct_questions+=1
		if int(user_choices[i])!=-1:
			attempted+=1
		if (int(correct_answers[i])!=int(user_choices[i]) and int(user_choices[i])!=-1) or (int(user_choices[i])==-1 and temp['compulsory']=='y'):
			wrong_questions+=1
			score+=temp['marks_wrong_ans']


	print("Total quiz questions :", le,end='\n')
	print("Total attempted questions :", attempted,end='\n')
	print("Total correct questions :",correct_questions,end='\n')
	print("Total wrong questions:",wrong_questions,end='\n')
	print("Total marks obtained:",score,end='\n')
	enter_into_database()
	quizwise_responses()

def test_interface():

	def get_quiz():
		global quiz_num
		global student_name
		global username
		print(f"the entered quiz is {quiz_num}",end='\n')
		quiz_file = './quiz_wise_questions/'+quiz_num+'.csv'
		global df
		df = pd.read_csv(quiz_file)
		global tim
		tim = get_time(df)*60
		print(f'the quiz time is {tim//60} min',end='\n')
		global root,l1 
		root=Tk()
		root.title("Test details and user details")
		root.geometry("400x300")
		Label(root,text='time').place(x=0,y=0)
		l1 = Label(root,text=str(tim))
		l1.place(x=130,y=0)
		l2 = Label(root,text=student_name)
		l2.place(x=0,y=25)
		l3 = Label(root,text=username)
		l3.place(x=0,y=50)
		global q_index
		q_index=0
		global p1,p2
		p1 = multiprocessing.Process(target=countdown)
		p2 = threading.Thread(target=quiz_questions)
		p1.start()
		p2.start()
		p1.join()
		p2.join()
		root.mainloop()
		#print(df.head())
	global quiz_num
	quizzes=os.listdir('./quiz_wise_questions')
	print("The available quizzes are\n")
	for q in quizzes:
		xl=q.split('.')
		num=xl[0][1:]
		fin='quiz '+num
		print(fin)

	quiz_num=input("Enter the quiz number that you want to attempt in the format q1,q2,...")
	get_quiz()

#connecting to our project database
#global conn, c


#now creating table inside our database
#creating project1_registration table 
if os.path.exists('project1_quiz_cs384.db')==False:
	conn = sqlite3.connect('project1_quiz_cs384.db')
	c = conn.cursor()
	c.execute("""CREATE TABLE project1_registration(

					name text,
					password text,
					roll text,
					whatsapp_number INTEGER
		)""")

	#creating project1_marks table
	c.execute("""CREATE TABLE project1_marks(

					roll text,
					quiz_num REAL,
					total_marks REAL
		)""")

# now creating the login portal
keyboard_shortcuts()
user_choice=input(("Do you want to register or login\n"))
user_choice=user_choice.lower()

def login():
	print("---------------------------Login Page------------------------\n")
	global username,c,conn
	conn = sqlite3.connect('project1_quiz_cs384.db')
	c = conn.cursor()
	global student_name
	username = input("Enter your username\n")
	password = input("Enter the password\n")
	hash_pass = hash_password(password)
	c.execute("SELECT * FROM project1_registration")
	lst = c.fetchall()
	flag=0
	#print(lst)
	for data in lst:
		if username in data and hash_pass in data:
			student_name=data[0]
			flag=1
			break
		if username in data and hash_pass not in data:
			print("Entered wrong password\n Try again")
			exit()
	if flag==0:
		print("You have not registered yet!!...redirecting you to registration page\n")
		register()
	else:
		print("You have logged in!!\n")
		test_interface()


if user_choice=='login':
	login()

else:
	#now register
	print("---------------------------Registration Page------------------------\n")
	register()
	print("you have registered now login\n")
	login()

show_data()
#os.remove('project1_quiz_cs384.db')
