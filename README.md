# html_mic_streaming
This repository will have the code to stream browser microphone to server.<br>
Reseving the stream using VLC

    using vlc  http://localhost:8888/out.mp3

Transmitting the stream using VLC<br>
Finding input device 
    
    arecord -l
    
   **** List of CAPTURE Hardware Devices ****
   card 1: PCH [HDA Intel PCH], device 0: ALC3226 Analog [ALC3226 Analog]
   Subdevices: 0/1
   Subdevice #0: subdevice #0

As seen above the Card 1   =   alsa://plughw:1  in the link below
This command will send the microphone audio from interface plughw:1

    cvlc -vvv alsa://plughw:1 --sout '#transcode{acodec=mp3,ab=16,channels=1,scodec=none}:standard{access=http,dst=0.0.0.0:8888/out.mp3}'

Python exsample from html to server

    
    
