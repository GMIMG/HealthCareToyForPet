#+00+00 앞 00은 pan(아래,좌우), 뒤 00은 tilt(위,상하)이며 +,-는 방향을 나타낸다. 


import serial
import time
ser=serial.Serial('/dev/ttyUSB0', 115200) #아두이노 연결선에 맞춰서 바꿀것.
sdata=' '+'\n'
ser.write(sdata.encode('utf-8'))
sdata='stop'+'\n'
ser.write(sdata.encode('utf-8'))

while ser.isOpen():
    while(True):
        for i in range(0,5):
        
            #a= [20,50,70,10,90]
            #b= [30,20,10,70,90]
            a=input('angle')
            sdata='@'+a+'\n' #'@'+
            #-90+90
            ser.write(sdata.encode('utf-8'))    
            #print (sdata.decode('utf-8'))
            time.sleep(0.5)

    ser.close()
    pass
