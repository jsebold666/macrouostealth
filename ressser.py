#agradecimentos à: |||ShadowRunner||| |||JiNx||| |||Quaker||| por suas contribuições no código... 
from py_stealth.methods import FindCount
from modules import *
from modules.common_utils import *
from py_stealth import (
    CastToObject,
    Wait,
    IsDead,
    UseType,
    WaitForTarget,
    TargetToObject,
    GetMana,
    Self,
    GetMaxHP,
    GetHP,
    IsPoisoned,
    FindTypesArrayEx,
    GetDistance,
    IsObjectExists,
    IsHidden,
    GetFindedList,
    SetFindDistance,
    SetFindVertical,
    IsTrade,
    GetTradeContainer,
    TradeCount,
    GetTradeOpponent,
    GetTradeOpponentName,
    FindType,
    UOSay,
    CancelTrade,
    ConfirmTrade,
    GetType,
    Backpack,
    FindItem,
    UseObject,
    MoveItem,
    GetTooltip,
    StealthPath,
    GetClilocByID
 )
from datetime import (
    datetime,
    timedelta
 )  
 


players = [0x0009AF6A, 0x21441, 0xa8465, 0x9af6a, 0x5fe72, 0x11fe28, 0x80285, 0xb6ea9, 0xa8465, 0x3df2a, 0xa72bb, 0x3b10b, 0x3e336, 0x17ad, 0xfc6a9, 0x54a53, 0x7173c, 0x120587, 0x21441, 0xbe78e, 0x66144, 0x31b92, 0xc1132, 0xad741, 0x1b40f9, 0x1b40f9, 0x10b10c, 0x8ba9e, 0x82a, 0xd9d5c, 0xabce3, 0x140513, 0x94715, 0x1282d5, 0x458c4, 0x133a62, 0x5c9d0, 0x7173c ]
pets = [0x1b18d8, 0x000BC6AB, 0x154f51, 0xfe661, 0x00065E68, 0xb58ba, 0x14f1e3, 0x8ee, 0x127847, 0x609ee, 0xcc ]
carp_type = [0x0E89, 0x0DF0]
skit_type = 0x0F9D
saw_type = 0x1034
tink_type = 0x1eb8
wait_time = 1200 #Default Wait Time
wait_lag_time = 1200 #Default Wait Lag Time
action_wait = 1200
color = [-1]
container = [-1]

def msg_disco(msg):
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=str(msg))
    webhook.execute()
    return

def find_players(distance = 5, vdistance = 8):
    SetFindDistance(distance)
    SetFindVertical(vdistance)
    listOfFinded = players
    return listOfFinded

def cure_players(players):
    for player in players:
        while IsPoisoned(player):
            if GetMana(Self()) >= 8:
                last_action = datetime.now()
                CastToObject("Arch Cure", player)
                Wait(2850)
            

def ress_players(players):
    for player in players:
        if GetDistance(player) < 2:
            while IsDead(player):  
                CastToObject('Resurrection', player)
                #UOSay('FUCK SHADOWSTRIKERS')
                WaitTargetObject(player)
                Wait(action_wait*2)
                Wait(2000)


def heal_players(players):
    SetFindDistance(10)
    for player in players:
        if GetHP(player) < GetMaxHP(player):
            if not IsDead(player):
                #last_action = datetime.now()
                CastToObject("Greater Heal", player)
                WaitTargetObject(player)  
                Wait(action_wait*2)
                Wait(1800)
                return

def heal_self():
    if GetHP(Self()) < GetMaxHP(Self()) and not IsDead(Self()):
        last_action = datetime.now()
        Cast('Heal')
        WaitTargetObject(Self())
        Wait(action_wait*2)
        Wait(1000)
        return



def find_pets(distance = 2, vdistance = 4):
    SetFindDistance(distance)
    SetFindVertical(vdistance)
    listOfFinded = pets
    return listOfFinded


def ress_pets(pets):
    IgnoreReset()
    find_pets()
    for pet in pets: 
        for player in players:
            if IsObjectExists(pet) and GetHP(player) > 0:
                if GetHP(pet) == 0:
                    UseType(0xe21, 0xFFFF)
                    WaitTargetObject(pet)
                    Wait(2850)
                elif GetHP(pet) > 0 and GetHP(pet) < GetMaxHP(pet):
                    if IsPoisoned(pet):
                        if GetMana(Self()) >= 8:
                            CastToObject("Arch Cure", pet)
                            Wait(2850) 
                    else:
                        CastToObject("Greater Heal", pet)
                        WaitTargetObject(pet)  
                        Wait(action_wait*2)
                        Wait(1800)
                else:
                    break
        else:
            Ignore(pet)

def hidding_self():
    for player in players:
        for pet in pets:
            #if not IsObjectExists(player) or GetHP(player) == GetMaxHP(player):
            if GetHP(player) == GetMaxHP(player):
                if GetHP(pet) == GetMaxHP(pet):
                    if not IsHidden(Self()):
                        if not IsTrade():
                            UseSkill('Hiding')
                            Wait(1000)
                else:
                    break
            else:
                break
        break

if __name__ == '__main__':
    while True:
        global HELP_MSG_TIMER
        starttime = datetime.now() - timedelta(seconds=1) 
        if check_timer(datetime.now() - timedelta(minutes=2), 80000000):
            HELP_MSG_TIMER = datetime.now()
            UOSay("Hello! I'm a official announcer O guild.")
            AddToSystemJournal("Hello! I'm a official announcer O guild.")
            UOSay("I declare that bcrowley and thiago have a peru pequeno")
            AddToSystemJournal("I declare that bcrowley and thiago have a peru pequeno") 
        heal_self()
        cure_players(find_players())
        ress_players(find_players())
        heal_players(find_players())
        ress_pets(find_pets())
        #handle_trade()