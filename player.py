import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import sys
import time
import subprocess
import os
import signal
import alsaaudio
from datetime import datetime
from subprocess import check_output
from espeak import espeak

#----------------------------------
# German Language
# de+12 de+13
#----------------------------------
espeak.set_voice("de+13")

#----------------------------------
# Volume Settings
#----------------------------------
m = alsaaudio.Mixer('PCM')
current_volume = m.getvolume() # Get the current Volume
print(current_volume)
vol=100
m.setvolume(vol) # Set the volume to 70%.
#----------------------------------
# Switch and Light pin 
#----------------------------------

sw1  =37
sw2  =35
sw3  =33
sw4  =31
light=40

#----------------------------------
# Variable for Switch Press Count 
#----------------------------------

sw1_cnt=0
sw2_cnt=0
sw3_cnt=0
sw4_cnt=0

#----------------------------------
# Variable for Switch Press Count 
#----------------------------------

audio_mode=0
music_mode=0
light_mode=0

abook_time=0
music_time=0
abook_hur=0
abook_min=0
end_abook=0
fade_volume=0
#----------------------------------
# Light Duty Cycle Variable 
#----------------------------------

light_max=100
light_off=0
fadeout=0
fadeout1=0
cnt=0
#----------------------------------
# File read : Used for playlist read 
#----------------------------------
def file_read(fname):
    content_array = []
    with open(fname) as f:
         for line in f:
             content_array.append(line)
         return(content_array)

#----------------------------------
# Switch 1 Callback 
#----------------------------------

def sw1_callback(channel):
    global sw1_cnt
    global last
    global pro
    global music_mode
    global abook_time
    abook_time=datetime.now()
    sw1_cnt=sw1_cnt+1
    print(str(sw1_cnt))
    #-------------------
    #Close music if playing 
    #-------------------
    if(music_mode==1):
       subprocess.call(['killall', 'omxplayer.bin'])
       print ("close the omxplayer")
       music_mode=0
       sw2_cnt=0
    #-------------------
    #skip the current audio book
    #-------------------
    if(sw1_cnt==2):
       subprocess.call(['killall', 'mpg123'])
       print ("skip the audiobook")
       sw1_cnt=1
    #-------------------
    #Setup the last Audiobook
    #-------------------
    elif (sw1_cnt>=3):
        last=1
        print("This is lastcount")

#----------------------------------
# Switch 2 Callback 
#----------------------------------

def sw2_callback(channel):
    global sw2_cnt
    global audio_mode
    sw2_cnt=sw2_cnt+1
    #-------------------
    # Close Audiobook 
    #-------------------
    if(audio_mode==1):
       subprocess.call(['killall', 'mpg123'])
       print "close the audiobook"
       audio_mode=0
       sw1_cnt=0
    #-------------------
    # Skip the Current Music Track 
    #-------------------
    if(sw2_cnt==2):
       subprocess.call(['killall', 'omxplayer.bin'])
       sw2_cnt-=1
    #-------------------
    # Change the Album 
    #-------------------
    if(sw2_cnt==3):
       print("change the ablum")
       skip_album()

#----------------------------------
# Switch 3 Callback 
#----------------------------------

def sw3_callback(channel):
    global sw3_cnt
    sw3_cnt=sw3_cnt+1

#----------------------------------
# Switch 4 Callback 
#----------------------------------

def sw4_callback(channel):
    global sw1_cnt
    global sw2_cnt
    global sw3_cnt
    global audio_mode
    global music_mode
    global light_mode
    if (audio_mode==1):
       subprocess.call(['killall', 'mpg123'])
       print "close the audiobook"
       audio_mode=0
       sw1_cnt=0
    if (music_mode==1):
       subprocess.call(['killall', 'omxplayer.bin'])
       print "close the Music"
       sw2_cnt=0
       music_mode=0
    if (light_mode==1):
        pwm.ChangeDutyCycle(0)
   
#----------------------------------
# Music Track Skip 
#----------------------------------

def music_skip(mindex):
    global sw2_cnt
    subprocess.call(['killall', 'omxplayer'])
    print("skip the track")
   

#----------------------------------
# Album Skip 
#----------------------------------

def album_skip():
    global sw2_cnt
    global music_path
    global album
    global music_playlist_path
    global music_playlist
    global subindex
    global mindex
    subprocess.call(['killall', 'omxplayer.bin'])
    sw2_cnt-=2
    print("skip the album")
    subindex+=1
    if subindex >= len(album):
       subindex=0 
    mindex=0
    music_playlist_path=music_path + album[subindex] +"/"+ "playlist.txt"
    music_playlist=file_read(music_playlist_path)


#----------------------------------
# GPIO Init 
#----------------------------------

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(sw1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(sw2, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(sw3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(sw4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(light,GPIO.OUT)
GPIO.add_event_detect(sw1,GPIO.FALLING,callback=sw1_callback,bouncetime=300) 
GPIO.add_event_detect(sw2,GPIO.RISING,callback=sw2_callback,bouncetime=300) 
GPIO.add_event_detect(sw3,GPIO.RISING,callback=sw3_callback,bouncetime=300) 
GPIO.add_event_detect(sw4,GPIO.RISING,callback=sw4_callback,bouncetime=300) 

#----------------------------------
# Audiobook Path 
#----------------------------------
audiobook_path="./media/audiobooks/"
#----------------------------------
# Music Path 
#----------------------------------
music_path="./media/music/"

#----------------------------------
# Music and Audiobook initialization 
#----------------------------------
aindex=0
subindex=0
mindex=0
last=0
album=next(os.walk(music_path))[1]
audio_playlist_path=audiobook_path + "playlist.txt"
music_playlist_path=music_path + album[subindex] +"/"+ "playlist.txt"
audiobook_playlist=file_read(audio_playlist_path)
music_playlist=file_read(music_playlist_path)


#----------------------------------
# PWM init() 
#----------------------------------
pwm=GPIO.PWM(light,100)
pwm.start(0) 
#----------------------------------
# Main Loop 
#----------------------------------

try:
    while True:
    #----------------------------------
    # Condition for Audio Books 
    #----------------------------------
    
       if(sw1_cnt==1 and audio_mode==0):
          sw2_cnt=0
          audio_mode=1
       elif(sw1_cnt==1 and audio_mode==1):
          abook=audiobook_path+audiobook_playlist[aindex].rstrip()
          name=str(audiobook_playlist[aindex].rstrip())
          ttsc="espeak -vde+f2 --stdout '" + name  + "' -a 100 -s 110 |aplay"
          os.system(ttsc)
          cmd='mpg123'  
          pro=subprocess.call([cmd,'-quit',abook])
          abook_min=("%2d" % (abook_time.minute))
          abook_hur=("%2d" % (abook_time.hour))
          end_abook=59- int(abook_min)
          current_time=datetime.now()
          current_hour=current_time.hour
          current_min =current_time.minute
          if ((int(current_hour)==(int(abook_hur)+1))and (int(current_min)==(end_abook))):
               fade_volume=1 
        
          if ((int(current_hour)==(int(abook_hur)+1))and (int(current_min)<(end_abook+2)) and fade_volume==1 ):
               m.setvolume(vol)
               vol-=1
          else:
               sw1_cnt=0
               audio_mode=0
               fade_volume=0

          if last==0:
             aindex+=1
          if aindex >= len(audiobook_playlist):
             aindex=0 
    
    #----------------------------------
    # Condition for Music Mode 
    #----------------------------------
       if(sw2_cnt==1 and music_mode==0):
          print("Play the Music Track")
          music_mode=1
          sw1_cnt=0
       elif(sw2_cnt==1 and music_mode==1):
          if(mindex >=len(music_playlist)):
             mindex=0
          print(music_path+album[subindex].rstrip()+"/"+ music_playlist[mindex].rstrip())
          music=music_path+album[subindex].rstrip()+"/"+ music_playlist[mindex].rstrip()     
          cmd1='omxplayer'  
          pre=subprocess.call([cmd1,music])
          mindex+=1
          abook_min=("%2d" % (abook_time.minute))
          abook_hur=("%2d" % (abook_time.hour))
          end_abook=59- int(abook_min)
          current_time=datetime.now()
          current_hour=current_time.hour
          current_min =current_time.minute
          if ((int(current_hour)==(int(abook_hur)+1))and (int(current_min)==(end_abook))):
               fade_volume=1 
        
          if ((int(current_hour)==(int(abook_hur)+1))and (int(current_min)<(end_abook+2)) and fade_volume==1 ):
               m.setvolume(vol)
               vol-=1
          else:
               sw2_cnt=0
               music_mode=0
               fade_volume=0

    #elif(sw2_cnt==2):
       #   print("Skip the Music Track")
       #   music_skip(mindex)
       #   sw2_cnt-=1
       #   print("after skip :%d" %(sw_cnt))
       #elif(sw2_cnt==3):
       #   print("Double Click : Change the Album")
       #   album_skip()
    
    #----------------------------------
    # Condition for Light Mode 
    #----------------------------------
    
       if(sw3_cnt==1 and light_mode==0):
          print("Play the light1")
          light_mode=1 
          start_light=datetime.now()
          start_second=('%2d' % (start_light.second))
          start_minute=('%2d' % (start_light.minute))
          if(int(start_second) > 30):
            end_second=int(start_second)+30-59
          else:
            end_second=int(start_second)+30

          if(int(start_minute) > 30):
            end_minute=int(start_minute)+30-59
          else:
            end_minute=int(start_minute)+30 
       elif(sw3_cnt==1 and light_mode==1):
           on_light=datetime.now()
           second=('%2d' % (on_light.second))
           minute=('%2d' % (on_light.minute))
           if(str(end_second)==second and fadeout==0):
                fadeout=1
           elif(fadeout==1):
             if(str(end_minute)==minute):
               pwm.ChangeDutyCycle(0)
             else:
                if(cnt==2142*4):
                   cnt=0
                   if(light_max!=0):
                      light_max-=1
                      pwm.ChangeDutyCycle(light_max)
                      #print(light_max)
                else:
                   cnt=cnt + 1
           elif(fadeout==0):
             pwm.ChangeDutyCycle(light_max)
       elif(sw3_cnt==2 and (light_mode==1 or light_mode==0)):
          print("Play the light3")
          # on the light till 60 mins
          on_light=datetime.now()
          minute=('%2d' % (on_light.minute))
          if(minute==minute-1): 
             fadeout=1   
             cnt=0
          elif(fadeout1==0):
             pwm.ChangeDutyCycle(light_max)
          elif(fadeout1==1):  
             if(str(end_minute)==minute):
               pwm.ChangeDutyCycle(0)
             else:
                if(cnt==2142*8):
                   cnt=0
                   if(light_max!=0):
                      light_max-=1
                      pwm.ChangeDutyCycle(light_max)
                      #print(light_max)
                else:
                   cnt=cnt + 1
       elif(sw3_cnt==3 and light_mode==1):
          print("Play the light3")
          pwm.ChangeDutyCycle(light_max)
          sw3_cnt=0
    
    
    time.sleep(0.5)

except KeyboardInterrupt:
    pass

GPIO.cleanup()
pwm.stop()
