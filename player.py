import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import sys
import time
import subprocess
from subprocess import check_output
import os
sw1_cnt=0
sw2_cnt=0
sw3_cnt=0
sw4_cnt=0

sw1=37
sw2=35
sw3=33
sw4=31

audio_mode=0
music_mode=0

light_mode1=0
light_mode2=0
light_mode3=0


def file_read(fname):
    content_array = []
    with open(fname) as f:
         for line in f:
             content_array.append(line)
         return(content_array)

def sw1_callback(channel):
    global sw1_cnt
    sw1_cnt=sw1_cnt+1
    print(str(sw1_cnt))

def sw2_callback(channel):
    global sw2_cnt
    sw2_cnt=sw2_cnt+1
#    print(str(sw2_cnt))

def sw3_callback(channel):
    global sw3_cnt
    sw3_cnt=sw3_cnt+1
    print("Button-3 was pushed :" + str(sw3_cnt))

def sw4_callback(channel):
    global sw4_cnt
    sw4_cnt=sw4_cnt+1
    print("Button-4 was pushed :" + str(sw4_cnt))

def audiobook_skip(aindex):
    global sw1_cnt
    sw1_cnt-=1
    print("Skip the file")
    #subprocess.call(['killall', 'mpg123'])

def music_skip(mindex):
    global sw1_cnt
    sw1_cnt-=1
    print("skip the track")

def album_skip(subindex,mindex):
    global sw1_cnt
    sw1_cnt-=2
    print("skip the alub")
    subindex+=1
    mindex=0

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(sw1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(sw2, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(sw3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(sw4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.add_event_detect(sw1,GPIO.RISING,callback=sw1_callback,bouncetime=200) 
GPIO.add_event_detect(sw2,GPIO.RISING,callback=sw2_callback,bouncetime=300) 
GPIO.add_event_detect(sw3,GPIO.RISING,callback=sw3_callback,bouncetime=300) 
GPIO.add_event_detect(sw4,GPIO.RISING,callback=sw4_callback,bouncetime=300) 

audiobook_path="./media/audiobooks/"
music_path="./media/music/"
album=next(os.walk(music_path))[1]
print(album)
playlist_path=audiobook_path + "playlist.txt"
music_playlist=music_path + "playlist.txt"
audiobook_playlist=file_read(playlist_path)
audiobook_number= sum(1 for line in open(playlist_path))
aindex=0
subindex=0
mindex=0
last=0

while True:
   if(sw1_cnt==1 and audio_mode==0):
      print("Play the Audiobook")
      sw2_cnt=0
      audio_mode=1
   elif(sw1_cnt==1 and audio_mode==1):
      print(audiobook_path+audiobook_playlist[aindex].rstrip())
      time.sleep(3)
      if last==0:
         aindex+=1
      else:
          print("Process Kill")
          exit()
      if aindex >= len(audiobook_playlist):
         aindex=0 
   elif(sw1_cnt==2):
      audiobook_skip(aindex)
   elif(sw1_cnt==3):
      print("Double Click : last Audio book")
      sw1_cnt=1
      last=1

   if(sw2_cnt==1 and music_mode==0):
      print("Play the Music Track")
      music_mode=1
      sw1_cnt=0
   elif(sw2_cnt==1 and music_mode==1):
      if(mindex >=len(music_playlist)):
         mindex=0
      print(music_path+"/"+album[subindex].rstrip()+"/"+ music_playlist[mindex].rstrip())
      time.sleep(3)
      mindex+=1
   elif(sw2_cnt==2):
      print("Skip the Music Track")
      music_skip(mindex)
   elif(sw2_cnt==3):
      print("Double Click : Change the Album")
      album_skip(subindex,mindex)

   if(sw3_cnt==1 and light_mode1==0):
      print("Play the light1")
      sw3_cnt=0
      light_mode1=1 
      light_mode2=0 
      light_mode3=0 
   elif(sw3_cnt==2):
      print("Play the light2")
      sw3_cnt=0
      light_mode2=1 
      light_mode3=0 
   elif(sw3_cnt==3):
      print("Play the light3")
      sw3_cnt=0
      light_mode1=0 
      light_mode3=1 

   if(sw4_cnt==1):
      print("close")
      sw4_cnt=0
      sys.exit()

time.sleep(1) 
