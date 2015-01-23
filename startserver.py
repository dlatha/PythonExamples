#!/usr/bin/env python
import xml.etree.ElementTree as ET
from wsgiref.simple_server import make_server
from cgi import parse_qs, escape
from wurfl_cloud import Cloud as WurflCloud
from wurfl_cloud import utils
import mysql.connector
from getnewzone_id import Getnewid
from mojiva_adcall import mojiva_adcall
from xml.dom.minidom import parse, parseString


def application(environ, start_response):
    # Returns a dictionary containing lists as values.
    d = parse_qs(environ['QUERY_STRING'].replace(';',''))
    # In this idiom you must issue a list containing a default value.
    # Get thezone, ip and age from the params
    zone = d.get('zone', [''])[0]
    ip = d.get('ip', [''])[0]
    ua = d.get('ua', [''])[0]

                
    # Always escape user input to avoid script injection
    zone = escape(zone)
    ip = escape(ip)
    ua = ua
    
    #connecting to the wurfl database to get the user agent information
    config = utils.load_config('/app/WurflCloudClient-Python-1.0.1-Simple/examples/filecache_config.conf')
    cache = utils.get_cache(config)
    client = WurflCloud(config, cache)
    
    device = client(ua, capabilities=["ux_full_desktop", "model_name", "brand_name"])

    user_ag='unknown'
    model_name='unknown'
    brand_name = 'unknown'
    for i in device:
        if str(i)=='id':
            user_ag=str(device[i])
        if str(i)=='capabilities':
            for capability in device[i]:
                if str(capability) =='model_name':
                    model_name = str(device[i][capability])
                if str(capability)=='brand_name':
                    brand_name = str(device[i][capability])

    #get the new zone ID from teh old zone ID
    new_zoneid = Getnewid(zone)
    zone = new_zoneid.get_newzoneid()

    #start of the ad call to mojia server
    url = "http://ads.mocean.mobi/ad?zone=" + zone +"&key=3&type=2"
    maddy = ET.Element("maddy")

    adcall = mojiva_adcall(url,zone,ua,model_name,brand_name,maddy)
    xmlfile = adcall.create_xml()
    dom = parse(xmlfile);
    adresponse = str(dom.toprettyxml())

    response_body = adresponse
    status = '200 OK'

    # Now content type is text/xml
    response_headers = [('Content-Type', 'text/xml'),('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)
                                        
    return [response_body]

httpd = make_server('localhost', 8051, application)
httpd.serve_forever()

