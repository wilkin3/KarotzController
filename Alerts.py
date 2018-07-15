#!/usr/bin/env python
import sys
import os
import requests
import logging
import json
import time
import rabbit_api

CritialAlertColor = 'E10000'
NonCriticalAlertColor = 'D7FF00'
AlertSound = 'laser_15'
AlertVoice = '6'


def strongbad():
     LED('000000','000000')
     LED('00FFFF','800080',1,300)
     ears(64,0)
     sound('system_is_down')
     LED('000000','000000') 

     

# Critical Alert. Message is any text for tts to speak. If not specified will say nothing. Sound = 1 will loop with alert sound
def CriticalAlert(message = 'off',noise = 0, sound = 0, soundFile = AlertSound, AlertVoice = AlertVoice, color = CritialAlertColor,loopnum = 2):
    rabbit_api.LED(color,'000000',1,250) # flash LED red quickly
    rabbit_api.ears_together(24,0) #ears will rotate. Ending straight out to the side
    if message != 'off' and noise == 0:
        rabbit_api.TTS(message,AlertVoice)
    elif message != 'off' and noise == 1:
        for number in range(loopnum):
            rabbit_api.sound(soundFile)
            rabbit_api.TTS(message,AlertVoice)
    elif message == 'off' and sound == 1:
        rabbit_api.sound(soundFile)
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


""" #Calls the state API and puls the curernt LED color. For checking the alert state of the bunny
def checkState():
    s = requests.get('http://'+Rabbit_IP+'/cgi-bin/status')
    resp = s.json()
    return resp['led_color']
 """