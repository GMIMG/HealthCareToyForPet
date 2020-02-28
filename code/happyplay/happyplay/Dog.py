import serial, datetime, time, threading, MySQLdb



#####Seiral thread function#####

def dataGetherSend():
        ######serial setting######
    
    act=0
    old_act=0
    module=0
    now=datetime.datetime.now()
    old_hour=int(now.strftime('%H'))
    

    db='pid'
    table1='sen'
    #table1=input('tablesname(default:sen): ')
    if table1=='':
        table1='sen'


    while 1:
        try:
            ser1 = serial.Serial(port='/dev/ttyS0',
            baudrate = 115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=None)
            x=ser1.readline()
            x=x.decode()
            print(x)
            rcvdata=x.split('=')
            module=int(rcvdata[0])
            act=float(rcvdata[1])
            ser1.close()
        except:
            if ser1.isOpen():
                ser1.close()
            pass

        #NowTimeSave
        now=datetime.datetime.now()
        d=now.strftime('%Y-%m-%d')
        t=now.strftime('%H:%M:%S')
        [year,mon,date]=[int(i) for i in d.split('-')]
        [hour,mini,sec]=[int(i) for i in t.split(':')]


        #change time
        if(old_hour != hour):
            old_act=act
        old_hour=hour
        send_data=act-old_act
        #play
        if(hour==13 and mini==0):
            if(act<500):
                play=1
            send_data=0
            act=0

        if(hour==21 and mini==0 and nowdata < 500):
            if(act<500):
                play=1
            send_data=0
            act=0

        if(hour==7 and mini==0):
            send_data=0
            act=0

            
        #serial_read
        sqldata=((module,year,mon,date,hour,mini,sec,send_data))
        #print(sqldata)
        #sqldata=((1,2018,2,26,15,30,30,7))


        #database connect
        conn=MySQLdb.connect(host='localhost',user='pi',passwd='1234',db='pid')        
        try:
            cur=conn.cursor()
            #insert data
            sql='INSERT INTO sen VALUES (%s,%s,%s,%s,%s,%s,%s,%s);'
            sql2='UPDATE sum SET sumact = {};'.format(act)
            cur.execute(sql,sqldata)
            #transaction
            conn.commit()
            cur.execute(sql2)
            conn.commit()
            #for print
            #sqls='SELECT * FROM {};'.format(table1)
            #cur.execute(sqls)
            #print(cur.fetchall())
        except:
            conn.rollback()
        finally:
            cur.close
            conn.close



########################################################
            
#dataGS=threading.Thread(target=dataGetherSend)
#dataGS.start()


