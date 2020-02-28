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

pan=0
tilt=0





#####################연수 함수############################

##logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s', )
ser3=serial.Serial('/dev/ttyUSB0',115200)

def client():
    global pan,tilt
##    HOST='192.168.0.200'
##    PORT=8888
##
##    s=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
##    s.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
##    s.bind((HOST,PORT))
##    while (1):
##        print(pan,tilt)

##    while (True):
##        s.listen(2)                             ##연결될 때까지 듣는중
##        conn, addr = s.accept()
##        print('connected by : ',addr)
##
##        data = conn.recv(1024)                  ##client에서 받음
##        data_decode=data.decode('utf-8')
##        ##print(data_decode)
##        ##print('\n')
##            
##        sign_up=data_decode.endswith("up")
##        sign_down=data_decode.endswith("down")
##        sign_left=data_decode.endswith("left")
##        sign_right=data_decode.endswith("right")
##        sign_break=data_decode.endswith("break")
##    conn.close()
        
##########################################################




#####################예으함수############################

#For Serial
ser2=serial.Serial('/dev/ttyUSB0',115200)

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
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
fgbg = cv2.createBackgroundSubtractorMOG2()


#For Culculate
pp1=500; pp2=620
pre_pan=0; pre_tilt=0

def SelectObject():
    global cx,cy, frame, col, width, row, height
    global rectangle, roi_hist, trackWindow
    global cxTest, cyTest
    try:
        cap=cv2.VideoCapture(0)
        cap.set(3,1280)
        cap.set(4,720)
    except:
        print('카메라 구동실패.')
        return

    ret, frame=cap.read()
    #print(frame)
    
    for i in range(0,1):

        #frame를 변환하여 fgmask에 저장
        fgmask = fgbg.apply(frame)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        fgmask = cv2.GaussianBlur(fgmask, (101, 101), 0)
        #fgmask = cv2.blur(fgmask,(51,51),0)

        #fgmask 스케일을 threash를 통해 흑백으로 바꿈
        _,binary = cv2.threshold(fgmask,1,255,0)


        #contours 설정부분
        _,contours,_ = cv2.findContours(binary,1,2)
        if len(contours) > 0:
            pre_area=0
            for i in range(len(contours)):
                
                cnt = contours[i]
                perimeter = cv2.arcLength(cnt,True)
                M = cv2.moments(cnt)
                area=M['m00']
                if area != 0 and area>pre_area:
                    cx,cy = int(M['m10']/area),int(M['m01']/area)
                    pre_area=area


        col=cx-5; row=cy-5; x=cx+5; y=cy+5


        #cv2.rectangle(frame, (col, row), (x,y), green, -1)
        cv2.rectangle(frame, (339, 330), (360,351), green, -1)
        height,width=abs(row-y),abs(col-x)
        trackWindow=col,row,width,height
        roi=frame[row:row+height,col:col+width]
        roi=cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        roi_hist=cv2.calcHist([roi],[0],None,[180],[0,180])
        cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
        cxTest=cx;cyTest=cy
        #print(cxTest, cyTest)


    
    

    
def CamshiftTracking():
    global frame, trackWindow, roi_hist
    global cxTest, cyTest
    global p1,p2
    global pan,tilt

    SelectObject()

    try:
        cap=cv2.VideoCapture(0)
        cap.set(3,1280)
        cap.set(4,720)

    except:
        print('카메라가 인식이 안된대..')
        return



    termination=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,10,1)

    while True:
        ret, frame=cap.read()
        #print('sss')
        

        if not ret:
            break
        
    

        #print(trackWindow)
        
        

        if trackWindow is not None:
            


            hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            #cv2.imshow('hsv',hsv)
            #cv2.circle(frame,(cxTest,cyTest),5,green,-1)
            dst=cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
            ret, trackWindow=cv2.CamShift(dst, trackWindow, termination)
             
            #pts는 왼쪽위에 점부터 시계방향으로 np
            pts=cv2.boxPoints(ret)
            pts=np.int0(pts)
            cv2.polylines(frame, [pts], True, (0,255,0),2)
            #p1=np.array([300, 300])
            #cv2.rectangle(frame, (pts[0,0],pts[0,1]),( pts[2,0],pts[2,1]), (0,0,255), -1)

            #p1, p2 결정.
            p1= (pts[0,0],pts[0,1])
            p2= (pts[2,0],pts[2,1])

            #print('Just',pts[0,0])
            #print(pts)
            #cv2.circle(frame, (pts[0]),5, (0,0,255), 2)
            

            cv2.imshow('frame',frame)
            
            #모터를 돌리는 코드   
            pp1,pp2=choice_where()
            ##print (pp1,pp2)
            pan, tilt=pixcel_to_world(pp1,pp2)
            motor(pan, tilt)


            k=cv2.waitKey(60)&0xFF
            if k==27:
                cap.release()
                cv2.destroyAllWindows()  
                break

def choice_where():
        global pp1,pp2
        global p1, p2
        if int(p1[0])-50<pp1<int(p1[0]+p2[0])+50 and int(p1[1])-50<pp2<int(p1[1] + p2[1])+50:
                ##print ('success')
                #ck_pwm.start(50)
                #time.sleep(0.3)
                #ck_pwm.stop()
                #GPIO.output(laser,False)
                x=random.randrange(400,800)
                y=random.randrange(600,630)
                pp1=x
                pp2=y    
        return pp1,pp2




def pixcel_to_world(pp1,pp2):
    wx=(0.0223*pp1-15.149)*2.5; wy=(-0.0678*pp2+48.793)*2.5+20 #구해진 현실좌표 얼추맞아.
    

    pan= math.atan(wx/25)*180/math.pi #수직, 좌우
    tilt= math.atan(25/(math.sqrt((wx**2)+((wy-10)**2))))*180/math.pi
    print(pan,tilt)
    return pan, tilt


def motor(pan, tilt):
        global pre_pan, pre_tilt
        if (pan!=pre_pan and tilt!=pre_tilt):
                pre_pan=pan; pre_tilt=tilt
                pan2=int(pan); tilt2=int(tilt)
                print(pan, tilt)
                print(pan2,tilt2)

                if(pan2<0):
                        a='-'+str(pan2)
                else:
                        a='+'+str(pan2)

                if(tilt2<0):
                        b='-'+str(tilt2)
                else:
                        b='+'+str(tilt2)

                sdata='@'+a+b+'\n'
                ser2.write(sdata.encode('utf-8'))
                print(a,b)
                print(sdata)


