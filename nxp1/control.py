import time
from bmp280 import bmp280_readdata,bmp280_convert,bmp280_checktemp
from si import hum,temp
from motor import init,forward,reverse,stop
import RPi.GPIO as gpio


def right(tf):
    init()
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(tf)
    gpio.cleanup()
    forward(0.025)

def funcclk(times,time):

        for x in range(1,times):#how many times rotate per day
            right(time)#here, set time to control the rotation time(angle)
            time.sleep(86400/times)#time interval between each rotation

def funcsensor():
    data = bmp280_readdata(0x77)
    p = bmp280_convert(data)
    t = bmp280_checktemp(data)
    te = temp()
    hu = hum()
    booldone=False
    global pointer
    pointer=0
    couter=0
    while booldone==False:
        if te > 35 and couter <2:
            reverse(x)  # set x manually here to control the time of operation
            counter=counter+1
            pointer = pointer + 1
        elif hu > 80 and couter <2:
            reverse(x) # set x manually here to control the time of operation
            counter = counter + 1
            pointer = pointer + 1
        elif p > 1005.7 and couter <2:
            reverse(x) # set x manually here to control the time of operation
            counter = counter + 1
            pointer = pointer + 1
        else:
            pass
    #time.sleep(1800)
    couter=0

def funcreturn():
    if pointer!=0:
        forward(pointer*x)#here x should be the same value with the previous function,前面退了几次这里一次性前进回去
        pointer=0
    else:
        pass















