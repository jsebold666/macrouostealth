#by Joey
from stealth import *
from datetime import datetime, timedelta
from time import sleep


WAIT_TIME = 500  # Tempo mínimo de atraso. Melhor não mudar.
WAIT_LAG_TIME = 10000  # O tempo que ficará esperando a defasagem. Melhor não mudar..
COLLECTOR = 0x12d2a8
MY_PROFILES = ['mimers', 
'mimerss', 
'mimersss', 
'mimerssss', 
'mimerssssd',
'mimerssssb',
'mimerssssw', 
'mimersssswf', 
'mimersssswfgg', 
'jezzy666tt', 
'mestre', 
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
'tailorbod10',
'mimers2',
'mimers3',
'mimers4',
'mimers5']

def wait_lag(wait_time=WAIT_TIME, lag_time=WAIT_LAG_TIME):
    Wait(wait_time)
    CheckLag(lag_time)
    return None

def Property(objid=None, name=None):
    tooltip = GetTooltip(objid)   
    properties = tooltip.upper().split("|") 
    for i, property in enumerate(properties):
        check_save()
        if name.upper() in property:
            if ': ' in property:
                prop = property.split(': ')
                propname = prop[0]
                propvalue = int(prop[1]) 
                return propvalue
            else:
                print('[Property] Error: Invalid', property)

def open_backpack():
    check_save()
    UseObject(Backpack())
    Wait(1500)

def check_save():
    if (InJournal('world will save') > -1):
        while not (InJournal('world save complete') > -1):
            Wait(1000)
        ClearJournal()

def CloseGumps():
    for i in range(GetGumpsCount()):
        if IsGumpCanBeClosed(i):
            CloseSimpleGump(i)

def count_books_on_trade():
    tradeContainer = GetTradeContainer(TradeCount()-1,2)
    FindType(0xFFFF, tradeContainer)
    founds = GetFindedList()
    if len(founds) > 80:
        return True
    else:
        return False

def accept_trade():
    if count_books_on_trade() is True:
        ConfirmTrade(TradeCount()-1)
    else:
        return False

def book_count():
    tradeContainer = GetTradeContainer(TradeCount()-1,2)
    FindType(0xFFFF, tradeContainer)
    founds = GetFindedList()
    if len(founds):
        return len(founds)
    else:
        return False

def Is_Range():
    if IsObjectExists(COLLECTOR):
        collectorrange = GetDistance(COLLECTOR)
        if collectorrange <= 2:
            return True
        else:
            return False
    else:
        return False
class Boder(object):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def movebooks():
        countbook = 0
        if Is_Range():
            while countbook < 2:
                if FindTypeEx(0x2259, 0xFFFF, Backpack(), False):
                    bookfinded = GetFindedList()
                    for book in bookfinded:
                        qtd = Property(book, 'Deeds in Book:') 
                        print(f'qtd: {qtd}')
                        if qtd > 230:
                            print(f'Deeds in Book: {qtd}')  
                            print(f'move o book')
                            MoveItem(book, 1, COLLECTOR, GetX(COLLECTOR), GetY(COLLECTOR), GetZ(COLLECTOR))
                            Wait(2000)
                            countbook + 1
                        else:
                            print(f'Deeds in Book: {qtd} - Logging the next char')
                            break
                    break
        while IsTrade(): 
            print(f'aceita o trade')
            ConfirmTrade(TradeCount()-1)
            Wait(1000) 
            print(f'aceitou o trade')
            break    
        while not Is_Range:
            print(f'not in range')
            Wait(1000)

if __name__ == '__main__':
    ClearJournal()
    ClearSystemJournal()
    for i in range(len(MY_PROFILES)):
        MY_PROFILES[i] = Boder(MY_PROFILES[i])
    while True:
        for profile in MY_PROFILES:
            ChangeProfile(profile.name)
            SetARStatus(True)
            Connect()
            Wait(2000)
            while not Connected():
                Wait(5000)
            check_save()
            open_backpack()
            if not profile.movebooks():
                check_save()
                MY_PROFILES.remove(profile)
            SetARStatus(False)
            while Connected():
                    Disconnect()
                    Wait(500)
            profile.time_order = datetime.now() + timedelta(hours=1)
            if len(MY_PROFILES) == 0:
                AddToSystemJournal('Script parado')
                quit('Trade COMPLETO')
        sleep(1)