from py_stealth import *
from stealth import *
from datetime import datetime, timedelta

############################################################################################
#Rememeber these need to be named the same HERE as you name them to login using stealth
############################################################################################
Profiles = ['mimers',
    'mimerss',
    'mimersss',
    'mimerssss',
    'mimerssssd',
    'mimerssssb',
    'mimerssssw',
    'mimersssswf',
    'mimersssswfgg',
    'jezzy666tt',
    'mimersssswfggfff',
    'mimersssswfggfffb',
    'novo',
    'mimersssswfggfffbdsd',
    'tailorbod',
    'tailorbod2',
    'tailorbod3',
    'tailorbod4',
    'tailorbod6',
    'tailorbod8',
    'tailorbod9',
    'tailorbod10']


############################################################################################
Tailor = 0x0009B52A  # Serial of Luna tailor/weaver  (NOT THE GUILDMASTERS)
Blacksmith = 0x0009B4F7  # Serial of Luna Blacksmith (NOT THE GUILDMASTERS)
WAIT_TIME = 500

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
            print('Waiting for BOD cycle..')
        else:
            print('Starting Script')

            GetBod(Tailor)
            GetBod(Blacksmith)
            ClickOnObject(Backpack())
            SortBods()
            #print("check1")
            WAIT_TIME = datetime.now() + timedelta(minutes = 60)
            #print("afterwait")
        Wait(1000)