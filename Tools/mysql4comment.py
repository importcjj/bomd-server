#coding:utf-8

import sae.const
import MySQLdb as mdb
import time
#-----------------------------------------------------------------
# sae.const.MYSQL_DB      # 数据库名
# sae.const.MYSQL_USER    # 用户名
# sae.const.MYSQL_PASS    # 密码
# sae.const.MYSQL_HOST    # 主库域名（可读写）
# sae.const.MYSQL_PORT    # 端口，类型为<type 'str'>，请根据框架要求自行转换为int
# sae.const.MYSQL_HOST_S  # 从库域名（只读）
#-----------------------------------------------------------------



#获取数据库连接
def get_conn():
	conn = mdb.connect(
		host=sae.const.MYSQL_HOST,
		user=sae.const.MYSQL_USER,
		passwd=sae.const.MYSQL_PASS,
		db=sae.const.MYSQL_DB,
		port=int(sae.const.MYSQL_PORT),
		charset='utf8')
	return conn

def new_comment(essayTitle, username, email, parentID, replyto, content):
	conn = get_conn()
	cursor = conn.cursor()
	uptime = time.strftime('%Y-%m-%d %X', time.localtime())
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

def total():
	conn = get_conn()
	cursor = conn.cursor()
	try:
		sql = "select count(*) from Comment"
		cursor.execute(sql)
		num = cursor.fetchone()
		conn.commit()
	except Exception as e:
		return e
	finally:
		cursor.close()
		conn.close()
	return num

def CreateTableComment():
	conn = get_conn()
	cursor = conn.cursor()
	sql = '''create table IF NOT EXISTS Comment(
	commentID INT PRIMARY KEY AUTO_INCREMENT,
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