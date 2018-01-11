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
    fp=open(path,'r')
    for line in fp:
        #print line
        Matrix.append(line)
    fp.close()
    return Matrix

def calculateConfidenceInterval(Matrix,SAMPLE_SIZE):
        sample=np.array(Matrix).astype(np.int)
	sample_mean=sample.mean()
        z_critical=stats.norm.ppf(q=0.95)
        stdev=sample.std()
        margin_of_error=z_critical*(stdev/math.sqrt(SAMPLE_SIZE))
	print margin_of_error
        confidence_interval=(sample_mean-margin_of_error,sample_mean+margin_of_error)
        return sample_mean,confidence_interval

def doplot(sample_means,intervals):
	SMALL_SIZE=15
	MEDIUM_SIZE=20
	BIGGER_SIZE=25
	lineformat=['bs','or','g^']
	fig=plt.figure()
	ax=fig.add_subplot(111)
	ax.xaxis.set_ticks(np.arange(50,250,50))
	ax.set_xlabel('time(s)',fontsize=BIGGER_SIZE)
	ax.set_ylabel('cumulation throughput(kb)',fontsize=BIGGER_SIZE)
        ax.set_ylim(ymin=0,ymax=45)
	ax.set_xlim(xmin=0,xmax=20)
	ax.tick_params(labelsize=MEDIUM_SIZE)
	for i in range(0,len(sample_means)):
		 ax.errorbar(x=np.arange(0,SAMPLE_SIZE,5),
                 y=sample_means[i],
	         yerr=[(top-bot)/2 for top,bot in intervals[i]],
	         fmt=lineformat[i])
	ax.legend(['bandwidth','shortest path','random'],loc='upper left',fontsize=MEDIUM_SIZE)
	plt.show()
	fig.savefig("combine-cumulation.png",bbox_inches='tight')
       
         

SAMPLE_SIZE=20
paths=[]
sample_means=[]
intervals=[]
paths.append("2-3.txt")
paths.append("2-4.txt")
paths.append("2-5.txt")
w=SAMPLE_SIZE
#setpltformat()
for path in paths:
    Matrix=[]
    Matrix=readfile(path,Matrix)   
    sample_mean,interval=calculateConfidenceInterval(Matrix,SAMPLE_SIZE)
    print path
    print sample_mean
    print interval
    '''
    sample_means.append(sample_mean)
    intervals.append(interval)
    doplot(sample_means,intervals)
    '''
'''
for interval in intervals:
      #  print Matrix[i] 
	print interval
'''

                       
