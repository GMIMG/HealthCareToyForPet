import MySQLdb, datetime, time
db='pid'
table1='sen'
now=datetime.datetime.now()
d=now.strftime('%Y-%m-%d')
t=now.strftime('%H:%M:%S')
[year,mon,date]=[int(i) for i in d.split('-')]
[hour,mini,sec]=[int(i) for i in t.split(':')]
sqldata=((1,year,mon,day,hour,mini,sec,50))
conn=MySQLdb.connect(host='localhost',user='pi',passwd='1234',db='pid')        
try:
    cur=conn.cursor()
    #insert data
    sql='INSERT INTO sen VALUES (%s,%s,%s,%s,%s,%s,%s,%s);'

    cur.execute(sql,sqldata)
    #transaction
    conn.commit()

    #for print
    sqls='SELECT * FROM {};'.format(table1)
    cur.execute(sqls)
    print(cur.fetchall())
except:
    conn.rollback()
finally:
    cur.close
    conn.close
