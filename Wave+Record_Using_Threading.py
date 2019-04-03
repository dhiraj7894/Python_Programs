import pyaudio #importing PyAudio
import struct #importing Struct
import numpy as np #importing numpy
import matplotlib.pyplot as plt #importing matplotlib for ploting graphs
import pandas as pd #import pandas
import wave
import multiprocessing as mltp
import time

CHUNK = 500 * 2 
FORMAT = pyaudio.paInt16
RATE = 44100

RECORD_SECONDS = 1


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
    
        file = open("Auidio_1","a")
        file.writelines(aS)
    
        line.set_ydata(data_int)
        fig.canvas.draw()
        fig.canvas.flush_events()
        
def task2():
    CHANNELS = 2
    
    WAVE_OUTPUT_FILENAME = "file_1.wav"
 
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

if __name__ == "__main__":
    t1 =mltp.Process(target = task1)
    t2 =mltp.Process(target = task2)
    t1.start()
    t2.start()
    t = RECORD_SECONDS
    while t >= 0:
        print(t, end='...')
        time.sleep(1)
        t -= 1
        if t == 0:
            t1.terminate()
            return True 
    t1.join()
    t2.join()
print("Done")
