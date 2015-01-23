from wurfl_cloud import Cloud as WurflCloud
from wurfl_cloud import utils
import mysql.connector

class Getnewid(object):
 def __init__(self, zone):
        self.zone = zone
        self.new_zoneid = ''
 
 def get_newzoneid(self):
        config = {
        'user': 'xxx',
            'password': 'xxxx',
                'host': '127.0.0.1',
                'database': 'zone',
                'raise_on_warnings': True,
                    }
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        select_zone = ("select new_id from zone where old_id=%s")
        
        cursor.execute(select_zone,(self.zone,))
        
        rows = cursor.fetchall()
        
        if not rows:
            self.new_zoneid = 'Invalid data'
        for row in rows:
            self.new_zoneid = str(row[0])
        conn.commit()
        cursor.close()
        conn.close()

        return self.new_zoneid


