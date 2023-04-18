from discord_webhook import DiscordWebhook  # pip install discord-webhook
import time
import re
from py_stealth import *
from datetime import datetime, timedelta

hookurl = 'https://discord.com/api/webhooks/990945080783306822/xOQMwNo-kiiIMhRIDrTqxzb8tR44bXGOTJNyCaPoXCGFPtZUQWAGJjvWHdHYY0WpDKVG'

friends = [0x123456, 0x234567]
shouttime = 60
idtimers = {}
SetFindDistance(30)
SetFindVertical(30)
ANTISPAM = datetime.now()
buffer = []
sb = ''
find_messeges = [
    '[req]',
    '[kvg]',
    '[loop]',
    '[msby]',
    '[trt]',
    '[chn]',
    '[es]',
    '[nwo]',
    '[req-]',
    '[1410]',
    '[dadz]',
    '[dads]',
    '[dad!]',
    '[sas]',
    '[sl]',
    '[tb]',
    '[com]',
    '[min]',
    '[stun]',
    '[fm]',
    '[f.m]',
    '[cst]',
    '[zxii]',
    '[cccp]',
    '[51-]',
    '[a^r]',
    '[.py]',
    '[.dps]',
    '[d*a]',
    '[epb]',
    '[mbga]',
    '[lolz]',
    '[cec]',
    '[drow]',
    '[x__x]',
    '[myth]',
    'server wars',
    'process took',
    'server',
    'event gate',
    'you see:',
    '[system]',
    '[hz]'
]
ignore_texts = ['healer','mondain','energy vortex','jack rabbit','a skeleton']

def fillter(s):
    global idtimers, buffer, ANTISPAM, sb

        
        
    ignore = False 
    for ig in ignore_texts:
        if ig in s.lower():
            ignore = True

    if ignore:
        return

    if s not in buffer:
        buffer.append(s)

def get_character_location(nickname):
    location = {
        "hiall": "You see", 
        "nick2": "You See"
    } 
    if (nickname == 'hiall') :
        return location.get(nickname, "Fire Entrance") 
    elif (nickname == 'nick2') :
        return location.get(nickname, "Destard")  
    else:
         return location.get(nickname, "You see") 


def discosend(message):
    print('MESSAGE ->', message)
    if len(message) <= 0:
        return

    msg = '```'
    for i in message:
        msg += i
    msg += '```'
    print('Send to Discord...')
    webhook = DiscordWebhook(url=hookurl, content=msg)
    webhook.execute()


def findenemy(location):
    global idtimers, buffer, ANTISPAM, sb
    if FindTypesArrayEx([0x0191, 0x0190, 0x25d], [0xFFFF], [Ground()], False):
        for character in GetFoundList():
            # enemy = GetName(character) # если имя
            enemy = character  # если ид

            fillter(GetAltName(character))
            if ANTISPAM <= datetime.now():
                for allnames in buffer:
                    if len(allnames) != 0:
                        print('vai enviar ->', str(allnames))
                        discosend(f"{location} : {allnames}")
                        buffer.clear()
                        print('limpado ->', allnames)
                        ANTISPAM = datetime.now() + timedelta(seconds=120)


location = get_character_location(GetName(Self()))
Ignore(Self())
while True:
    time.sleep(0.1)
    findenemy(location)
    Wait(1000)