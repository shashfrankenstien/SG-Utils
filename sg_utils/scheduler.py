import time
from datetime import timedelta, datetime as dt
import holidays

USHolidays = holidays.US()


class Job(object):

	RUNABLE_DAYS = {
		'day': lambda d : True,
		'weekday': lambda d : d.isoweekday() < 6,
		'weekend': lambda d : d.isoweekday() > 5,
		'businessday': lambda d : d not in USHolidays,
		'holiday': lambda d : d in USHolidays or d.isoweekday() > 5
	}

	def __init__(self, every, at, func, kwargs):
		self.interval = every
		self.time_string = at
		self.func = func
		self.kwargs = kwargs
		self.schedule_next_run()
		print(self)

	def to_timestamp(self, d):
		return time.mktime(d.timetuple())+d.microsecond/1000000.0

	def schedule_next_run(self, just_ran=False):
		h, m = self.time_string.split(':')
		n = dt.now()
		n = dt(n.year, n.month, n.day, int(h), int(m), 0)
		ts = self.to_timestamp(n)
		if self.job_must_run_today() and time.time() < ts+500 and not just_ran: 
			self.timestamp = ts
		else:
			next_day = n + timedelta(days=1)
			while not self.job_must_run_today(next_day):
				next_day += timedelta(days=1)
			self.timestamp = self.to_timestamp(next_day)#next_day.timestamp()

	def job_must_run_today(self, date=None):
		return self.RUNABLE_DAYS[self.interval](date or dt.now())


	def is_due(self):
		# print(str(dt.fromtimestamp(time.time())), str(dt.fromtimestamp(self.timestamp)), time.time() >= self.timestamp)
		return time.time() >= self.timestamp

	def run(self):
		try:
			print("========== Scheduler Start =========")
			print(self)
			return self.func(**self.kwargs)
		except Exception as e:
			print(e)
		finally:
			print("Finished execution of {}".format(self))
			self.schedule_next_run(just_ran=True)
			print("========== Scheduler End =========")


	def __repr__(self):
		return "{}. Scheduled = {}".format(self.func, str(dt.fromtimestamp(self.timestamp)))



class TaskScheduler(object):

	def __init__(self):
		self.jobs = []

	def __current_timestring(self):
		return dt.now().strftime("%H:%M")

	def check(self):
		for j in self.jobs:
			if j.is_due():
				j.run()

	def every(self, interval):
		self.interval = interval
		return self

	def at(self, time_string):
		if not self.interval: self.interval = 'day'
		self.temp_time = time_string
		return self

	def do(self, func, **kwargs):
		if not self.interval: raise Exception('Run .at()/.every().at() before .do()')
		if not self.temp_time: self.temp_time = self.__current_timestring()
		self.jobs.append(Job(self.interval, self.temp_time, func, kwargs))
		self.temp_time = None
		self.interval = None
		return True






if __name__ == '__main__':
	def job(x, y): print(x, y)

	s = TaskScheduler()
	k = s.every('holiday').at("23:31").do(job, x="hello", y="world")

	x = 1
	while x <5:
		s.check()
		x +=1
		time.sleep(1)
		print('ran')
	print(s.jobs)