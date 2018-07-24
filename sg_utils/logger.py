from flask import request
import time, sys, os
import traceback
from itertools import takewhile, repeat


def print_error(e):
	print((e, sys.exc_info()[0].__name__, os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename), sys.exc_info()[2].tb_lineno))
	print(str(traceback.format_exc().splitlines()))

class Logger(object):
	"""docstring for Logger"""

	def __init__(self, file_name, limit=10000):
		self.file_name = file_name
		self.limit = limit
		self.lc = self._linecount()

	def _linecount(self):
		if not os.path.isfile(self.file_name): return 0
		with open(self.file_name, 'rb') as f:
			bufgen = takewhile(lambda x: x, (f.read(1024*1024) for _ in repeat(None)))
			return sum( buf.count(b'\n') for buf in bufgen )

	def _truncate(self):
		bak = self.file_name+'.bak'
		os.system('head -n {count} {f} > {bak}; mv {bak} {f}'.format(count=self.limit, f=self.file_name, bak=bak))
		self.lc = self.limit


		
	def log(self, message, _print=True):
		mess = '[ {} ] - {}'.format(str(time.ctime(time.time())), str(message))
		with open(self.file_name, "a") as log_file:
			log_file.write(mess+'\n')
		if _print:
			print(mess)
		self.lc += 1
		if self.lc%100==0 and self.lc>self.limit:
			self._truncate()


	def error(self, e):
		self.log((e, sys.exc_info()[0].__name__, os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename), sys.exc_info()[2].tb_lineno))

	def traceback(self, e):
		self.log(str(traceback.format_exc().splitlines()))



class FlaskLogger(object):
	"""
	docstring for FlaskLogger
	
	Requires 'LOG_FILE' config entry
	"""

	def __init__(self, app):
		try:
			super(self.__class__, self).__init__(app.config['LOG_FILE'])
		except:
			super(self.__class__, self).__init__('./event_log.log')


	def log(self, message, _print=True):
		try:
			ip = str(request.headers['X-Real-Ip'])
		except: ip = 'ip_not_found'
		mess = '{} - {} - {}'.format(ip, str(time.ctime(time.time())), str(message))
		with open(self.file_name, "a") as log_file:
			log_file.write(mess+'\n')
		if _print:
			print(mess)



		
if __name__ == '__main__':
	log = Logger('./logtest.log')
	log.log('hello world')