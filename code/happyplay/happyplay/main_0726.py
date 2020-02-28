#!/usr/bihn/env python
import os
import sys
import time 
import threading 
import logging
os.system('sudo chmod 666 /dev/ttyS0')
os.system('sudo modprobe bcm2835-v4l2')
from MobileTracking4 import*
from Dog import*


#logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s ) %(message)s', )
#time.sleep(5)

###지민 Dog
dataGS=threading.Thread(target=dataGetherSend)
dataGS.start()
print("##########################")

###예은 연수 MobileTracking
mobile = threading.Thread(target=client)
track = threading.Thread(target=CamshiftTracking)

track.start()
print("##########################")
mobile.start()
print("##########################")

dataGS.join()
mobile.join()
track.join()




#logging.debug('main program ended!\n')
