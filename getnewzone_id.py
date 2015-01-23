from wurfl_cloud import Cloud as WurflCloud
from wurfl_cloud import utils
import mysql.connector

config = {
    'user': 'root',
    'password': 'maddykrish',
    'host': '127.0.0.1',
    'database': 'zone',
    'raise_on_warnings': True,
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

select_zone = ("select new_id from zone where old_id=%s")

cursor.execute(select_zone,('123243',))

rows = cursor.fetchall()
if not rows:
    print 'no rows'
for row in rows:
    print row[0]

config = utils.load_config('/app/WurflCloudClient-Python-1.0.1-Simple/examples/filecache_config.conf')
cache = utils.get_cache(config)
client = WurflCloud(config, cache)

ua = 'Nokia3650/1.0 UP.Browser/6.2' # Presented as an example
device = client(ua, capabilities=["ux_full_desktop", "model_name", "brand_name"])

print device
#conn.commit()

#cursor.close()
#conn.close()