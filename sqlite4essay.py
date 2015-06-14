#coding:utf-8

import sqlite3

#获取数据库连接
def get_conn():
  conn = sqlite3.connect('../temp/litedb.db')
  return conn



def InsertEssay(title, date, body, pwd, tag=""):
	conn = get_conn()
	cursor = conn.cursor()
	sql = "insert into Essay(title,uptime,pwd,body,tag) values"\
							" ('%s','%s','%s','%s','%s')"%(
								title, date, pwd, body,tag)
	try:
		cursor.execute(sql)
		conn.commit()
	except Exception as e:
		raise e
	finally:
		cursor.close()
		conn.close()


def UpdateEssay(title, date, body, lock, tag=""):
	conn = get_conn()
	cursor = conn.cursor()
	sql = "update Essay set "\
				"uptime = '%s', pwd = '%s', body = '%s', tag = '%s' "\
					"where title = '%s'"%(date, lock, body, tag, title)
	try:
		cursor.execute(sql)
		conn.commit()
	except Exception as e:
		raise e
	finally:
		cursor.close()
		conn.close()

def DeleteEssay(tableID):
	conn = get_conn()
	cursor = conn.cursor()
	sql1 = "select * from Essay limit %d,1"%tableID
	try:
		cursor.execute(sql1)
		essayID = cursor.fetchone()[0]
        
		sql = "delete from Essay where essayID = '%s'"%essayID
		cursor.execute(sql)
		conn.commit()
	except Exception as e:
		raise e
	finally:
		cursor.close()
		conn.close()
        #return "%s"%essayID

def SelectEssay(title):
	conn = get_conn()
	cursor = conn.cursor()
	sql = "select * from Essay where title = '%s'"%title
	try:
		cursor.execute(sql)
		essay = cursor.fetchone()
		conn.commit()
	except Exception as e:
		raise e
	finally:
		cursor.close()
		conn.close()
	return essay

def listEssays():
	conn = get_conn()
	cursor = conn.cursor()
	sql = "select title, uptime, pwd, tag from Essay order by EssayID desc"
	try:
		cursor.execute(sql)
		artilces = cursor.fetchall()
		conn.commit()
	except Exception as e:
		raise e
	finally:
		cursor.close()
		conn.close()

	return artilces


def CreateTableEssay():
	conn = get_conn()
	cursor = conn.cursor()
	sql = '''create table IF NOT EXISTS Essay(
	essayID INTEGER PRIMARY KEY AUTOINCREMENT,
	title TEXT NOT NULL,
	uptime TEXT NOT NULL,
	pwd TEXT,
	body TEXT ,
	tag TEXT
	)'''
	cursor.execute(sql)
	conn.commit()
	cursor.close()
	conn.close()

if __name__ == "__main__":
	CreateTableEssay()