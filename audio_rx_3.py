# importing os module 
import os 
  
# Command to execute
# Using Windows OS command
cmd = "cvlc -vvv alsa://plughw:1 --sout '#transcode{acodec=mp3,ab=16,channels=1,scodec=none}:standard{access=http,dst=0.0.0.0:8888/out.mp3}'"

os.system(cmd)
