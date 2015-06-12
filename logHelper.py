#coding:utf-8



__all__ = ['log']

import time


def log(logFile, logMessage):
	"""简单的日志记录
	"""
	RESULT = "FALSE"
	date = time.strftime('%Y-%m-%d %X',time.localtime())
	try:
		with open(logFile, 'a+') as fp:
			fp.write(date + " : " + logMessage + "\n")

		RESULT = "OK"
	except Exception as e:
		with open('log/logHelper.log', 'a+') as f:
			f.write(date + " : " + e.message + "\n")
		RESULT = "FALSE"
	finally:
		return RESULT



if __name__ == "__main__":
	log('log/test.log','cjj-module logHelper test')

