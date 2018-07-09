#!/usr/bin/env python
import sys
import os
import requests
import logging
import json
import time
Rabbit_IP = '192.168.1.253'
CritialAlertColor = 'E10000'
NonCriticalAlertColor = 'D7FF00'
AlertSound = 'twang_04'
AlertVoice = 6

def strongbad():
     LED('000000','000000')
     LED('00FFFF','800080',1,300)
     ears(64,0)
     sound('system_is_down')
     LED('000000','000000') 

     

# Critical Alert. Message is any text for tts to speak. If not specified will say nothing. Sound = 1 will loop with alert sound
def CriticalAlert(message = 'off',noise = 0, soundFile = AlertSound,AlertVoice = AlertVoice, color = CritialAlertColor,loopnum = 2):
    LED(color,'000000',1,250) # flash LED red quickly
    ears(24,0) #ears will rotate. Ending straight out to the side
    if message != 'off' and noise == 0:
        TTS(message,AlertVoice)
    elif message != 'off' and noise == 1:
        for number in range(loopnum):
            sound(soundFile)
            TTS(message,AlertVoice)
    elif message == 'off' and sound == 1:
        sound(soundFile)
    else:
        return

""" # same as critical, without sound effect
def CriticalAlertNoSound(message,color = CritialAlertColor): #"Wake the dead" sort of thing. With passion!
    LED(color,'000000',1,250) # flash LED red quickly
    ears(24,0) #ears will rotate. Ending straight out to the side
    TTS(message,3) """

# Non-critical warnings
def nonCriticalAlert(color = NonCriticalAlertColor):
    if checkState() == CritialAlertColor: #uses the LED as a proxy for a state flag. If the LED is the CritialAlertColor, will not overwrite
        return
    else:
        LED(color,'000000',1,1750)
        ears_individual(0,7,0)

#Reset the ears to up, LED to green and announce system is up
def CriticalAlertReset (message = 'System back to normal'):
    LED('00FF00',000000,0,0)
    ears_reset()
    TTS(message,AlertVoice)
# clears alerts with less fuss
def nonCritialAlertReset():
    if checkState() == CritialAlertColor: #uses the LED as a proxy for a state flag. If the LED is the CritialAlertColor, will not overwrite
        return
    else:
        LED('00FF00',000000,0,0)
        ears_reset()


#Calls the state API and puls the curernt LED color. For checking the alert state of the bunny
def checkState():
    s = requests.get('http://'+Rabbit_IP+'/cgi-bin/status')
    resp = s.json()
    return resp['led_color']

"""
LED Parameters
    color: RGB hex color Solid color with pulse = 0 or first color in flash if pulse = 1
        Red = FF0000 Green = 00FF00 Blue = 0000FF Yellow = 60FF00 Magenta=800080 Purple = 200080 Teal = 00FFFF Orange = D7FF00 White = 40FFFF
    color 2: If set and pulse =1. LED will fade between color and color2.
    speed: LED Flash frequency in ms
    pulse: 1 = yes 0= no
"""
def LED(color,color2, pulse = 0, speed = 0,no_memory = 0):
    LED = {'color': color, 'color2': color2, 'pulse': pulse,'speed': speed,'no_memory': no_memory}
    l = requests.get('http://'+Rabbit_IP+'/cgi-bin/leds',params=LED)

"""
Text-to-Speech Parameters
    message : plaintext message to send to bunny
    voice: tts voice type. 3 = CA Female 4 = CA Male 5 = US Female 6 = Us Female 7 = UK female 8 = UK male
"""
def TTS(message,voice = 6):
    TTS = {'voice': voice,'text': message,'nocache': '0'}
    t = requests.get('http://'+Rabbit_IP+'/cgi-bin/tts',params=TTS)

""" # for one with an alert noise and TTS
def TTSAlert(message,name,loopnum = 2,voice = 6):
    TTS = {'voice': voice,'text': message,'nocache': '0'}
    SOUND = {'id': name}
    for number in range(loopnum):
        s = requests.get('http://'+Rabbit_IP+'/cgi-bin/sound',params=SOUND)
        t = requests.get('http://'+Rabbit_IP+'/cgi-bin/tts',params=TTS) """

#For sound list point browser to Rabbit_IP/cgi/bin/sound_list
def sound(name):
    SOUND = {'id': name}
    s = requests.get('http://'+Rabbit_IP+'/cgi-bin/sound',params=SOUND)

"""
Ear Rotation Parameters
position is a value from 0 to infinity, with one full rotation being 16. 32 = 2 rotations, 48 = 3 rotations..etc
Unless a reset is called, ear will always rotate from last recorded postion.
ex. last call was 64 (4 rotations) and next call is 8 (1/2 rotation) then ears will rotate 3.5 times backward back from 64 to 8
noreset = 1 will cycle ears to top position and start from 0
"""
def ears(pos,noreset=1):
    EAR = {'left': pos,'right':pos,'noreset': noreset}
    e = requests.get('http://'+Rabbit_IP+'/cgi-bin/ears',params=EAR)

def ears_individual(left,right,noreset=1):
    EAR = {'left': left,'right': right,'noreset': noreset}
    e = requests.get('http://'+Rabbit_IP+'/cgi-bin/ears',params=EAR)

def ears_reset():
    e = requests.get('http://'+Rabbit_IP+'/cgi-bin/ears_reset')

#ears_reset()
#sound(AlertSound)
""" CriticalAlert('BNSF Sniffer Down',1)
nonCriticalAlert()
CriticalAlertReset()
time.sleep(1.5)
nonCriticalAlert()
time.sleep(1.5)
nonCritialAlertReset() """
#nonCriticalAlert()
#strongbad()
