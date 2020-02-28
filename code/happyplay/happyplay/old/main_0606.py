from Mobile import*
from Tracking import*
##from Dog import*

import sys
import threading 
import logging

logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s', )
pan=0
tilt=0

###지민 Dog
##dataGS=threading.Thread(target=dataGetherSend)
##dataGS.start()

###예은 Tracking
track = threading.Thread(target=CamshiftTracking)


###연수 Mobile
mobile = threading.Thread(target=client)
track.start()
mobile.start()


##dataGS.join()
mobile.join()
track.join()




logging.debug('main program ended!\n')
