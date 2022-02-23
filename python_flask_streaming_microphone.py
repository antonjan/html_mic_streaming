from flask import Flask, Response,render_template, request
import pyaudio
import re

app = Flask(__name__)

def genHeader(sampleRate, bitsPerSample, channels, samples):
    datasize = 10240000 # Some veeery big number here instead of: #samples * channels * bitsPerSample // 8
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o

FORMAT = pyaudio.paInt16
CHUNK = 1024 #1024
RATE = 44100
bitsPerSample = 16 #16
CHANNELS = 1
wav_header = genHeader(RATE, bitsPerSample, CHANNELS, CHUNK)

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
    rate=RATE, input=True, input_device_index=1,
    frames_per_buffer=CHUNK)

@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response

@app.route('/audio.wav')
def audio():
    range_header = request.headers.get('Range', None)
    print(range_header)
    byte1, byte2 = 0, None
    if range_header:
        match = re.search(r'(\d+)-(\d*)', range_header)
        groups = match.groups()

        if groups[0]:
            byte1 = int(groups[0])
        if groups[1]:
            byte2 = int(groups[1])
        print(str(byte1) + " " + str(byte2))
            
    # sound
    def sound():
        data = wav_header
        data += stream.read(CHUNK)
        yield(data)
        while True:
            data = stream.read(CHUNK)
            yield(data)
    resp = Response(sound(), mimetype="audio/x-wav")
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True,port=5000)

