from discord_webhook import DiscordWebhook
from datetime import datetime, timedelta
import os
import time

# here you can put text for scan in journal
find_messeges = [
    'server wars',
    'process took',
    'server',
    'event gate',
    'you see:',
    '[system]'
]
# Paste your webhook url below
link4 = 'https://discord.com/api/webhooks/990945080783306822/xOQMwNo-kiiIMhRIDrTqxzb8tR44bXGOTJNyCaPoXCGFPtZUQWAGJjvWHdHYY0WpDKVG'
# In uo folder open uo.cfg and set this lines
# SaveJournal=on
# JournalSaveFile=journal.txt     #if you are missing this string, add it
# path to your journal file
# example path = r'your_patch'
path = r'D:\gameuo - Copia\GameClient\journal.txt'
#
ANTISPAM = datetime.now()
buffer = []


def send_discord_msg(ls):
    if len(ls) <= 0:
        return

    msg = '```'
    for i in ls:
        msg += i
    msg += '```'
    print('Send to Discord...')
    d4 = DiscordWebhook(url=link4, content=msg)
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



def readJournal(path):
    global buffer, ANTISPAM
    fsize = os.path.getsize(path)
    log = []
    while True:
        time.sleep(0.1)
        if os.path.getsize(path) != fsize:
            with open(path, "r") as f:
                log = f.readlines()
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