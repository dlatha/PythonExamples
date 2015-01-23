from threading import Thread
from random import randint
import time
import random
import requests
import xml.etree.ElementTree as ET
from multiprocessing import Value, Lock

class MyThread(Thread):
    def __init__(self, val,v,lock,maddy):
        ''' Constructor. '''
        Thread.__init__(self)
        self.val = val
        self.v = v
        self.lock = lock
        self.maddy = maddy

    def run(self):

      for i in range(1,3):
        response = requests.get(self.val)
        content = str(response.content)
        root = ET.fromstring(content)

        for url in root.iter('url'):
            url = url.text
        for img in root.iter('img'):
            img = img.text
        #        print img
        words = img.split('/img/')
        if len(words) < 2:
            words = img.split('&icon=')
        print('Calling %d times in thread %s' % (self.v.value,self.getName()))

        ET.SubElement(maddy,"\n")
        ad = ET.SubElement(maddy,"ad")
        ad.set("id",str(self.v.value))

        url_ele = ET.SubElement(ad,"url")
        url_ele.text=str(url)

        img_ele = ET.SubElement(ad,"img")
        img_ele.text = str(img)

        with lock:
            self.v.value +=1

      tree = ET.ElementTree(maddy)
      tree.write("filename.xml")

if __name__ == '__main__':
    # Declare objects of MyThread class
    url = "http://ads.mocean.mobi/ad?zone=85&key=3&type=2"
    v = Value('i', 1)
    lock = Lock()
    maddy = ET.Element("maddy")
    num_of_threads = 1
    num_of_calls = int(raw_input("Enter number of calls to be made:"))

    if num_of_calls == 1 or num_of_calls % 2 != 0:
        num_of_calls = num_of_calls + 1

    num_of_threads = num_of_calls / 2

    for i in range(1,num_of_threads + 1):
        myThreadOb = MyThread(url,v,lock,maddy)
        threadname = "Thread" + str(i)
        myThreadOb.setName(threadname)
        myThreadOb.start()
        myThreadOb.join()
    print('Main Terminating...')
