import cv2
import numpy as np



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


    
    

    
def CmashiftTracking():
    global frame, trackWindow, roi_hist
    global cxTest, cyTest

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
            p1=np.array([300, 300])
            cv2.rectangle(frame, (pts[0,0],pts[0,1]),( pts[2,0],pts[2,1]), (0,0,255), -1)
            #print('Just',pts[0,0])

            #print(pts)
            
            #cv2.circle(frame, (pts[0]),5, (0,0,255), 2)
            

            cv2.imshow('frame',frame)

        k=cv2.waitKey(60)&0xFF
        if k==27:
            cap.release()
            cv2.destroyAllWindows()  
            break








CmashiftTracking()
quit()

