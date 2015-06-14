#coding:utf-8

import sqlite3
import time

#获取数据库连接
def get_conn():
	conn = sqlite3.connect('../temp/litedb.db')
	return conn

def new_comment(essayTitle, username, email, parentID, replyto, content):
	conn = get_conn()
	cursor = conn.cursor()
	uptime = time.strftime('%Y-%m-%d-%X', time.localtime())
	try:
		#return "gg"
		sql = "insert into Comment(essayTitle, username, email, uptime, parentID, replyto, content)"\
		"values('%s','%s','%s','%s','%d','%s','%s')"%(essayTitle, username, email, uptime, parentID, replyto, content)
		cursor.execute(sql)
		conn.commit()
	except Exception as e:
		return sql
	finally:
		cursor.close()
		conn.close()

def getByTitle(essayTitle):
	conn = get_conn()
	cursor = conn.cursor()
	try:
		sql = "select * from Comment where essayTitle = '%s'"%essayTitle
		cursor.execute(sql)
		comments = cursor.fetchall()
		conn.commit()
	except Exception as e:
		return sql
	finally:
		cursor.close()
		conn.close()
	return comments

def CreateTableComment():
	conn = get_conn()
	cursor = conn.cursor()
	sql = '''create table IF NOT EXISTS Comment(
	commentID INTEGER PRIMARY KEY AUTOINCREMENT,
	essayTitle TEXT NOT NULL,
	username TEXT NOT NULL,
	email TEXT NOT NULL,
	uptime TEXT NOT NULL,
	parentID INT,
	replyto TEXT,
	content TEXT
	)'''
	try:
		cursor.execute(sql)
		conn.commit()
	except Exception as e:
		raise e
	finally:
		cursor.close()
		conn.close()

if __name__ == "__main__":
	CreateTableComment()