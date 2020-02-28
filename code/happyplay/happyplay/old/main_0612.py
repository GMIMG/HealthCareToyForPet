#!/usr/bihn/env python

from MobileTracking3 import*
#from Dog import*

import sys
import threading 
import logging

logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s', )
pan=0
tilt=0

###지민 Dog
#dataGS=threading.Thread(target=dataGetherSend)
#dataGS.start()
print("##########################")

###예은 연수 MobileTracking
mobile = threading.Thread(target=client)
track = threading.Thread(target=CamshiftTracking)

track.start()
print("##########################")
mobile.start()
print("##########################")

#dataGS.join()
mobile.join()
track.join()




logging.debug('main program ended!\n')
