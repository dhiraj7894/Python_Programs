import pyaudio #importing PyAudio
import struct #importing Struct
import numpy as np #importing numpy
import matplotlib.pyplot as plt #importing matplotlib for ploting graphs
import wave
import multiprocessing as mltp
import time
import serial 
from drawnow import*                                                    #import new lib drawnow
import pandas as pd                                                     #import pandas

CHUNK = 500 * 2 
FORMAT = pyaudio.paInt16
RATE = 44100 

RECORD_SECONDS = 50

aD = serial.Serial('/dev/ttyACM0',9600)
L = []
tmpF = []
aX = []
aY = []
aZ = []

plt.ion()
#cnt = 0

def task1():
    %matplotlib tk
    CHANNELS = 1
    p = pyaudio.PyAudio()
    steam = p.open(
        format = FORMAT,
        channels = CHANNELS,
        rate = RATE,
        input = True,
        output = True,
        frames_per_buffer=CHUNK
        )
    fig, ax =plt.subplots()
    x = np.arange(0, 2 * CHUNK, 2)
    line, =ax.plot(x,np.random.rand(CHUNK))
    ax.set_ylim(0,255)
    ax.set_xlim(0, CHUNK)

    while True:
        data = steam.read(CHUNK)
        data_int = np.array(struct.unpack(str(2*CHUNK)+'B',data),dtype = 'b')[::2]+128
        aS = str(data_int)
    
        file = open('/home/dhiraj_gt/SynthticSensor/Audio_wave_data.csv','a')
        file.writelines(aS)
    
        line.set_ydata(data_int)
        fig.canvas.draw()
        fig.canvas.flush_events()
        
def task2():
    CHANNELS = 2
    
    WAVE_OUTPUT_FILENAME = "/home/dhiraj_gt/SynthticSensor/Audio_in_MP3.wav"
 
    audio = pyaudio.PyAudio()
 
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print("recording...")
    frames = []
 
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording",)
    
 
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
 
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    
    
def task3():
    %matplotlib tk  
    def plotVal():
        plt.plot(tmpF, linestyle = ':' ,label = 'Temperature', color = "red", linewidth=3.5)
        plt.plot(L, linestyle = '--', label = 'Light Data', color = "green")
        plt.plot(aX, linestyle = '-.', label = 'Accelerometer X', color = "yellow")
        plt.plot(aY, linestyle = '-.', label = 'Accelerometer Y', color = "blue")
        plt.plot(aZ, linestyle = '-.', label = 'Accelerometer Z', color = "black")

        #plt.plot(L)
        plt.title('Serial Data from Arduino')

        plt.grid(True)
        plt.ylabel('Tempe, Ligh, X, Y, Z')
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
        z = dataArray[4]
        tmpF.append(tmp)
        L.append(LED)
        aX.append(x)
        aY.append(y)
        aZ.append(z)
        dfTmp = pd.DataFrame(tmpF)
        dfL = pd.DataFrame(L)
        dfAxyz = pd.DataFrame(aX, aY)

        dfTmp.to_csv('/home/dhiraj_gt/SynthticSensor/Temprature.csv')
        dfL.to_csv('/home/dhiraj_gt/SynthticSensor/Light.csv')
        dfAxyz.to_csv('/home/dhiraj_gt/SynthticSensor/Accelerometer.csv')
        drawnow(plotVal)
        '''cnt = cnt+1
        if (cnt > 50):
            tmpF.pop(0)
            L.pop(0)
            aX.pop(0)
            aY.pop(0)
            aZ.pop(0)'''

if __name__ == "__main__":
    t1 =mltp.Process(target = task1)
    t2 =mltp.Process(target = task2)
    t3 =mltp.Process(target = task3)
    t1.start()
    t2.start()
    t3.start()
    t = RECORD_SECONDS
    while t >= 0:
        print(t, end='...')
        time.sleep(1)
        t -= 1
        if t == 0:
            t1.terminate()
            t3.terminate()
    t1.join()
    t2.join()
    t3.join()
print(' \n Program worked successfully Done \n')
