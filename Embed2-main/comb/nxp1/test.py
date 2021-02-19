#!/usr/bin/env python

from __future__ import division, print_function
from nxp_imu import IMU
import time
from bmp280 import bmp280_readdata,bmp280_convert,bmp280_checktemp
from si import hum,temp
 
"""
accel/mag - 0x1f
gyro - 0x21
bmp280 - 0x77
si7021 - 0x44
pi@r2d2 nxp $ sudo i2cdetect -y 1
    0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 1f
20: -- 21 -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: 40 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- 77
"""
import paho.mqtt.client as mqtt

import json
import time
receive_data = 1


client = mqtt.Client(userdata=receive_data)
 
def on_message(client, userdata, message):
 global receive_data
 receive_data = json.loads(message.payload)
   
def on_connect(client, userdata, flags, rc):
 if rc==0:
  print('connected successfully')
 client.subscribe("IC.embedded/Team_ALG/#",2)

client.on_connect = on_connect
client.on_message = on_message
 
 
client.connect("test.mosquitto.org",port=1883)

def publish_data(temp,hum,pressure,flower_pot):
  payload=json.dumps({"temp":temp,"humidity":hum,"pressure":pressure,"flowerpot":flower_pot})
  client.publish("IC.embedded/Team_ALG/test",payload)
  #default keep alive is 60s,thus we need at least 1 imformation change between broker and client per minutes#
  
def receive():
  global receive_data
  client.loop_start()
  time.sleep(20) #change holding-connection-state time here
  client.loop_stop()
  
   
  
# the following function is able to read all the data from the sensor,but it not use in the main
def imu():
    imu = IMU(gs=4, dps=2000, verbose=True)
    header = 67
    print('-'*header)
    print("| {:17} | {:20} | {:20} |".format("Accels [g's]", " Magnet [uT]", "Gyros [dps]"))
    print('-'*header)
    for _ in range(10):
        a, m, g = imu.get()
        print('| {:>5.2f} {:>5.2f} {:>5.2f} | {:>6.1f} {:>6.1f} {:>6.1f} | {:>6.1f} {:>6.1f} {:>6.1f} |'.format(
            a[0], a[1], a[2],
            m[0], m[1], m[2],
            g[0], g[1], g[2])
        )
        time.sleep(0.50)
    print('-'*header)
    print(' uT: micro Tesla')
    print('  g: gravity')
    print('dps: degrees per second')
    print('')

#this function convert sensor data to roll,pitch and yaw. However,yaw is not accurate enough without use of kalman filter and
# other alogorithm such as sensor fusion. stepper motor may use instead
def ahrs():
    #print('')
    imu = IMU(verbose=False)
    header = 47
    #print('-'*header)
    #print("| {:20} | {:20} |".format("Accels [g's]", "Orient(r,p,h) [deg]"))
    #print('-'*header)
    fall = False
    #for _ in range(10):
    a, m, g = imu.get()# get data from nxp-9dof fxos8700 + fxas21002
    r, p, h = imu.getOrientation(a, m) # convert sensor data to angle in roll,pitch,yaw axis
    #print the angle data
    #print('| {:>6.1f} {:>6.1f} {:>6.1f} | {:>6.1f} {:>6.1f} {:>6.1f} |'.format(a[0], a[1], a[2], r, p, h))
    time.sleep(1)

    r = abs(r)
    p = abs(p)
    #h =abs(h)

    if r>50 or p>50 :
        fall = True
    else:
        fall =False

    return fall


if __name__ == "__main__":
    try:

       while True:
        client.loop_start()
        flower = ahrs()
        data = bmp280_readdata()
        p = bmp280_convert(data)
        t = bmp280_checktemp(data)
        te = temp()
        hu = hum()
        print("fall:", flower, "pressure:", p, "temperature:", t, "humidity:", hu)
        publish_data(te, hu, p, flower)
   
        time.sleep(6)
        print(receive_data)
        client.loop_stop()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        pass

    #print('Done ...'
