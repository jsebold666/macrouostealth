#Bods Combiner by Joey, Uostealth version: 9.20

from stealth import *
import re
import modules.common_utils as utils

COLLECTOR = 0xc64a8
HOME_RUNEBOOK_NAME ="home"
TRAVEL_SPELL = "recall"
HOME_RUNE_POSITION = 2

def waitgumpid(gumpid, object, timeout=15):
    maxcounter = 0
    UseObject(object)
    while maxcounter < timeout * 10:
        if IsGump():
            for currentgumpnumb in range(0, (GetGumpsCount())):
                currentgump = GetGumpInfo(currentgumpnumb)
                if 'GumpID' in currentgump:
                    if currentgump['GumpID'] == gumpid:
                        return True
                if IsGumpCanBeClosed(currentgumpnumb):
                    CloseSimpleGump(currentgumpnumb)
        maxcounter += 1
        CheckLag(100000)
    return False

def waitgumpid_press(gumpid, number=0, pressbutton=True, timeout=15):
    maxcounter = 0
    while maxcounter < timeout * 10:
        if IsGump():
            for currentgumpnumb in range(0, (GetGumpsCount())):
                currentgump = GetGumpInfo(currentgumpnumb)
                if 'GumpID' in currentgump:
                    if currentgump['GumpID'] == gumpid:
                        if pressbutton:
                            NumGumpButton(currentgumpnumb, number)
                        else:
                            return currentgump
                        return True
                if IsGumpCanBeClosed(currentgumpnumb):
                    CloseSimpleGump(currentgumpnumb)
        maxcounter += 1
        CheckLag(100000)
    return False

def book_qtd(objid):
    tooltip = GetTooltip(objid)
    respi = re.findall(
        re.compile(r"^.*.Deeds in book: (.*.)\|"),tooltip)
    if respi == []:
        return 0
    return int(respi[0])

def prop_contents(objid):
    tooltip = GetTooltip(objid)
    resp = re.findall(
        re.compile(r"^.*.Contents: (.*.)/125"), tooltip
    )
    if resp == []:
        return 0
    return int(resp[0])

def CloseGumps():
    for i in range(GetGumpsCount()):
        if IsGumpCanBeClosed(i):
            CloseSimpleGump(i)

def recall_home():
    utils.debug("Going home.")
    remount()
    if utils.travel_to(HOME_RUNEBOOK_NAME, TRAVEL_SPELL, HOME_RUNE_POSITION):
        return True

while IsTrade(): 
    print(f'aceita o trade')
    ConfirmTrade(TradeCount()-1)
    Wait(1000) 
    print(f'aceitou o trade') 
booka = None
bookb = None
ClientPrint('choose the book you want to put the bods')
while booka is None:
    ClientRequestObjectTarget()
    WaitForClientTargetResponse(10_000)
    booka = ClientTargetResponse()['ID']
ClientPrint('choose the book you want to take the bods')
while bookb is None:
    ClientRequestObjectTarget()
    WaitForClientTargetResponse(10_000)
    bookb = ClientTargetResponse()['ID']

ClientPrint('Start combine books')
print('Start')
while book_qtd(bookb) > 0:
    waitgumpid(0x54f555df, bookb)
    while prop_contents(Backpack()) <= 123:
        waitgumpid_press(0x54f555df, 5, True)
    while FindTypeEx(0x2258, 0xFFFF, Backpack(), True) > 0:
        listbods = GetFindedList()
        for bod in listbods:
            MoveItem(bod, 1, booka, 1, 1, 0)
            Wait(300)
        CloseGumps()
while FindTypeEx(0x2258, 0xFFFF, Backpack(), True) > 0:
    listbods = GetFindedList()
    for bod in listbods:
        MoveItem(bod, 1, booka, 1, 1, 0)
        Wait(300)
    CloseGumps()
print(book_qtd(booka))
while book_qtd(booka) >= 257:
    recall_home()
    Wait(5000)
    utils.gotToHouse()

   
