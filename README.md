# Demo audio process

## 几个示例
- demo_pyaudio.py 播放音频文件
- demo_video.py 接收rtsp视频流
- demo_audio.py 接收rtsp音频流，并进行转码等处理

## Play pcm
```
ffplay -f s16le -ar 16k -ac 1 raw_16k_16bits.pcm
```

## Convert pcm to wav
```
ffmpeg -f s16le -ar 16k -ac 1 -i raw_16k_16bits.pcm raw_16k_16bits.wav     
```
 
## Library for manipulating wave and pcm/raw file
- audioop: manipulate raw audio data
- wave: read and write WAV files

## Libary for manipulating rstp
- ffmpeg-python
