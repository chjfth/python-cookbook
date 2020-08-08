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
			with self._cv:
				self._flag ^= 1
				print("_cv.notify_all() ...")
				self._cv.notify_all()
			
			# chj: sleep() *after* notify.
			# and we can see that: the _cv.notify_all() above won't wake up 
			# other thread's later _cv.wait()
			time.sleep(self._interval) 

	def wait_for_tick(self, myid):
		'''
		Wait for the next tick of the timer
		'''
		with self._cv:
			last_flag = self._flag
			while last_flag == self._flag:
				print('[{}] waits... '.format(myid))
				self._cv.wait()
				print('[{}] sees {}'.format(myid, '=='if last_flag==self._flag else '!!'))

# Example use of the timer
ptimer = PeriodicTimer(2)
ptimer.start()

# Two threads that synchronize on the timer
def countdown(nticks, myid):
	time.sleep(0.5) # delay 100ms so that _cv.notify_all() executes first
	while nticks > 0:
		ptimer.wait_for_tick(myid)
		print("T-minus", nticks)
		nticks -= 1

def countup(last, myid):
	time.sleep(0.5) # delay 100ms so that _cv.notify_all() executes first
	n = 0
	while n < last:
		ptimer.wait_for_tick(myid)
		print("Counting", n)
		n += 1

threading.Thread(target=countdown, args=(10,'D')).start()
threading.Thread(target=countup, args=(5,'U')).start()
