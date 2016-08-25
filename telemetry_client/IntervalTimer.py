from threading import Thread, Event
from time import sleep

class StoppableThread(Thread):  

    def __init__(self):
        super(StoppableThread,self).__init__()
        self.stop_event = Event()
        self.daemon = True

    def stop(self):
        if self.isAlive() == True:
            self.stop_event.set()
            self.join()

class IntervalTimer(StoppableThread):

    def __init__(self, interval, worker_func):
        super(IntervalTimer, self).__init__()
        self._interval = interval
        self._worker_func = worker_func
        self.paused = 0

    def run(self):
        while not self.stop_event.is_set():
            if not self.paused:
		self._worker_func()
            sleep(self._interval)

    def pause(self):
        self.paused = 1

    def unpause(self):
        self.paused = 0

