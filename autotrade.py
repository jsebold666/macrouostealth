#by Joey  teste
from stealth import *
from datetime import datetime, timedelta
from time import sleep
from py_stealth import ( ConfirmTrade )


TAILOR_VENDOR = 0xb0278  # ID NPC Taylor.
BLACKSMITH_VENDOR = 0xb0299  # ID NPC Blacksmith.
VENDOR_CONTEXT_MENU = 1  # O número do item do menu de contexto responsável por capturar o baud de Taylor.
BOD_TYPE = 0x2258  # Grafico da BOD.
TAILOR_BOD_COLOR = 1155  # Cor da BOD de Taylor.
BLACKSMITH_BOD_COLOR = 1102  # Cor da BOD de BS.
TAKE_TAILOR = False  # True pega BODS de Tailor, False Nao Pega de Tailor.
TAKE_BLACKSMITH = True  # True pega BODS de BS, False Nao Pega de BS.
TAILOR_BOOK = 0x2259  # ID livros nos quais trabalhar taylor bods. Se o valor for 0, o baud vai para a mochila.
BLACKSMITH_BOOK = 0x2259  # ID livros nos quais trabalhar BS bods. Se o valor for 0, o baud vai para a mochila.
TAILOR_MSG = 'Taking Tailor BOD'
BLACKSMITH_MSG = 'Taking BS BOD'

WAIT_TIME = 500  # Tempo mínimo de atraso. Melhor não mudar.
WAIT_LAG_TIME = 10000  # O tempo que ficará esperando a defasagem. Melhor não mudar..
COLLECTOR = 0xc64a8
MY_PROFILES = ['mimers', 'mimerss', 'mimersss', 'mimersss', 'mimerssssb', 'mimerssss', 'mimerssssd', 'mimerssssw', 'mimersssswf', 'mimersssswfgg', 'jezzy666tt', 'mestre', 'mimersssswfggfff', 'mimersssswfggfffb',
'novo', 'tailorbod',  'tailorbod2', 'tailorbod3', 'tailorbod4' , 'tailorbod6', 'tailorbod8', 'tailorbod9', 'tailorbod10', 'mimersssswfggfffboo']

tailor_bods, blacksmith_bods = 0, 0

def get_bods_count(bod_color):
    if bod_color == TAILOR_BOD_COLOR:
        global tailor_bods
        tailor_bods = CountEx(BOD_TYPE, bod_color, Backpack())
        AddToSystemJournal('Quantidade de Taylor BOD na Bag = {0}'.format(tailor_bods))
    else:
        global blacksmith_bods
        blacksmith_bods = CountEx(BOD_TYPE, bod_color, Backpack())
        AddToSystemJournal('Quantidade de Blacksmith BOD na Bag = {0}'.format(blacksmith_bods))


def collect_bods(msg, vendor, menu, bod_color, bod_book):
    while True:
        start_time = datetime.now()
        AddToSystemJournal(msg)
        wait_lag(WAIT_TIME // 2)
        SetContextMenuHook(vendor, menu)
        wait_lag(WAIT_TIME // 2)
        RequestContextMenu(vendor)
        wait_lag()
        WaitGump('1')
        wait_lag()
        if bod_book:
            while FindTypeEx(BOD_TYPE, bod_color, Backpack(), False) > 1:
                MoveItem(FindItem(), 1, bod_book, 0, 0, 0)
                wait_lag()
                close_gumps()
        if InJournalBetweenTimes('in your backpack|may be available in about', start_time,
                                    datetime.now()) > 0:
            break
    get_bods_count(bod_color)
    return None

def close_gumps():
    while IsGump():
        if not Connected():
            return False
        if not IsGumpCanBeClosed(GetGumpsCount() - 1):
            return False
        CloseSimpleGump(GetGumpsCount() - 1)
    return True

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
    if len(founds) > 1:
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
        self.name = name
        self.time_order = datetime.now()
        self.backpack_item_count = 0

    @staticmethod
    def movebooks():

        open_backpack()
        
        while FindTypeEx(0x2259, 0xFFFF, Backpack(), False) == 0:
            bookfinded = GetFindedList()
            
            while IsTrade():
                ConfirmTrade(TradeCount()-1)
                Wait(5000)
            break

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
                Wait(1000)
            if len(MY_PROFILES) == 0:
                AddToSystemJournal('Script parado')
                quit('Trade COMPLETO')
        sleep(1)