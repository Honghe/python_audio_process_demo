import json
import logging
import subprocess

import ffmpeg
from flask import Flask, request

app = Flask(__name__)


def save_mp3_to_wav(file):
    """ Convert Flask mp3 file to wav and save
    Flask request.file is wrap request.file.stream
    And request.file.stream ia type: tempfile.SpooledTemporaryFile
    tempfile.SpooledTemporaryFile: Temporary file wrapper, specialized to switch from BytesIO \
    or StringIO to a real file when it exceeds a certain size or when a fileno is needed.
    :param file:
    :return:
    """
    f_path = 'upload_file.wav'
    stream = ffmpeg.input('pipe:0')
    stream = ffmpeg.output(stream, f_path, acodec='pcm_s16le', ac=1, ar='16k')
    # TODO, prompt and log when overwrite
    stream = ffmpeg.overwrite_output(stream)
    # call ffmpeg manually (i.e. p = subprocess.Popen(stream.compile(), stdin=subprocess.PIPE)),
    # use stdin as input in ffmpeg (use pipe:0 as the file name, see [this](https://ffmpeg.org/ffmpeg-protocols.html#pipe))
    
    # stream.compile() Build command-line for invoking ffmpeg.
    # subprocess.Popen() Execute a child program in a new process
    p = subprocess.Popen(stream.compile(), stdin=subprocess.PIPE)
    CHUNK_SIZE = 1024
    data = file.read(CHUNK_SIZE)
    while data:
        p.stdin.write(data)
        data = file.read(CHUNK_SIZE)


@app.route("/", methods=['POST', 'GET'])
def save_and_verification_audio():
    if request.method == 'GET':
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=text name=id value="bala">
          <input type=submit value=Upload>
        </form>
        '''

    task_id = request.form['id']
    # get file
    file = request.files['file']
    filename = file.filename
    save_mp3_to_wav(file)
    logging.info('save file: {}'.format(json.dumps({'filename': filename, 'task_id': task_id}, ensure_ascii=False)))
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True)
