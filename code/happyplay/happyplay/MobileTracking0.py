import socket as sk
import sys
import threading as th
import logging
import time
import serial

import cv2
import numpy as np
from math import *
import random

A=1

ser3=serial.Serial('/dev/ttyUSB0',115200)
sdata='stop'+'\n'
ser3.write(sdata.encode('utf-8'))




#####################연수 함수############################



def client():
    global pan,tilt
    global A
    HOST='192.168.0.47'
    PORT=8888

    s=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
    s.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
    s.bind((HOST,PORT))

    while (True):
        s.listen(2)                             ##연결될 때까지 듣는중
        conn, addr = s.accept()
        print('connected by : ',addr)

        data = conn.recv(1024)                  ##client에서 받음
        data_decode=data.decode('utf-8')
        
        sign_up=data_decode.endswith("up")
        sign_down=data_decode.endswith("down")
        sign_left=data_decode.endswith("left")
        sign_right=data_decode.endswith("right")
        sign_stop=data_decode.endswith("stop")

        if (sign_up==True):
            sdata='up'+'\n'
            print('up\n')
        elif (sign_down==True):
            sdata='down'+'\n'
            print('down\n')
        elif (sign_left==True):
            sdata='left'+'\n'
            print('left\n')
        elif (sign_right==True):
            sdata='right'+'\n'
            print('right\n')
        elif(sign_stop==True):
            sdata='stop'+'\n'
            A+=1
            print('stop\n')
            print(A)
        else:
            conn.close()
            break
        
        ser3.write(sdata.encode('utf-8')) 
        conn.close()
        
##########################################################
        
#####################yeaheun함수############################
#For Tracking
col, width, row, height =-1, -1, -1, -1
frame=None
frame2=None
inputmode=False
rectangle=False
trackWindow=None
roi_hist=None
cx=0; cy=0
green=(0,255,0)
red=(255,0,0)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.createBackgroundSubtractorMOG2()


#For Culculate
pan=0; tilt=0
pre_pan=0; pre_tilt=0
q=0


    
def CamshiftTracking():
    #motor init


    
    global frame, trackWindow, roi_hist
    global cxTest, cyTest
    global x,y,h,w
    global A #A 는 연수와 나의연결고리
    global q
    
    init=0
    

    #SelectObject()

    try:
        cap=cv2.VideoCapture(1)
        cap.set(3,1280)
        cap.set(4,720)

    except:
        print('카메라가 인식이 안된대..')
        return


    
    while True:
        ret, frame=cap.read()

        frame=cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        fgmask = fgbg.apply(frame)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        fgmask = cv2.GaussianBlur(fgmask, (101, 101), 0)
        

        _,binary = cv2.threshold(fgmask,1,255,0)
        _,contours,_ = cv2.findContours(binary,1,2)

                
        if not ret:
            break

            


        if len(contours) > 0:
            pre_area=0
            k=0
            for i in range(len(contours)):
                cnt = contours[i]

                #perimeter = cv2.arcLength(cnt,True)
                M = cv2.moments(cnt)
                area=M['m00']
                if area != 0 and area>pre_area:
                    cx,cy = int(M['m10']/area),int(M['m01']/area)
                    pre_area=area
                    k=i

            cnt=contours[k] ##가장 모양이 큰 값 k

            #frame에 contours를 그린다.
            cv2.drawContours(frame,[cnt],0,green,2)

            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),red,2)

        cv2.imshow('frame',frame) #display monitoring (*can be slowly)
        
        #모터를 돌리는 코드
        if init==0:

            wx=-18; wy=20
            pp1=(wx-36.075)/(-0.1156); pp2=(wy-177.88)/(-0.4276) #구해진 pixcel좌표
            pan= atan(wx/(wy+3))*180/pi #수직, 좌우
            tilt= (atan(25/(sqrt((wx**2)+((wy+3)**2))))*180/pi)
        
            init=1
        

        if int(x)-50<int(pp1)<int(x+w)+50 and int(y)-50<int(pp2)<int(y+h)+50:
            print ('success')
            
            wx=[0,-18]; wy=[30,20]
            pp1=(wx[q]-36.075)/(-0.1156); pp2=(wy[q]-177.88)/(-0.4276)
            pan= atan(wx[q]/(wy[q]+3))*180/pi #수직, 좌
            tilt= (atan(20/(sqrt((wx[q]**2)+((wy[q]+3)**2))))*180/pi)
            q=q+1

            if q==2:
                q=0
        
        if ((A%2)==1):
            motor(int(pan), int(tilt))
            print('pan=',int(pan),'tilt=',int(tilt))
            print('wx=',wx,'wy=',wy)


        k=cv2.waitKey(60)&0xFF
        if k==27:
            cap.release()
            cv2.destroyAllWindows()  
            break

def motor(pan, tilt):
    global pre_pan, pre_tilt
    if (pan!=pre_pan and tilt!=pre_tilt):
            pre_pan=pan; pre_tilt=tilt
            print('ccchange')

            if(pan<0):
                    pan=-pan
                    if pan<10:
                            a='-'+'0'+str(pan)
                    else:
                            a='-'+str(pan)
                            
            else:
                    if pan<10:
                            a='+'+'0'+str(pan)
                    else:
                            a='+'+str(pan)
                    

            if(tilt<0):
                    tilt=-tilt
                    if tilt<10:
                    
                            b='-'+'0'+str(tilt)
                    else:
                            b='-'+str(tilt)
            else:
                    if tilt<10:
                    
                            b='+'+'0'+str(tilt)
                    else:
                            b='+'+str(tilt)

            sdata='@'+a+b+'\n'
            ser3.write(sdata.encode('utf-8'))
            time.sleep(1)
