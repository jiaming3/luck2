import paho.mqtt.client as mqtt
import json
import time
client = mqtt.Client()
client.connect("test.mosquitto.org",port=1883)
message = {'meaage':"from compujter"}
payload=json.dumps(message)
i = 0
while i <1:
  client.publish("IC.embedded/Team_ALG/test",payload)
  time.sleep(3)
