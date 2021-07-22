import sqlite3 as sql
import subprocess
import time
from datetime import datetime
import re

# creates db with specific name or makes connection to the db, if it's already exists
conn = sql.connect('statistic_data.db')

# creates tables and rows in it; if table/s are already exist, it skips this step
try:
    conn.execute('''CREATE TABLE ReceivedData
               (TIME INTEGER NOT NULL,
               LOST TEXT NOT NULL,
               PACKETTIME TEXT NOT NULL,
               TTL TEXT NOT NULL)''')
    print("Table ReceivedData created successfully")
except:
    pass

try:
    conn.execute('''CREATE TABLE LostData
               (TIME INTEGER NOT NULL,
               LOST TEXT NOT NULL,
               SENT TEXT NOT NULL,
               RECEIVED TEXT NOT NULL)''')
    print("Table LostData created successfully")
except:
    pass

try:
    conn.execute('''CREATE TABLE NoData
               (TIME INTEGER NOT NULL)''')
    print("Table NoData created successfully")
except:
    pass

### this block of code shows all data in selected table, just an example:
# alldata = conn.execute('SELECT * from LostData')
# rows = alldata.fetchall()
# print('\n LostData table')
# for row in rows:
#     print(row)

cur = conn.cursor()

def ping():
    current_time = datetime.now().strftime("%B %d, %Y %I:%M%p")
    # google web site is taken for an example
    response = subprocess.Popen(["ping", "www.google.com"], stdout=subprocess.PIPE)
    # ping response
    output = response.communicate()[0]

    try:
        lost = re.compile('Lost = \d*').search(str(output)).group()
        # if response is positive (=='0'), script takes useful information and sends it to the ReceivedData table
        if lost[-1] == '0':
            ttl = re.compile('TTL=\d*').search(str(output)).group()
            packettime = re.compile('time=\d*').search(str(output)).group()
            cur.execute('INSERT INTO ReceivedData (TIME, LOST, PACKETTIME, TTL) VALUES (?, ?, ?, ?)', (current_time, lost, packettime, ttl))
            conn.commit()
        # if response is negative, script commits info about missed data in table LostData
        else:
            sent = re.compile('Sent = \d*').search(str(output)).group()
            received = re.compile('Received = \d*').search(str(output)).group()
            cur.execute('INSERT INTO LostData (TIME, LOST, SENT, RECEIVED) VALUES (?, ?, ?, ?)', (current_time, lost, sent, received))
            conn.commit()
    # in case of totally lost internet connection
    except:
        cur.execute('INSERT INTO NoData VALUES (?)', (current_time,))
        conn.commit()
    # loops it again every 3 secs
    time.sleep(3)
    ping()
ping()