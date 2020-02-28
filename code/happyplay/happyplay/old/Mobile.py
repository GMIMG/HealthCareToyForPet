import socket as sk
import sys
import threading as th
import logging
import time
import serial

##logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s', )
ser3=serial.Serial('/dev/ttyUSB0',115200)

#####################연수 함수############################
def client():
    global pan,tilt
    HOST='192.168.0.200'
    PORT=8888

    s=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
    s.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
    s.bind((HOST,PORT))
    print(pan,tilt)

    while (True):
        s.listen(2)                             ##연결될 때까지 듣는중
        conn, addr = s.accept()
        print('connected by : ',addr)
            
        data = conn.recv(1024)                  ##client에서 받음
        data_decode=data.decode('utf-8')
        ##print(data_decode)
        ##print('\n')
            
        sign_up=data_decode.endswith("up")
        sign_down=data_decode.endswith("down")
        sign_left=data_decode.endswith("left")
        sign_right=data_decode.endswith("right")
        sign_break=data_decode.endswith("break")


        
        
##        if (sign_up==True):
##            sdata='up'+'\n'
##            ser3.write(sdata.encode('utf-8'))
##            print('up\n')
##            
##        elif (sign_down==True):
##            sdata='down'+'\n'
##            ser3.write(sdata.encode('utf-8'))
##            print('down\n')
##
##        elif (sign_left==True):
##            sdata='left'+'\n'
##            ser3.write(sdata.encode('utf-8'))
##            print('left\n')
##
##        elif (sign_right==True):
##            sdata='right'+'\n'
##            ser3.write(sdata.encode('utf-8'))
##            print('right\n')
##
##        elif (sign_break==True):
##            sdata='break'+'\n'
##            ser3.write(sdata.encode('utf-8'))
##            print('break\n')
##
##        else:
##            break


    conn.close()

###############################################################


##mobile = th.Thread(target=client)
##mobile.start()
##
##
##mobile.join()
##
##logging.debug('main program ended!\n')


