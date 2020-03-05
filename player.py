import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import sys
import time

sw1_cnt=0
sw2_cnt=0
sw3_cnt=0
sw4_cnt=0

sw1=37
sw2=35
sw3=33
sw4=31

audio_mode1=0
audio_mode2=0
audio_mode3=0

music_mode1=0
music_mode2=0
music_mode3=0
music_mode4=0


light_mode1=0
light_mode2=0
light_mode3=0


def sw1_callback(channel):
    global sw1_cnt
    sw1_cnt=sw1_cnt+1
    print("Button-1 was pushed :" + str(sw1_cnt))

def sw2_callback(channel):
    global sw2_cnt
    sw2_cnt=sw2_cnt+1
    print("Button-2 was pushed :" + str(sw2_cnt))

def sw3_callback(channel):
    global sw3_cnt
    sw3_cnt=sw3_cnt+1
    print("Button-3 was pushed :" + str(sw3_cnt))

def sw4_callback(channel):
    global sw4_cnt
    sw4_cnt=sw4_cnt+1
    print("Button-4 was pushed :" + str(sw4_cnt))


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(sw1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(sw2, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(sw3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(sw4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.add_event_detect(sw1,GPIO.RISING,callback=sw1_callback,bouncetime=300) 
GPIO.add_event_detect(sw2,GPIO.RISING,callback=sw2_callback,bouncetime=300) 
GPIO.add_event_detect(sw3,GPIO.RISING,callback=sw3_callback,bouncetime=300) 
GPIO.add_event_detect(sw4,GPIO.RISING,callback=sw4_callback,bouncetime=300) 


while True:

   if(sw1_cnt==1 and audio_mode1==0):
      audio_mode1=1
      sw_cnt=0 
      audio_mode2=0
      audio_mode3=0
      print("read the file name") 
      print("Play the firstfile")
   elif(sw1_cnt==1 and audio_mode1==1):
      print("playing...");
      print("skip the next file..")
      sw_cnt=0
   elif(sw1_cnt==2 and audio_mode2==0):
      print("Play the mode2")
      sw1_cnt=0
      audio_mode2=1 
      audio_mode3=0 
   elif(sw1_cnt==3 and audio_mode3==0):
      print("Play the mode3")
      sw1_cnt=0
      audio_mode3=1
      audio_mode1=0 

   if(sw2_cnt==1 and music_mode1==0):
      print("Play the music1")
      sw2_cnt=0
      music_mode1=1 
      music_mode2=0 
      music_mode3=0 
   elif(sw2_cnt==2 and music_mode2==0):
      print("Play the music2")
      sw2_cnt=0
      music_mode2=1 
      music_mode3=0 
   elif(sw2_cnt==3):
      print("Play the music3")
      sw2_cnt=0
      music_mode3=1 
      music_mode1=0 

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
