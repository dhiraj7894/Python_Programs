import pyaudio #importing 
import struct #importing Struct
import numpy as np #importing numpy
import matplotlib.pyplot as plt #importing matplotlib for ploting graphs
import pandas as pd #import pandas
import wave
import threading

%matplotlib tk
def task1():
    CHUNK = 500 * 2 
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
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
    
        file = open("Auidio","a")
        file.writelines(aS)
    
        line.set_ydata(data_int)
        fig.canvas.draw()
        fig.canvas.flush_events()
        
def task2():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 500 * 2
    RECORD_SECONDS = 15
    WAVE_OUTPUT_FILENAME = "file.wav"
 
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
    t1 = threading.Thread(target = task1)
    t2 = threading.Thread(target = task2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("Done")
