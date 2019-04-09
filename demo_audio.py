import logging
import os

import ffmpeg
import pyaudio

logging.basicConfig(level=logging.DEBUG)

filename = 'data/demo.mp4'


def demo_simple_subprocess():
    host = '172.31.23.124'
    stream = '2'
    out, _ = (
        ffmpeg
            .input('rtsp://' + host + '/' + stream)
            # 将音频转码为 sample rate 16k, 16 bits, one channel的pcm格式
            # 直接保存至文件
            .output('rtsp_audio.pcm', format='s16le', acodec='pcm_s16le', ac=1, ar='16k')
            .overwrite_output()
            .run(capture_stdout=True)
    )


def demo_extract_audio():
    host = '172.31.23.124'
    stream = '2'
    stream = ffmpeg.input('rtsp://' + host + '/' + stream)
    stream = stream['a']
    # 只抽出MPEG-4 AAC音频不转码
    stream = ffmpeg.output(stream, 'out/rtsp_audio.mp4', strict='-2')
    # 直接覆盖同名文件不询问
    stream = ffmpeg.overwrite_output(stream)
    stream.run(capture_stdout=True)


# 使用子进程方式，中间可以进行音频处理
def demo_subprocess():
    host = '172.31.23.124'
    stream = '2'
    packet_size = 1024

    # 子进程
    process = (
        ffmpeg
            .input('rtsp://' + host + '/' + stream)['a']  # ['a']抽出音频流
            # .input(filename)  # 源是文件
            .filter('volume', 1)  # 放大
            # '-'将流输出至标准输出
            .output('-', format='s16le', acodec='pcm_s16le', ac=1, ar='16k')
            # .overwrite_output()
            # 将子进程的标准输出由管道转出
            .run_async(pipe_stdout=True)
    )

    class PCMSaver:
        def __init__(self, file_name):
            out_path = './out'
            os.makedirs(out_path, exist_ok=True)
            self.file_path = os.path.join(out_path, file_name)

        def _write(self, data):
            with open(self.file_path, 'ab') as f:
                f.write(data)
                f.close()

        def write(self, data):
            # TODO a separated process worker to safely write file.
            self._write(data)

    # 打开声音输出流
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    output=True)
    # 保存声音至文件
    pcm_saver = PCMSaver('audio_output.pcm')

    # 写声音输出流进行播放
    while process.poll() is None:
        packet = process.stdout.read(packet_size)
        if packet == "":
            break
        # 播放
        stream.write(packet)
        # 保存至文件
        pcm_saver.write(packet)


if __name__ == '__main__':
    # demo_subprocess()
    # demo_simple_subprocess()
    demo_extract_audio()
