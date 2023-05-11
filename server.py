#need to pip install  tt
# pip3 install -r requirements.txt 
import requests
import json
import time
import datetime
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import sqlite3
import random
import time
from flask import Flask, jsonify
#from flask_cors import CORS
from flask_cors import CORS, cross_origin

#hi g
#run below only once to createn table..
# conn = sqlite3.connect("library.db")
# cursor = conn.cursor()
# cursor.execute("""CREATE TABLE bcsonoff2
#                  (counter INTEGER, voltage INTEGER, power INTEGER, timestamp1 TIMESTAMP)
#              """)

#---------Imports
from numpy import arange, sin, pi
import numpy as np
counter2=0

app = Flask(__name__)
CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
# @cross_origin()
def hello():
  return "lala"

@app.route("/hello")
def hello2():
  global counter2
  counter2 +=1
  return jsonify([counter2,5,6,7, "amazing"]) 
  # return "This is a test   "+str(counter2)f f

open('example.txt', 'w').close()
consumecount = 0 
counter = 1
recentconsume = []
consumecountlist = []
broker = 'broker.emqx.io'
sub_topic = "stat/mospow2/STATUS10"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(sub_topic)
    print("subscribed to ..." + sub_topic)

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_message(client, userdata, msg):
    global counter
    global consumecount
    global recentconsume
    global consumecountlist
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    m_in = json.loads(m_decode) #decode json data
    #print(type(m_in))
    voltage = m_in["StatusSNS"]["ENERGY"]["Voltage"]
    power = m_in["StatusSNS"]["ENERGY"]["Power"]
    timestamp = int(time.time())
    print("Voltage = " + str(voltage) + "  Power = " + str(power))
    #append spreadsheet - the big moment!
    #write to text file
    
    with open('example.txt', 'r+') as f:
        lines = f.readlines()

        consumecount +=1
        recentconsume.append(str(power))
        consumecountlist.append(str(consumecount))
        #put number of reads that are OK before starting to scroll
        if consumecount >=30:
            f.seek(0)
            f.truncate()
            f.writelines(lines[1:])
            recentconsume.pop(0)
            consumecountlist.pop(0)
        nuwe = str(counter)+"," + str(power)
        f.write(nuwe)
        f.write('\n')

    
    body=[timestamp, voltage, power] #the values should be a list

    ## TO DO CALL THIS EVERY 15 seconds
    # thingspeakcall = "https://api.thingspeak.com/update?api_key=ZIPWDOGJTN68PNDL&field1="+str(voltage)
    # thingspeakcall2 = "https://api.thingspeak.com/update?api_key=ZIPWDOGJTN68PNDL&field1="+str(voltage)+"&field2="+str(power)
    # print (thingspeakcall2)
    # x = requests.get(thingspeakcall2)
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    counter = counter + 1
    insertQuery = """INSERT INTO bcsonoff2 VALUES (?, ?, ?, ?);"""
    currentDateTime = datetime.datetime.now()
    cursor.execute(insertQuery, (counter, voltage, power, currentDateTime))
    conn.commit()
    cursor.execute(""" SELECT max(rowid) FROM bcsonoff2 """)
    recordcount = cursor.fetchone()[0]
    print ("number of databse records =  "+str(recordcount))
    #next step retrieve data, maybe from another file
    stats = str(voltage)+"V  "+ str(power)+"W "+str(recordcount)+" recs"
    client.publish("stats", stats)

##exper start 



##exper end

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, 1883, 60)
client.loop_start()

if __name__ == "__main__":
  app.run()

while True:
    print ("loop running yay")
    client.publish("cmnd/mospow2/STATUS", 10)
    client.publish("werkreplit", "yep")
    # this little bugger below stuffed up my json validation!!! test gh
    
    #client.publish("werkdit", "yep")
    
    time.sleep(1)
  
    #print number of records in data base
    #root.update()


# root = Tk()
# # Open window having dimension 100x100
# root.geometry('100x100')

# btn = Button(root, text = 'Click me !', bd = '5',
# command = root.destroy)
# root.mainloop()

#put in overall while loop 
# ping the sonoff device for readings
# write the readings tot the gsheet
####tk loop





######tk loop#####



    


#kind of important to do the loop forever and must be last line
