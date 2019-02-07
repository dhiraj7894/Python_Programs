import pyaudio #importing PyAudio
import struct #importing Struct
import numpy as np #importing numpy
import matplotlib.pyplot as plt #importing matplotlib for ploting graphs

%matplotlib tk

CHUNK = 1024 * 2 
FORMAT = pyaudio.paInt16
CHANNELS = 2
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
    line.set_ydata(data_int)
    fig.canvas.draw()
    fig.canvas.flush_events()
