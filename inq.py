from datetime import datetime, timedelta
from discord_webhook import DiscordWebhook
from py_stealth import *

ClearSystemJournal()

urls = [
    "https://discord.com/api/webhooks/847056450714861568/BHiOdK54Z2lQVOb_HLMVrdhYC0b1yIgPMcn9pa5Y4b8l1IQi1LA_WBAb3y3tbkFmr4rV",
    # outro webhook aqui
    "https://discord.com/api/webhooks/844931660272369724/TuwiNWp1AIU0MsiEDmZbcutYhvEPRp3iR1MieBx7E-_4Vgg2ynfs-o7-UlcMDBu3-ruK",
    "https://discord.com/api/webhooks/847056450714861568/BHiOdK54Z2lQVOb_HLMVrdhYC0b1yIgPMcn9pa5Y4b8l1IQi1LA_WBAb3y3tbkFmr4rV",
]


WAV_INQ = "C:\\vUsers\\ferra\\Desktop\\uostealth\\alarm2.wav"

no_inquis_msg = "No inquisitors so far..."
inquis_found_msg = "@everyone Inquisitors ta ai malandro!!! Loga ai pra catar!"


def send_discord(msg):
    webhook = DiscordWebhook(urls, content=str(msg))
    webhook.execute()


PLATEMAIL_GLOVES = 0x1414
INQUISITORS_COLOR = 0x04F2


def check_timer(starttime, time_limit_in_miliseconds):
    currentTime = datetime.now()
    timeDifference = currentTime - starttime
    differenceInMiliseconds = timeDifference.total_seconds() * 1000
    if differenceInMiliseconds > time_limit_in_miliseconds:
        return True
    return False


hourly_msg_timer = datetime.now()
daily_msg_timer = datetime.now()
print("STARTING INQUISITORS SCANNER MACRO...")
while True:
    SetFindVertical(100)
    SetFindDistance(20)
    GetFindVertical()
    GetFindDistance()
    if FindTypeEx(PLATEMAIL_GLOVES, INQUISITORS_COLOR, Ground()):
        PlayWav(WAV_INQ)
        send_discord("@everyone INQUISITORS RESOLUTION SPAWNED! QUICK, ALVIN IS COMING!")
        Wait(5000)
    else:
        # send discord daily to let us know inquis hasnt spawned yet
        if datetime.now() >= daily_msg_timer + timedelta(days=1):
            send_discord(no_inquis_msg)
            print("No inquis so far....")
            daily_msg_timer = datetime.now()

        # print every hour just to keep tracking macro state
        if datetime.now() >= hourly_msg_timer + timedelta(hours=1):
            print("No inquis so far....")
            hourly_msg_timer = datetime.now()