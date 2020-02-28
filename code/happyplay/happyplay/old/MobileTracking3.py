import socket as sk
import sys
import threading as th
import logging
import time
import serial

import cv2
import numpy as np
import math
import random

A=2
pan=0
tilt=0




#####################연수 함수############################

##logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s', )
ser3=serial.Serial('/dev/ttyUSB0',115200)

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
            ser3.write(sdata.encode('utf-8'))
            print('up\n')
            
        elif (sign_down==True):
            sdata='down'+'\n'
            ser3.write(sdata.encode('utf-8'))
            print('down\n')

        elif (sign_left==True):
            sdata='left'+'\n'
            ser3.write(sdata.encode('utf-8'))
            print('left\n')

        elif (sign_right==True):
            sdata='right'+'\n'
            ser3.write(sdata.encode('utf-8'))
            print('right\n')

        elif(sign_stop==True):
            sdata='stop'+'\n'
            ser3.write(sdata.encode('utf-8'))
            A+=1
            print(A)
            
        else:
            break
            

           
            
        conn.close()
        
##########################################################




#####################예으함수############################

#For Serial
ser=serial.Serial('/dev/ttyUSB0',115200)

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

###For GPIO
##GPIO.setwarnings(False)
##GPIO.cleanup()
##GPIO.setmode(GPIO.BCM)
##laser=4
##BUZ=15
##ON=1
##OFF=0
##
###GPIO.setup(laser, GPIO.OUT)
###GPIO.setup(BUZ,GPIO.OUT)
###ck_pwm=GPIO.PWM(BUZ,1000)

#For Culculate
pp1=300; pp2=100  ##$$$$$$$
pre_pan=0; pre_tilt=0
q=0


    
def CamshiftTracking():
    global frame, trackWindow, roi_hist
    global cxTest, cyTest
    global x,y,h,w
    global pan, tilt
    global A #A 는 연수와 나의연결고리
    
    first=0
    

    #SelectObject()

    try:
        cap=cv2.VideoCapture(0)
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

        while first==10:
            first+=1
            


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
            

            
            #outline=np.int0(cnt)
            #print(cnt)

            #frame에 contours를 그린다.
            cv2.drawContours(frame,[cnt],0,green,2)

            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),red,2)##


        #print('Just',pts[0,0])
        #print(pts)
        #cv2.circle(frame, (pts[0]),5, (0,0,255), 2)
        

        cv2.imshow('frame',frame)
        
        #모터를 돌리는 코드
        
        pp1,pp2=choice_where(x,y,w,h)
        print (pp1,pp2)
        pan, tilt=pixcel_to_world(pp1,pp2)
        
        if ((A%2)==1):
            motor(pan, tilt)
        #print(pan,tilt)
        #print('*\n')
        ##motor(pan, tilt)


        k=cv2.waitKey(60)&0xFF
        if k==27:
            cap.release()
            cv2.destroyAllWindows()  
            break

def choice_where(x,y,w,h):
        global pp1,pp2, q#iiiiiiiiiiii
        #print(p1[0],(p1[0]+p2[0]))
        #print(p1[1],p1[1] + p2[1])
        #print(p1[0],p2[0])
        #print(p1[1],p2[1])
        if int(x)-100<pp1<int(x+w)+100 and int(y)-100<pp2<int(y+h)+100:
                print ('success')
                #ck_pwm.start(50)
                #time.sleep(0.3)
                #ck_pwm.stop()
                #GPIO.output(laser,False)
                
                x=[0,300,100,300,200,100] #@@@@@@@@@@@@@@@
                y=[60,20,30,10,30,50]
                
                pp1=x[q]
                pp2=y[q]
                q=q+1
                if q==6:
                    q=0
                
        return pp1,pp2




def pixcel_to_world(pp1,pp2):
    global pan, tilt
    wx=(-0.1156)*pp1+36.075; wy=(-0.4276)*pp2+177.88#구해진 현실좌표
    #print('pixel location:',pp1,',',pp2)
    #print('world location:',wx,',',wy)

    pan= math.atan(wx/(wy+3))*180/math.pi #수직, 좌우
    tilt= math.atan(25/(math.sqrt((wx**2)+((wy+3)**2))))*180/math.pi
    #print(pan,tilt)
    return pan, tilt


def motor(pan, tilt):
        global pre_pan, pre_tilt
        if (pan!=pre_pan and tilt!=pre_tilt):
                pre_pan=pan; pre_tilt=tilt
                pan2=int(pan); tilt2=int(tilt)
               # print(pan, tilt)
                #print(pan2,tilt2)

                

                if(pan2<0):
                        pan2=-pan2
                        if pan2<10:
                                a='-'+'0'+str(pan2)
                        else:
                                a='-'+str(pan2)
                                
                else:
                        if pan2<10:
                                a='+'+'0'+str(pan2)
                        else:
                                a='+'+str(pan2)
                        

                if(tilt2<0):
                        tilt2=-tilt2
                        if tilt2<10:
                        
                                b='-'+'0'+str(tilt2)
                        else:
                                b='-'+str(tilt2)
                else:
                        if tilt2<10:
                        
                                b='+'+'0'+str(tilt2)
                        else:
                                b='+'+str(tilt2)

                sdata='@'+a+b+'\n'
                ser.write(sdata.encode('utf-8'))
                #print(a,b)
                #print(sdata)
                time.sleep(5)
