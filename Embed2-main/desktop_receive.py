import paho.mqtt.client as mqtt
import time

client = mqtt.Client()
client.connect("test.mosquitto.org",port=1883)

import json
 

def on_message(client, userdata, message):
   mesg = json.loads(message.payload)
   print(mesg)
   

client.on_message = on_message
client.subscribe("IC.embedded/Team_ALG/#",2)

client.loop_start()
time.sleep(20)
client.loop_stop()
