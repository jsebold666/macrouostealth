from py_stealth import *
from stealth import *
from datetime import datetime, timedelta
from discord_webhook import DiscordWebhook  # pip install discord-webhook
hookurl = 'https://discord.com/api/webhooks/1084518909329289398/Cj1tmArGE5fdQj1BXqV3JK42PPzZXJ8PDPw58ney5FTEjAUJak6ajfoDUFBrwB2RkXhz'

############################################################################################
#Rememeber these need to be named the same HERE as you name them to login using stealth
############################################################################################
Profiles = ['bot3',
    'bot3-1',
    'bot3-2',
    'bot3-4',
    'bot3-5',
    'bot3-6',
    'bot3-7',
    'bot4',
     'bot4-2',
    'bot4-3',
    'bot4-4',
    'bot4-5',
    'bot4-6',
    'bot4-7',
    'bot5',
     'bot5-2',
    'bot5-3',
    'bot5-4',
    'bot5-5',
    'bot5-6',
    'bot5-7',
     'bot6-2',
    'bot6-3',
    'bot6-4',
    'bot6-5',
    'bot6-6',
    'bot6-7']


############################################################################################
Tailor = 0x0009B52A  # Serial of Luna tailor/weaver  (NOT THE GUILDMASTERS)
Blacksmith = 0x0009B4F7  # Serial of Luna Blacksmith (NOT THE GUILDMASTERS)
WAIT_TIME = 500

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

def ConnectChar(profile):
    print("Connecting with profile {}".format(profile))
    while not Connected():
        Connect()
        Wait(10000)
    print("{} connected".format(profile))


def DisconnectChar():
    print("Disconnecting...")
    while Connected():
        Disconnect()
        Wait(10000)
    print("Disconnected")


def GetBod(npc):
    RequestContextMenu(npc)
    Wait(600)
    SetContextMenuHook(npc, 1)
    Wait(1000)
    WaitGump('1')
    Wait(2000)


def SortBods():
    res = FindTypeEx(8793, 0, Backpack(), False)
    FoundBooks = GetFindedList()
    res = FindTypeEx(8792, 1155, Backpack(), False)  # Tailor
    if res != 0:
        FoundTailorBods = GetFindedList()
    else:
        FoundTailorBods = []
    res = FindTypeEx(8792, 1102, Backpack(), False)  # Blacksmith
    if res != 0:
        FoundBlacksmithBods = GetFindedList()
    else:
        FoundBlacksmithBods = []
    for book in FoundBooks:
        tooltip = GetTooltip(book)
        print(tooltip)
        # Dividir a string em uma lista de substrings
        substrings = tooltip.split("|")
        deeds_in_book = ""
        # Procurar a substring que começa com "Deeds in book:"
        for substring in substrings:
            if substring.startswith("Deeds in book:"):
                # Extrair o valor numérico
                deeds_in_book = int(substring.split(":")[1])
                break
        if (str(deeds_in_book) >= str(498)):
          discosend(GetName(Self()) + " bods in books " + str(deeds_in_book))
        if 'Tailor' in tooltip:
            for tbod in FoundTailorBods:
                MoveItem(tbod, 0, book, 0, 0, 0)
                Wait(1000)
        else:
            for bbod in FoundBlacksmithBods:
                MoveItem(bbod, 0, book, 0, 0, 0)
                Wait(1000)


# Main body
if __name__ == '__main__':
    print()
    WAIT_TIME = datetime.now()
    # Print while wait the time
    while True:
        if WAIT_TIME > datetime.now():
            teste = 'await'
        else:
            print('Starting Script')
            for Char in Profiles:
                changed = ChangeProfile(Char)
                if changed != 0:
                    print("Error while changing to profile {}. Result {}".format(Char, changed))
                ConnectChar(Char)
                ##GetBod(Tailor)
                GetBod(Blacksmith)
                ClickOnObject(Backpack())
                SortBods()
                DisconnectChar()
                #print("check1")
            WAIT_TIME = datetime.now() + timedelta(minutes = 60)
            #print("afterwait")
        Wait(1000)