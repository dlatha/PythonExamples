from threading import Thread
from random import randint
import time
import random
import requests
import xml.etree.ElementTree as ET
from multiprocessing import Process, Value, Lock

class MyThread(Thread):
    def __init__(self, val, lock):
        ''' Constructor. '''
        Thread.__init__(self)
        self.val = val
        self.lock = lock


    def run(self):
        for i in range(1,3):
            print self.val.value
            with lock:
                self.val.value += 1

#print('Value calling %d time in thread %s' % ( i,self.getName()))

if __name__ == '__main__':
    v = Value('i', 1)
    lock = Lock()
    for i in range(1,3):
        myThreadOb = MyThread(v,lock)
        threadname = "Thread" + str(i)
        myThreadOb.setName(threadname)
        myThreadOb.start()
        myThreadOb.join()

    print('Main Terminating...')