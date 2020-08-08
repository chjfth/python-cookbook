import threading
import time

class PeriodicTimer:
	def __init__(self, interval):
		self._interval = interval
		self._flag = 0
		self._cv = threading.Condition()

	def start(self):
		t = threading.Thread(target=self.run)
		t.daemon = True
		t.start()

	def run(self):
		'''
		Run the timer and notify waiting threads after each interval
		'''
		while True:
			time.sleep(self._interval)
			with self._cv:
				self._flag ^= 1
				self._cv.notify_all()

	def wait_for_tick(self, tls):
		'''
		Wait for the next tick of the timer
		'''
		with self._cv:
			last_flag = self._flag
			while last_flag == self._flag:
				self._cv.wait()
				print('[{}] sees {}'.format(tls.myid, '=='if last_flag==self._flag else '!!'))

# Example use of the timer
ptimer = PeriodicTimer(2)
ptimer.start()

# Two threads that synchronize on the timer
def countdown(nticks, tls):
	tls.myid = 'D'
	while nticks > 0:
		ptimer.wait_for_tick(tls)
		print("T-minus", nticks)
		nticks -= 1

def countup(last, tls):
	tls.myid = 'U' # will not overwrite 'D' of countdown()
	n = 0
	while n < last:
		ptimer.wait_for_tick(tls)
		print("Counting", n)
		n += 1

tls = threading.local() # chj
#
threading.Thread(target=countdown, args=(10, tls)).start()
threading.Thread(target=countup, args=(5, tls)).start()
