import json
import requests
"""
Various API calls to the openkarotz API interface

LED Parameters
    color: RGB hex color Solid color with pulse = 0 or first color in flash if pulse = 1
        Red = FF0000 Green = 00FF00 Blue = 0000FF Yellow = 60FF00 Magenta=800080 Purple = 200080 Teal = 00FFFF Orange = D7FF00 White = 40FFFF
    color 2: If set and pulse =1. LED will fade between color and color2.
    speed: LED Flash frequency in ms
    pulse: 1 = yes 0= no
"""
def LED(Rabbit_IP,color,color2, pulse = 0, speed = 0,no_memory = 0):
    LED = {'color': color, 'color2': color2, 'pulse': pulse,'speed': speed,'no_memory': no_memory}
    l = requests.get('http://'+Rabbit_IP+'/cgi-bin/leds',params=LED)

"""
Text-to-Speech Parameters
    message : plaintext message to send to bunny
    voice: tts voice type. 3 = CA Female 4 = CA Male 5 = US Female 6 = Us Female 7 = UK female 8 = UK male
"""
def TTS(Rabbit_IP,message,voice = 6,cache = 0):
    TTS = {'voice': voice,'text': message,'nocache': cache}
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


    #Calls the state API and puls the curernt LED color. For checking the alert state of the bunny
def checkState(Rabbit_IP):
    s = requests.get('http://'+Rabbit_IP+'/cgi-bin/status')
    resp = s.json()
    return resp['led_color']
