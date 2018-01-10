import glob
import numpy as np
import scipy.stats as stats
import math
import matplotlib.pyplot as plt
#define a two dimention array, x is the filenumer 20 files, y is the time(interval is 3 seconds)
def setpltformat():
	SMALL_SIZE=15
	MEDIUM_SIZE=20
	BIGGER_SIZE=25
	plt.rc('axes',labelsize=BIGGER_SIZE)
	plt.rc('legend',fontsize=MEDIUM_SIZE)
	plt.rc('xtick',labelsize=MEDIUM_SIZE)
	plt.rc('ytick',labelsize=MEDIUM_SIZE)
	plt.xlabel("time(s)")
	plt.ylabel("cumulation throughput(kb)")
   
def readfile(path,Matrix):
    fileNum=0
    timeNum=0
    files=glob.glob(path)
    lastNum=0
    for f in files:
        fp=open(f,'r')
        for line in fp:
            #print line
            Matrix[fileNum][timeNum]=line.split()[1]
            lastNum=line.split()[1]
            timeNum +=1
            if timeNum==66:
                break
        while timeNum<66:	
			Matrix[fileNum][timeNum]=lastNum
			timeNum +=1
        fileNum +=1
        timeNum=0
        fp.close()
    return Matrix

def calculateConfidenceInterval(Matrix,SAMPLE_SIZE,FILE_SIZE):
    intervals=[]
    sample_means=[]
    for i in range(0,SAMPLE_SIZE):
	A=np.array(Matrix)
        sample=np.array(A[:,i]).astype(np.int)
        sample_mean=sample.mean()
        sample_means.append(sample_mean)
        z_critical=stats.norm.ppf(q=0.95)
        stdev=sample.std()
        margin_of_error=z_critical*(stdev/math.sqrt(FILE_SIZE))
        confidence_interval=(sample_mean-margin_of_error,sample_mean+margin_of_error)
        intervals.append(confidence_interval)
    return sample_means,intervals

def doplot(sample_means,intervals):
	SMALL_SIZE=15
	MEDIUM_SIZE=20
	BIGGER_SIZE=25
	lineformat=['bs','or','g^']
	fig=plt.figure()
	ax=fig.add_subplot(111)
	ax.set_xlabel('time(s)',fontsize=BIGGER_SIZE)
	ax.set_ylabel('cumulation throughput(kb)',fontsize=BIGGER_SIZE)
	ax.tick_params(labelsize=MEDIUM_SIZE)
	for i in range(0,len(sample_means)):
		 ax.errorbar(x=np.arange(0,SAMPLE_SIZE*3,3),
          y=sample_means[i],
	      yerr=[(top-bot)/2 for top,bot in intervals[i]],
	     fmt=lineformat[i])
	ax.legend(['bandwidth','shortest path','random'],loc='upper left',fontsize=MEDIUM_SIZE)
	plt.show()
	fig.savefig("combine-cumulation.png",bbox_inches='tight')
       
         
SAMPLE_INTERVAL=3
FILE_SIZE=20
SAMPLE_SIZE=66
paths=[]
sample_means=[]
intervals=[]
paths.append("bandwidth-cumulation/*.txt")
paths.append("shortestPath-cumulation/*.txt")
paths.append("random-cumulation/*.txt")
w,h=SAMPLE_SIZE,FILE_SIZE
#setpltformat()
for path in paths:
    Matrix=[[0 for x in range(w)] for y in range(h)]
    Matrix=readfile(path,Matrix)   
    sample_mean,interval=calculateConfidenceInterval(Matrix,SAMPLE_SIZE,FILE_SIZE)
    sample_means.append(sample_mean)
    intervals.append(interval)
    doplot(sample_means,intervals)
'''
for interval in intervals:
      #  print Matrix[i] 
	print interval
'''

                       
