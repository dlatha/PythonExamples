from threading import Thread
from random import randint
import time
import random
import requests
import xml.etree.ElementTree as ET
from getnewzone_id import Getnewid

class mojiva_adcall(object):
    def __init__(self,adcall,zone,user_agent,model_name,brand_name,maddy):
        ''' Constructor. '''
        self.adcall=adcall
        self.zone = zone
        self.user_agent = user_agent
        self.brand_name=brand_name
        self.model_name=model_name
        self.maddy=maddy
        self.xmlfile="adcall.xml"

    def create_xml(self):
        response = requests.get(self.adcall)
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

        ad = ET.SubElement(self.maddy,"ad")
        #ad.set("id",str(self.v.value))

        url_ele = ET.SubElement(ad,"url")
        url_ele.text=str(url)
        
        img_ele = ET.SubElement(ad,"img")
        img_ele.text = str(img)
        
        img_ele = ET.SubElement(ad,"ua")
        img_ele.text = str(self.user_agent)

        img_ele = ET.SubElement(ad,"model_name")
        img_ele.text = str(self.model_name)

        img_ele = ET.SubElement(ad,"brand_name")
        img_ele.text = str(self.brand_name)

        tree = ET.ElementTree(self.maddy)
        tree.write(self.xmlfile)
        return self.xmlfile
