# rabbit_api
#API calls to the OpenKarotz software. Go to Rabbit_IP/api.html for additionaldocumentation.
import json
import requests
import configparser
import logging

#read config.ini and set Rabbit_IP
def get_ip():
    config = configparser.ConfigParser()
    config.read('config.ini')
    IP = config.sections()
    return print(IP)

def get_timeout():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()
    return config['controllerconfig']['timeout']

"""
LED
    color: RGB hex color Solid color with pulse = 0 or first color in flash if pulse = 1
        Red = FF0000 Green = 00FF00 Blue = 0000FF Yellow = 60FF00 Magenta=800080 Purple = 200080 Teal = 00FFFF Orange = D7FF00 White = 40FFFF
    color 2: If set and pulse =1. LED will fade between color and color2.
    speed: LED Flash frequency in ms
    pulse: 1 = yes 0= no
"""
def LED(color,color2 = '000000', pulse = 0, speed = 500,no_memory = 0):
    Rabbit_IP = get_ip()
    rabbit_timeout = get_timeout()
    try:
        LED = {'color': color, 'color2': color2, 'pulse': pulse,'speed': speed,'no_memory': no_memory}
        l = requests.get('http://'+Rabbit_IP+'/cgi-bin/leds',params=LED,timeout=rabbit_timeout)
        resp = s.json()
        if resp[msg] == 'Unable to perform action, rabbit is sleeping.':
            raise rabbitSleeping (msg)
        else:
            return resp
    except (ConnectionError, Timeout):
        resp = s.json()
        return resp
    except rabbitSleeping:
        print('Rabbit is in sleep mode')

    


"""
Text-to-Speech Parameters
    message : plaintext message to send to bunny
    voice: tts voice type. 3 = CA Female 4 = CA Male 5 = US Female 6 = Us Female 7 = UK female 8 = UK male
"""
def TTS(message,voice = 6,cache = 1):
    Rabbit_IP = get_ip()
    TTS = {'voice': voice,'text': message,'nocache': cache}
    t = requests.get('http://'+Rabbit_IP+'/cgi-bin/tts',params=TTS,timeout=rabbit_timeout)

"""
Sound parameters
For sound list point browser to Rabbit_IP/cgi/bin/sound_list
For custome sound upload mp3 file to /usr/openkarotz/Sounds
"""
def sound(name):
    Rabbit_IP = get_ip()
    SOUND = {'id': name}
    s = requests.get('http://'+Rabbit_IP+'/cgi-bin/sound',params=SOUND,timeout=rabbit_timeout)

"""
Ear Rotation Parameters
position is a value from 0 to infinity, with one full rotation being 16. 32 = 2 rotations, 48 = 3 rotations..etc
Unless a reset is called, ear will always rotate from last recorded postion.
ex. last call was 64 (4 rotations) and next call is 8 (1/2 rotation) then ears will rotate 3.5 times backward back from 64 to 8
noreset = 1 will cycle ears to top position and start from 0
"""
def ears_together(pos,noreset=1):
    Rabbit_IP = get_ip()
    EAR = {'left': pos,'right':pos,'noreset': noreset}
    e = requests.get('http://'+Rabbit_IP+'/cgi-bin/ears',params=EAR,timeout=rabbit_timeout)

def ears_individual(left,right,noreset=1):
    Rabbit_IP = get_ip()
    EAR = {'left': left,'right': right,'noreset': noreset}
    e = requests.get('http://'+Rabbit_IP+'/cgi-bin/ears',params=EAR,timeout=rabbit_timeout)

def ears_reset():
    Rabbit_IP = get_ip()
    e = requests.get('http://'+Rabbit_IP+'/cgi-bin/ears_reset',timeout=rabbit_timeout)


#Calls the state API
def checkStatus(key =''):
    Rabbit_IP = get_ip()
    if key != '':
        s = requests.get('http://'+Rabbit_IP+'/cgi-bin/status',timeout=rabbit_timeout)
        resp = s.json()
        return resp[key]
    elif key == '':
        s = requests.get('http://'+Rabbit_IP+'/cgi-bin/status',timeout=rabbit_timeout)
        resp = s.json()
        return resp
# puts rabbit in sleep mode. Can be used to mute actions
def gotosleep():
    Rabbit_IP = get_ip()
    r = requests.get('http://'+Rabbit_IP+'/cgi-bin/sleep',timeout=rabbit_timeout)

# wake the rabbit up from sleep mode
def wakeup():
    Rabbit_IP = get_ip()
    r = requests.get('http://'+Rabbit_IP+'/cgi-bin/wakeup?silent=1')

#reboot the rabbit
def rabbit_reboot():
    Rabbit_IP = get_ip()
    r = requests.get('http://'+Rabbit_IP+'/cgi-bin/reboot')