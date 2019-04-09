# -*- coding: utf-8 -*-
import logging

import pyaudio
import wave

chunk = 1024
logging.basicConfig(level=logging.DEBUG)

wf = wave.open('./data/raw_16k_16bits.wav', 'rb')

p = pyaudio.PyAudio()

# 打开声音输出流
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# 写声音输出流进行播放
while True:
    data = wf.readframes(chunk)
    if data == "": break
    stream.write(data)

stream.close()
p.terminate()
