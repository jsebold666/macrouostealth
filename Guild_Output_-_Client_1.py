from discord_webhook import DiscordWebhook
from datetime import datetime, timedelta
import os
import time

# here you can put text for scan in journal
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
# Webhook url
#link3 = 'https://discordapp.com/api/webhooks/765804725622800436/1LmaM5ZozxzyA2lcHwxTZdHXzO1e69Ez-6hL35aNNvLeN0-pbr8RpFpS0sE0Jsgphyb3'
#link = 'https://discordapp.com/api/webhooks/729205467636564008/0mTtIBJFcC5KiXr10eu4e7NV89qy9zY7KJ5IwgmG3-E034MqIISIlPj_6otijY5E6QhD'
link2 = 'https://discord.com/api/webhooks/943463522531168287/DhwRzULeTHnQyqWSeEh-j3nemazbRAjppj8eDJ_Dbhm4kAQ2tLQuhwiBEYErbLB9OuA-'
link4 = 'https://discordapp.com/api/webhooks/772885855823986689/gHcBbpBru8pNXYcz6ZSJhXvzijrSzX4httWN2DWLW1nEPnIz1CJussffsRhk-LwKXYOr'
# In uo folder open uo.cfg and set this lines
# SaveJournal=on
# JournalSaveFile=journal.txt     // if you miss this string add it
# path to your journal file
# example path = r'your_patch'
path = r'D:\gameuo - Copia\GameClient\journal.txt'
#path = r'C:\Users\Administrator\Desktop\_Client 1_journal.txt'
#
ANTISPAM = datetime.now()
buffer = []


#

def send_discord_msg(ls):
    if len(ls) <= 0:
        return

    msg = '```'
    for i in ls:
        msg += i
    msg += '```'
    print('Send to Discord...')
    #d = DiscordWebhook(url=link, content=msg)
    d2 = DiscordWebhook(url=link2, content=msg)
    #d3 = DiscordWebhook(url=link3, content=msg)
    d4 = DiscordWebhook(url=link4, content=msg)
    #d.execute()
    d2.execute()
   # d3.execute()
    d4.execute()

ignore_texts = ['healer','mondain','energy vortex','jack rabbit','a skeleton'] #journal text to ignore
def fillter(ls):       
    for s in ls:     
        ignore = False 
        for ig in ignore_texts:
            if ig in s.lower():
                ignore = True

        if ignore:
            continue

        for fm in find_messeges:
            if fm in s.lower():
                if s not in buffer:
                    buffer.append(s)
                    print('DETECTED ->', s)

#def fillter(ls):
#    for s in ls:
 #       for fm in find_messeges:
 #           if fm in s.lower():
 #               if s not in buffer:
 #                   buffer.append(s)
 #                   print('DETECTED ->', s)


def readJournal(path):
    global buffer, ANTISPAM
    fsize = os.path.getsize(path)
    log = []
    while True:
        time.sleep(0.1)
        if os.path.getsize(path) != fsize:
            with open(path, "r") as f:
                log = f.readlines()
                print(log)
            f = open(path, 'w').close()
            fsize = os.path.getsize(path)
            fillter(log)
            if ANTISPAM <= datetime.now():
                send_discord_msg(buffer)
                buffer.clear()
                ANTISPAM = datetime.now() + timedelta(seconds=1)


if __name__ == '__main__':
    f = open(path, 'w').close()
    readJournal(path=path)