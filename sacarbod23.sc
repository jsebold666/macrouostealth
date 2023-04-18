from stealth import *
from datetime import datetime, timedelta


Profiles = ['mimers', 'mimerss', 'mimersss', 'mimersss', 'mimerssssb', 'mimerssss', 'mimerssssd', 'mimerssssw', 'mimersssswf', 'mimersssswfgg', 'jezzy666tt', 'mestre', 'mimersssswfggfff', 'mimersssswfggfffb', 'mimersssswfggfffbçç', 'novo', 'mimersssswfggfffbdsd', 'tailorbod',  'tailorbod2', 'tailorbod3', 'tailorbod4' , 'tailorbod6', 'tailorbod8', 'tailorbod9', 'tailorbod10']

Tailor = 266315  # Deandra the Tailor
Blacksmith = 266286  # Rhiamon the Blacksmith
BSVendor= $000B0299; 
BSMsg='Taking BS BOD';

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


def RunTo(x, y):
    while x != GetX(Self()) or y != GetY(Self()):
        NewMoveXY(x, y, False, 0, True)
        Wait(1000)


def GoThroughDoor(x, y):
    while x != GetX(Self()) or y != GetY(Self()):
        OpenDoor()
        Wait(1000)
        NewMoveXY(x, y, False, 0, True)
        Wait(500)


def MoveAround():
    RunTo(991, 524)
    RunTo(991, 523)  # So we face the door
    GoThroughDoor(991, 521)
    RunTo(991, 519)
    RunTo(990, 519)
    GoThroughDoor(988, 519)
    RunTo(978, 525)  # Tailor reached
    GetBod(Tailor)
    GetBod(Tailor)
    RunTo(978, 514)  # Blacksmith reached
    GetBod(Blacksmith)
    GetBod(Blacksmith)
    RunTo(987, 518)
    RunTo(988, 518)
    GoThroughDoor(991, 518)
    RunTo(991, 520)
    RunTo(991, 521)
    GoThroughDoor(991, 524)
    RunTo(992, 527)


def GetBod(npc):
    AddToSystemJournal(BSMsg);
    SetContextMenuHook(BSVendor, 1);
    CheckLag(WaitLag);
    RequestContextMenu(BSVendor);
    Wait(WaitTime*2);
    WaitGump('1');
    Wait(WaitTime*4);


def SortBods():
    res = FindTypeEx(8793, 0, Backpack(), False)
    FoundBooks = GetFindedList()
    res = FindTypeEx(8792, 1155, Backpack(), False)  # Tailor
    FoundTailorBods = GetFindedList()
    res = FindTypeEx(8792, 1102, Backpack(), False)  # Blacksmith
    FoundBlacksmithBods = GetFindedList()
    for book in FoundBooks:
        tooltip = GetTooltip(book)
        if 'tailor' in tooltip:
            for tbod in FoundTailorBods:
                MoveItem(tbod, 0, book, 0, 0, 0)
                Wait(100)
        else:
            for bbod in FoundBlacksmithBods:
                MoveItem(bbod, 0, book, 0, 0, 0)
                Wait(100)

def SortBodsFix():
    '''
    tem que ter dois livros.
    :return:
    '''
    tbook = 'tbook' # nome livro tailor
    bsbook = 'bsbook' # nome livro bs
    res = FindTypeEx(8793, 0, Backpack(), False)
    FoundBooks = GetFindedList()
    for book in FoundBooks:
        tooltip = GetTooltip(book)
        if tbook in tooltip:
            tailor = book
        elif bsbook in tooltip:
            bs = book
    tailorbods = FindTypeEx(8792, 1155, Backpack(), False)  # Tailor

# Main body
if __name__ == '__main__':
    DisconnectChar()
    dt = datetime.now() + timedelta(hours=1)
    while True:
        for Char in Profiles:
            changed = ChangeProfile(Char)
            if changed != 0:
                print("Error while changing to profile {}. Result {}".format(Char, changed))
            ConnectChar(Char)
            GetBod(Blacksmith)
            GetBod(Blacksmith)
            SortBods()
            DisconnectChar()
        while dt > datetime.now():
            Wait(30000)
        dt = datetime.now() + timedelta(hours=1)