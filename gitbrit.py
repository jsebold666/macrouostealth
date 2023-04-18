from discord_webhook import DiscordWebhook  # pip install discord-webhook
import time
import re
from py_stealth import *
from datetime import datetime, timedelta

hookurl = 'https://discord.com/api/webhooks/985864620390645810/9XA7TjkhC0VcaaE4qr8xPzAfP5SrJHpnzkNuMSIlH-j_cINrTw5ZoUi-oacCZ3z08E5g'
hookurl2 = 'https://discordapp.com/api/webhooks/943463522531168287/DhwRzULeTHnQyqWSeEh-j3nemazbRAjppj8eDJ_Dbhm4kAQ2tLQuhwiBEYErbLB9OuA-'
hookurlmarcos =   'https://discord.com/api/webhooks/1067495037564354681/Xdf-Zzl1s32LG0jxoCPgLWJ4QUnOYPxV3XA0r_M3cJLtS3xYZ8ePRvEyrSQxQunC7ltZ'
friends = [0x123456, 0x234567]
shouttime = 60
idtimers = {}
SetFindDistance(30)
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
ignore_texts = ['healer','mondain','energy vortex','jack rabbit','a skeleton', 'RIP Demise', 'rip demise']

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
        "sentinel": "You see",
    }
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
    webhook2 = DiscordWebhook(url=hookurlmarcos, content=msg)
    webhook2.execute()



def findenemy(location):
    global idtimers, buffer, ANTISPAM, sb
    if FindTypesArrayEx([0x0191, 0x0190], [0xFFFF], [Ground()], False):
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
                        print('limpado ->', buffer)
                        ANTISPAM = datetime.now() + timedelta(seconds=5)


location = get_character_location(GetName(Self()))
Ignore(Self())
while True:
    time.sleep(0.1)
    findenemy(location)
    Wait(1000)