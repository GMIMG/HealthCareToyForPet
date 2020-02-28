import numpy as np
import cv2
import numpy as np  
import time
import math
import RPi.GPIO as GPIO
import random


#pantilt, laser GPIO설정.
GPIO.setwarnings(False)
pinpan=2 # pwm pin num 2 좌우
pintilt=3
laser=4

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

GPIO.setup(pinpan, GPIO.OUT)
GPIO.setup(pintilt, GPIO.OUT)
GPIO.setup(laser, GPIO.OUT)

pl2=GPIO.PWM(pinpan,50)
pl3=GPIO.PWM(pintilt,50)

pl2.start(0)
pl3.start(0)


#tracking을 보여주는 사각형 변수초기화.
col, width, row, height =-1, -1, -1, -1
frame=None
frame2=None
inputmode=False
rectangle=False
trackWindow=None
roi_hist=None


#fps를 계산하기 위한 변수.
prevTime=0

#현실좌표의 초기값.
pp1=500; pp2=620

def choice_where(): #레이저의 픽셀좌표와 개의 tracking할때의 픽셀 좌표가 같은가?
    global pp1
    global pp2
    global x1, y1
    
    if (col)-100<pp1<(row)+100 and (x1)-50<pp2<(y1)+50:
        print ('success')
        GPIO.output(laser,False)
        a=random.randrange(400,600)
        b=random.randrange(600,650)
        pp1=a
        pp2=b    

    return pp1,pp2

    
def pixcel_to_world(pp1,pp2): #픽셀좌표에 맞게 각도를 계산해주는 함수
        
    wx=(0.0223*pp1-15.149)*2.5; wy=(-0.0678*pp2+48.793)*2.5+20 #구해진 현실좌표 얼추맞아.
    print('pixel location:',pp1,',',pp2)
    print('world location:',wx,',',wy)
    
    pan= math.atan(wx/25)*180/math.pi #수직, 좌우
    tilt= math.atan(25/(math.sqrt((wx**2)+((wy-10)**2))))*180/math.pi
    #print(pan,tilt)
    return pan, tilt




def motor(pan, tilt): #각도에 맞게 모터를 돌리는 함수.
    pl2.ChangeDutyCycle(4.5-pan*9/180) 
    #print ("angle pan :",4.5-pan*10/180)
    
    pl3.ChangeDutyCycle(tilt*5/90)
    #print ("angle tilt:",tilt*10/180)


#tracking 대상을 선택하는함수.
    
def onMouse(event, x, y, flags, param):
    global col, width, row, height, frame, frame2, inputmode
    global rectangle, roi_hist, trackWindow
    global x1,y1

    if inputmode:
        if event==cv2.EVENT_LBUTTONDOWN:
            rectangle=True
            col, row=x,y
            x1=x; y1=y

        elif event==cv2.EVENT_MOUSEMOVE:
            if rectangle:
                frame=frame2.copy()
                cv2.rectangle(frame, (col,row),(x,y),(0,255,0),2)
                x1=x; y1=y
                cv2.imshow('frame',frame)


        elif event==cv2.EVENT_LBUTTONUP:
            inputmode=False
            rectangle=False
            cv2.rectangle(frame,(col,row),(x,y),(0,255,0),2)
            x1=x; y1=y
            print(col,row,x,y)
            height,width=abs(row-y),abs(col-x)
            trackWindow=col,row,width,height
            roi=frame[row:row+height,col:col+width]
            roi=cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            roi_hist=cv2.calcHist([roi],[0],None,[180],[0,180])
            cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
            
    return



def camShift():
    global frame, frame2, inputmode, trackWindow, roi_hist, out

    try:
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)
    except:
        print('카메라 구동실패.')
        return

    ret, frame=cap.read()
    frame=cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA) #프레임줄이기2.

    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', onMouse, param=(frame, frame2))

    termination=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,10,1)
    



    while True:
        global pp1,pp2 
        global prevTime
        ret, frame=cap.read()
        frame=cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA) #프레임줄이기2.
        
        if not ret:
            break

        

        if trackWindow is not None:
            hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            dst=cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
            ret, trackWindow=cv2.CamShift(dst, trackWindow, termination)

            pts=cv2.boxPoints(ret)
            pts=np.int0(pts)
            cv2.polylines(frame, [pts], True, (0,255,0),2)


       
        #시간알리는코드.
        curTime=time.time()
        
        sec=curTime-prevTime
        prevTime=curTime
        fps=1/(sec)


        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50,170,50), 2);

        cv2.imshow('frame',frame) #프레임을보여줫~~

        #뭐..여러가지일을하는애들..프레임다음에 넣어주면 된다.
        GPIO.output(laser,True)
        pp1,pp2=choice_where()
        #print (pp1,pp2)
        pan, tilt=pixcel_to_world(pp1,pp2)
        motor(pan, tilt)
        

        k=cv2.waitKey(60)&0xFF
        if k==27:
            break

        elif k==ord('i'):
            print('Select Area for CamShift and Enter a Key')
            inputmode=True
            frame2=frame.copy()
            

            while inputmode:
                cv2.imshow('frame',frame)
                cv2.waitKey(0)

    cap.release()
    cv2.destroyAllWindows()


camShift()

