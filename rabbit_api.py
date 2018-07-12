# rabbit_api
#API calls to the OpenKarotz software. Go to Rabbit_IP/api.html for additionaldocumentation.
import json
import requests
import configparser
import logging
import os

# define Python user-defined exceptions
class rabbitSleeping(Exception):
   """Rabbit is in sleep mode"""
   pass

## config paser is being a pain in the ass. Dummy functions for now
def get_ip():
    Rabbit_IP = '192.168.1.253'
    return Rabbit_IP

def get_timeout():
    timeout = 10
    return timeout

""" 
# fucntions that use config parser. Cant figure out why it will not see the file
#read config.ini and set Rabbit_IP
def get_ip():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['Rabbit']['rabbitIP']

def get_timeout():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()
    return config['controller']['timeout'] """

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
        l = requests.get('http://'+Rabbit_IP+'/cgi-bin/leds',params=LED, timeout=rabbit_timeout)
        resp = json.loads(l.text)
        if 'msg' in resp:
            if resp['msg'] == 'Unable to perform action, rabbit is sleeping.':
                return print(resp['msg'])
        else:
            return print(resp)
    except (requests.ConnectionError, requests.Timeout):
        resp = json.loads(l.text)
        print ('connection timeout')
        return resp

    


"""
Text-to-Speech Parameters
    message : plaintext message to send to bunny
    voice: tts voice type. 3 = CA Female 4 = CA Male 5 = US Female 6 = Us Female 7 = UK female 8 = UK male
"""
def TTS(message,voice = 6,cache = 1):
    Rabbit_IP = get_ip()
    rabbit_timeout = get_timeout()
    try:
        TTS = {'voice': voice,'text': message,'nocache': cache}
        l = requests.get('http://'+Rabbit_IP+'/cgi-bin/tts',params=TTS,timeout=rabbit_timeout)
        resp = json.loads(l.text)
        if resp['played'] == 'False':
            return print(resp['Unable to perform action, rabbit is sleeping.'])
        else:
            return print(resp)
    except (requests.ConnectionError, requests.Timeout):
        resp = json.loads(l.text)
        print ('connection timeout')
        return resp
"""
Sound parameters
For sound list point browser to Rabbit_IP/cgi/bin/sound_list
For custome sound upload mp3 file to /usr/openkarotz/Sounds
"""
def sound(name):
    Rabbit_IP = get_ip()
    rabbit_timeout = get_timeout()
    try:
        SOUND = {'id': name}
        l = requests.get('http://'+Rabbit_IP+'/cgi-bin/sound',params=SOUND,timeout=rabbit_timeout)
        resp = json.loads(l.text)
        if 'msg' in resp:
            if resp['msg'] == 'Unable to perform action, rabbit is sleeping.':
                return print(resp['msg'])
        else:
            return print(resp)
    except (requests.ConnectionError, requests.Timeout):
        resp = json.loads(l.text)
        print ('connection timeout')
        return resp

"""
Ear Rotation Parameters
position is a value from 0 to infinity, with one full rotation being 16. 32 = 2 rotations, 48 = 3 rotations..etc
Unless a reset is called, ear will always rotate from last recorded postion.
ex. last call was 64 (4 rotations) and next call is 8 (1/2 rotation) then ears will rotate 3.5 times backward back from 64 to 8
noreset = 1 will cycle ears to top position and start from 0
"""
def ears_together(pos,noreset=1):
    Rabbit_IP = get_ip()
    rabbit_timeout = get_timeout()
    try:
        EAR = {'left': pos,'right':pos,'noreset': noreset}
        l = requests.get('http://'+Rabbit_IP+'/cgi-bin/ears',params=EAR,timeout=rabbit_timeout)
        resp = json.loads(l.text)
        if 'msg' in resp:
            if resp['msg'] == 'Unable to perform action, rabbit is sleeping.':
                return print(resp['msg'])
        else:
            return print(resp)
    except (requests.ConnectionError, requests.Timeout):
        resp = json.loads(l.text)
        print ('connection timeout')
        return resp

def ears_individual(left,right,noreset=1):
    Rabbit_IP = get_ip()
    rabbit_timeout = get_timeout()
    try:   
        EAR = {'left': left,'right': right,'noreset': noreset}
        l = requests.get('http://'+Rabbit_IP+'/cgi-bin/ears',params=EAR,timeout=rabbit_timeout)
        resp = json.loads(l.text)
        if 'msg' in resp:
            if resp['msg'] == 'Unable to perform action, rabbit is sleeping.':
                return print(resp['msg'])
        else:
            return print(resp)
    except (requests.ConnectionError, requests.Timeout):
        resp = json.loads(l.text)
        print ('connection timeout')
        return resp

def ears_reset():
    Rabbit_IP = get_ip()
    rabbit_timeout = get_timeout()
    try:
        l = requests.get('http://'+Rabbit_IP+'/cgi-bin/ears_reset',timeout=rabbit_timeout)  
        resp = json.loads(l.text)
        if 'msg' in resp:
            if resp['msg'] == 'Unable to perform action, rabbit is sleeping.':
                return print(resp['msg'])
        else:
            return print(resp)
    except (requests.ConnectionError, requests.Timeout):
        resp = json.loads(l.text)
        print ('connection timeout')
        return resp


#Calls the state API
def checkStatus(key =''):
    Rabbit_IP = get_ip()
    rabbit_timeout = get_timeout()
    try:
        if key != '':
            l = requests.get('http://'+Rabbit_IP+'/cgi-bin/status',timeout=rabbit_timeout)
            resp = json.loads(l.text)
            return resp[key]
        elif key == '':
            l = requests.get('http://'+Rabbit_IP+'/cgi-bin/status',timeout=rabbit_timeout)
            resp = json.loads(l.text)
            return resp
    except (requests.ConnectionError, requests.Timeout):
        resp = json.loads(l.text)
        print ('connection timeout')
        return resp

# puts rabbit in sleep mode. Can be used to mute actions
def gotosleep():
    Rabbit_IP = get_ip()
    rabbit_timeout = get_timeout()
    try:
        l = requests.get('http://'+Rabbit_IP+'/cgi-bin/sleep')
        resp = json.loads(l.text)
        if 'msg' in resp:
            if resp['msg'] == 'Unable to perform action, rabbit is sleeping.':
                return print(resp['msg'])
        else:
            return print(resp)
    except (requests.ConnectionError, requests.Timeout):
        resp = json.loads(l.text)
        print ('connection timeout')
        return resp

# wake the rabbit up from sleep mode
def wakeup():
    Rabbit_IP = get_ip()
    rabbit_timeout = get_timeout()
    try:
        l = requests.get('http://'+Rabbit_IP+'/cgi-bin/wakeup?silent=1')
        resp = json.loads(l.text)
        return resp
    except (requests.ConnectionError, requests.Timeout):
        resp = json.loads(l.text)
        print ('connection timeout')
        return resp
#reboot the rabbit
def rabbit_reboot():
    Rabbit_IP = get_ip()
    rabbit_timeout = get_timeout()
    try:
        l = requests.get('http://'+Rabbit_IP+'/cgi-bin/reboot')
        resp = json.loads(l.text)
        return resp
    except (requests.ConnectionError, requests.Timeout):
        resp = json.loads(l.text)
        print ('connection timeout')
        return resp