# html_mic_streaming
This repository will have the code to stream browser microphone to server.<br>
Reseving the stream using VLC

    using vlc  http://localhost:8888/out.mp3

Transmitting the stream using VLC

    cvlc -vvv alsa://plughw:0 --sout '#transcode{acodec=mp3,ab=16,channels=1,scodec=none}:standard{access=http,dst=0.0.0.0:8888/out.mp3}'

Python exsample from html to server

    
    
