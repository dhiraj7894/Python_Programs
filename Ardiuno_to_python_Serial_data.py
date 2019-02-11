import serial                                                           #To import serial lib
import numpy as np                                                      #import numpy
import matplotlib.pyplot as plt                                         #import matplotlib
from drawnow import*                                                    #import new lib drawnow
import pandas as pd                                                     #import pandas
import time                                                             #importing Time modual

%matplotlib tk  

aD = serial.Serial('/dev/ttyACM0',9600)
tmpF = [] 
L = []
plt.ion()
cnt = 0

def plotVal():
    plt.plot(tmpF, 'rx-', label = 'Temperature')
    #plt.plot(L)
    plt.title('Serial temperature from Arduino')
    plt.grid(True)
    plt.ylabel('Temperature')
    #plt.plot(tmpF, 'rx-', labl = 'values')
    plt.legend(loc = 'upper right')
    
    
while True:
    while(aD.inWaiting()==0):
        pass
    #aD.flushInput()
    aS = aD.readline()[:].decode('ascii')
    time.sleep(1)
    dataArray = aS.split(' ')
    tmp = dataArray[0]
    LED = dataArray[1]
    x = dataArray[2]
    y = dataArray[3]
    z = float(dataArray[4])
    tmpF.append(tmp)
    L.append(LED)
    df = pd.DataFrame(tmpF)
    df.to_csv('/home/makerghat/Anaconda/Temprature.csv')
    drawnow(plotVal)
    cnt = cnt+1
    if (cnt > 50):
        tmpF.pop(0)
        L.pop(0)
    print(tmp, LED, x, y, z)
