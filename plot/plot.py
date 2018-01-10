import sys
import time
from datetime import datetime
import calendar
import matplotlib.pyplot as plt 
import MySQLdb
import numpy as np

def timeConvert(indate):
    dt=datetime.strptime(indate,"%Y-%m-%d %H:%M:%S")
    dt_now=datetime.now()
    dt=dt.replace(year=dt_now.year,month=dt_now.month,day=dt_now.day)
    t1=calendar.timegm(dt.utctimetuple())
    return t1
    
def dataXY(record,basetime,t,s):
    oneM=1000000
    indate=record[1]
    relativetime=timeConvert(indate)-basetime
   # print ("relativetime %d",relativetime)
    t.append(relativetime)
    s.append((record[2]+record[3])/(oneM*1.0))
def excuteSql(sql,conn):
    #print sql
    cursor=conn.cursor()
    cursor.execute(sql)
    return cursor
def cumulation_func(record,basetime,t_cumulation,cumulation,accum):
    kb=1000*8  #bits
    indate=record[1]
    relativetime=timeConvert(indate)-basetime
    t_cumulation.append(relativetime)
    acc=((record[2]+record[3])/kb)*3+accum
    cumulation.append(acc)	   #unit is bits
    return acc
    
    
t=[]
s=[]
t1=[]
s1=[]
t_cumulation=[]
cumulation=[]     #here only record the cumulation of migration src host
accum=0
SMALL_SIZE=15
MEDIUM_SIZE=20
BIGGER_SIZE=25
titleName=sys.argv[3]+"-"+sys.argv[4]+" "+sys.argv[5]+"s"
conn=MySQLdb.connect(user="root",passwd="",db="SDN",unix_socket="/opt/lampp/var/mysql/mysql.sock") 
for j in range(len(sys.argv)-4):
    sql='SELECT * FROM %s' % sys.argv[j+1]
    cursor=excuteSql(sql,conn)
    rowNum=cursor.rowcount
    rec=cursor.fetchone()
    basetime=timeConvert(rec[1])
    if j == 0:
           dataXY(rec,basetime,t,s)
           t_cumulation.append(0)
           cumulation.append(0)

    else:
           dataXY(rec,basetime,t1,s1)  
   # print basetime
    for i in range(rowNum-1):
        record=cursor.fetchone()
        if j == 0:
           dataXY(record,basetime,t,s)
           acc=cumulation_func(record,basetime,t_cumulation,cumulation,accum)
           accum=acc
        else:
           dataXY(record,basetime,t1,s1)
f=open("cumulation.txt","w")
for i in range(len(t_cumulation)):
    f.write('%d %d\n' %(t_cumulation[i],cumulation[i]))
plt.rc('axes',labelsize=BIGGER_SIZE)
plt.rc('legend',fontsize=MEDIUM_SIZE)
plt.rc('xtick',labelsize=MEDIUM_SIZE)
plt.rc('ytick',labelsize=MEDIUM_SIZE)
#plt.rc('figure',titlesize=BIGGER_SIZE)
lines=plt.plot(t,s,'-r',t1,s1,'--b')
plt.setp(lines,linewidth=2.0)
plt.axis([min(t),250,min(s),max(s)])
#plt.xticks(np.arange(min(t),250,50.0))
plt.xticks([10,50,100,150,200,250])
plt.legend(['source host','destination host'],loc='upper right')
plt.xlabel("time(s)")
plt.ylabel("bandwidth consumption(Mbps)")
plt.suptitle("random policy",fontsize=BIGGER_SIZE)
#plt.suptitle(titleName,fontsize=BIGGER_SIZE)
plt.savefig(titleName+".png",bbox_inches='tight')
plt.show()
plt.clf()
plt.xlabel("time(s)")
plt.ylabel("cumulation throughput(kb)")
plt.plot(t_cumulation,cumulation,"-b")
plt.setp(lines,linewidth=3.0)
plt.savefig(titleName+"_cumulation.png",bbox_inches='tight')
f.close()
plt.show()


    
