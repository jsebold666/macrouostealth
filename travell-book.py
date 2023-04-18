#Bods Combiner by Joey, Uostealth version: 9.20

from stealth import *
import re
import modules.common_utils as utils

COLLECTOR = 0xc64a8
HOME_RUNEBOOK_NAME ="Home"
TRAVEL_SPELL = "recall"
HOME_RUNE_POSITION = 2
BAGS = [
    0x409C8774,
    0x409C876F,
    0x409C877F,
    0x409C877D,
    0x409C8779,
    0x409C877A,
    0x409C8778,
    0x409C877C,
    0x409C877E,
    0x40ED41F7,
    0x409CB263,
    0x409CB260,
    0x409C8771,
    0x409C8772,
    0x409CB26B,
    0x409CB25E,
    0x409C8770,
    0x409CB266,
    0x409CB258,
    0x409C877B
]

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
    utils.travel_to(HOME_RUNEBOOK_NAME, TRAVEL_SPELL, HOME_RUNE_POSITION)

while IsTrade(): 
    print(f'aceita o trade')
    ConfirmTrade(TradeCousnt()-1)
    Wait(1000) 
    print(f'aceitou o trade') 
booka = None
SetARStatus(True)
ClientPrint('choose the book you want to put the bods')
while booka is None:
    ClientRequestObjectTarget()
    WaitForClientTargetResponse(10_000)
    booka = ClientTargetResponse()['ID']
ClientPrint('choose the book you want to take the bods')

print(book_qtd(booka))
while book_qtd(booka) >= 256:
    recall_home()
    Wait(5000)
    x = 1247
    y = 1204
    while x != GetX(Self()) or y != GetY(Self()):
        utils.gotToHouse()
        utils.gotToHouse2()
        utils.gotToHouse3()
    
    i[0] for i, bag in BAGS:
        print(f'entrou no for') 
        if prop_contents(BAGS[i]) < 100:
            print(f"vai mover {bag}")
            if BAGS[:1]
                UseObject(bag)
                MoveItem(booka, 1, BAGS[i], 0, 0, 0)

   
