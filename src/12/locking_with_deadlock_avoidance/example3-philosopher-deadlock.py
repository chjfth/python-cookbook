import time
import threading
from deadlock import acquire

# The philosopher thread
def philosopher(left, right):
    while True:
        with left:
            print(threading.currentThread(), 'grabbed left...') # time.sleep(0.01)
            with right:
            	print(threading.currentThread(), 'eating')

# The chopsticks (represented by locks)
NSTICKS = 5
chopsticks = [threading.Lock() for n in range(NSTICKS)]

# Create all of the philosophers
for n in range(NSTICKS):
    t = threading.Thread(target=philosopher,
            args=(chopsticks[n],chopsticks[(n+1) % NSTICKS]))
    t.daemon = True
    t.start()

while True:
    time.sleep(1)


