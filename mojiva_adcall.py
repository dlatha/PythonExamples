from threading import Thread
from random import randint
import time
import random
import requests
import xml.etree.ElementTree as ET

class mojia_adcall(Thread):
    def __init__(self,val,zone,user_agent,maddy):
        ''' Constructor. '''
        Thread.__init__(self)
        self.val=val
        self.zone = zone
        self.user_agent = user_agent
        self.maddy=maddy

    def run(self):
        response = requests.get(self.val)
        content = str(response.content)
        root = ET.fromstring(content)
        
        for url in root.iter('url'):
            url = url.text
        for img in root.iter('img'):
            img = img.text

        words = img.split('/img/')
        if len(words) < 2:
            words = img.split('&icon=')
#        print('Calling %d times in thread %s' % (self.v.value,self.getName()))

        ET.SubElement(maddy,"\n")
        ad = ET.SubElement(maddy,"ad")
        #ad.set("id",str(self.v.value))

        url_ele = ET.SubElement(ad,"url")
        url_ele.text=str(url)
        
        img_ele = ET.SubElement(ad,"img")
        img_ele.text = str(img)
        
        
        tree = ET.ElementTree(maddy)
        tree.write("adcall.xml")

if __name__ == '__main__':
    # Declare objects of MyThread class
    zone = 85
    url = "http://ads.mocean.mobi/ad?zone=" + str(zone) +"&key=3&type=2"
    user_agent="user_agent"
    maddy = ET.Element("maddy")
    
    myThreadOb = mojia_adcall(url,zone,user_agent,maddy)
    myThreadOb.setName("first")
    myThreadOb.start()
    myThreadOb.join()
    print('Main Terminating...')

