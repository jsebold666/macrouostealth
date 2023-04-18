# ======================================================================================================================
# Author: Joey Inspired on Half-Life(br) macro.
# Description: Script de coleta de BODS.
# Por padrão, coleta baud, ferreiro e taylor.
# Escrito para RunUO.
# Server UO DEMISE.
# UOStealthClientVersion: 7.3.1;
# ======================================================================================================================

from stealth import *
from datetime import datetime, timedelta
from time import sleep

TAILOR_VENDOR = 0xb0278  # ID NPC Taylor.
BLACKSMITH_VENDOR = 0xb0299  # ID NPC Blacksmith.
VENDOR_CONTEXT_MENU = 1  # O número do item do menu de contexto responsável por capturar o baud de Taylor.
BOD_TYPE = 0x2258
BODTYPES = [0x2258]  # Grafico da BOD.
TAILOR_BOD_COLOR = 1155  # Cor da BOD de Taylor.
LIST_BOD_COLLORS = [1155, 1102]
BLACKSMITH_BOD_COLOR = 1102  # Cor da BOD de BS.
TAKE_TAILOR = False  # True pega BODS de Tailor, False Nao Pega de Tailor.
TAKE_BLACKSMITH = True  # True pega BODS de BS, False Nao Pega de BS.
TAILOR_BOOK = 0  # ID livros nos quais trabalhar taylor bods. Se o valor for 0, o baud vai para a mochila.
BLACKSMITH_BOOK = 0  # ID livros nos quais trabalhar BS bods. Se o valor for 0, o baud vai para a mochila.
TAILOR_MSG = 'Taking Tailor BOD'
BLACKSMITH_MSG = 'Taking BS BOD'
WAIT_TIME = 500  # Tempo mínimo de atraso. Melhor não mudar.
WAIT_LAG_TIME = 10000  # O tempo que ficará esperando a defasagem. Melhor não mudar..
BOOK_LIMIT = 500

MY_PROFILES = [
    'mimers5'
    'bot7', 
     'bot7-2', 
    'bot7-3', 
    'bot7-4', 
    'bot7-5', 
    'bot7-6', 
    'bot7-7', 
    'bot8', 
     'bot8-2', 
    'bot8-3', 
    'bot8-4', 
    'bot8-5', 
    'bot8-6', 
    'bot8-7',
    'bot9', 
     'bot9-2', 
    'bot9-3', 
    'bot9-4', 
    'bot9-5', 
    'bot9-6', 
    'bot9-7',
    'bot10', 
     'bot10-2', 
    'bot10-3', 
    'bot10-4', 
    'bot10-5', 
    'bot10-6', 
    'bot10-7',
        'mimers4'

    ]

tailor_bods, blacksmith_bods = 0, 0

def wait_lag(wait_time=WAIT_TIME, lag_time=WAIT_LAG_TIME):
    Wait(wait_time)
    CheckLag(lag_time)
    return None

def open_backpack():
    check_save()
    UseObject(Backpack())
    Wait(1500)

def check_save():
    if (InJournal('world will save') > -1):
        while not (InJournal('world save complete') > -1):
            Wait(1000)
        ClearJournal()

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

def findNamedBook(searchStr):
    res = FindTypeEx(8793, 0, Backpack(), False)
    FoundBooks = GetFindedList()
    for book in FoundBooks:
        check_save()
        tooltip = GetTooltip(book)
        if searchStr in tooltip:
           return book
        else:
            print('Vai mudar o nome')
            SetContextMenuHook(book,0)
            RequestContextMenu(book)
            Wait(1500)
            ConsoleEntryUnicodeReply((searchStr+"\r"))
            Wait(1500)
    return 0

def MoveBodToBook():
    print('Identificando Deeds')
     
    smithBook = findNamedBook('BS') # find our smith book
    while FindTypeEx(8792, 1102, Backpack(), False) > 0:  # Get all smith bods
        check_save()
        FoundSmithBods = GetFindedList()
        print('Deed Encontrado, Movendo pro Book')
        for bod in FoundSmithBods :
            check_save()
            MoveItem(bod, 0, smithBook , 0, 0, 0)
            Wait(1000)
            print(f'BlackSmith Book Deeds: {AnalyzeBodBook(smithBook)}')  
        return   
        print(f'BlackSmith Book Deeds: {AnalyzeBodBook(smithBook)}')                      

def AnalyzeBodBook(objid):
    global BOOK_LIMIT

    if not objid:
        return False 
             
    qty_deeds = Property(objid,'Deeds in book')  
    return qty_deeds  

def close_gumps():
    while IsGump():
        if not Connected():
            return False
        if not IsGumpCanBeClosed(GetGumpsCount() - 1):
            return False
        CloseSimpleGump(GetGumpsCount() - 1)
    return True

class Boder(object):
    def __init__(self, name):
        self.name = name
        self.time_order = datetime.now()
        self.backpack_item_count = 0

    @staticmethod
    def get_bods_count(bod_color):
        if bod_color == TAILOR_BOD_COLOR:
            global tailor_bods
            tailor_bods = CountEx(BOD_TYPE, bod_color, Backpack())
            AddToSystemJournal('Quantidade de Taylor BOD na Bag = {0}'.format(tailor_bods))
        else:
            global blacksmith_bods
            blacksmith_bods = CountEx(BOD_TYPE, bod_color, Backpack())
            AddToSystemJournal('Quantidade de Blacksmith BOD na Bag = {0}'.format(blacksmith_bods))

    def check_backpack(self):
        backpack_item_count = GetTooltipRec(Backpack())
        for item in backpack_item_count:
            check_save()
            if len(item['Params']) == 4:
                self.backpack_item_count = int(item['Params'][0])
                break
        if self.backpack_item_count >= 125:
            check_save()
            AddToSystemJournal('{0} Mochila Cheia'.format(self.name))
            return True
        return False

    def collect_bods(self, msg, vendor, menu, bod_color, bod_book):
        while True:
            check_save()
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
                    Wait(1500)
                    check_save()
                    close_gumps()
            if InJournalBetweenTimes('in your backpack|may be available in about', start_time,
                                     datetime.now()) > 0:
                break
        self.get_bods_count(bod_color)
        return None


if __name__ == '__main__':
    ClearJournal()
    ClearSystemJournal()
    if not TAKE_TAILOR and not TAKE_BLACKSMITH:
        quit(AddToSystemJournal('Pelo menos um dos parâmetros TAKE_TAILOR ou TAKE_BLACKSMITH deve ser True.' +
                                'Script Parado!!!'))
    for i in range(len(MY_PROFILES)):
        MY_PROFILES[i] = Boder(MY_PROFILES[i])
    while True:
        for profile in MY_PROFILES:
            if datetime.now() > profile.time_order:
                ChangeProfile(profile.name)
                SetARStatus(True)
                Connect()
                Wait(5000)
                while not Connected():
                    Wait(500)
                check_save()
                if not profile.check_backpack():
                    close_gumps()
                    if TAKE_TAILOR:
                        profile.collect_bods(TAILOR_MSG,
                                             TAILOR_VENDOR,
                                             VENDOR_CONTEXT_MENU,
                                             TAILOR_BOD_COLOR,
                                             TAILOR_BOOK)
                    if TAKE_BLACKSMITH:
                        profile.collect_bods(BLACKSMITH_MSG,
                                             BLACKSMITH_VENDOR,
                                             VENDOR_CONTEXT_MENU,
                                             BLACKSMITH_BOD_COLOR,
                                             BLACKSMITH_BOOK)
                else:
                    profile.get_bods_count(TAILOR_BOD_COLOR)
                    profile.get_bods_count(BLACKSMITH_BOD_COLOR)
                    MY_PROFILES.remove(profile)
                MoveBodToBook()
                SetARStatus(False)
                while Connected():
                    Disconnect()
                    Wait(500)
                profile.time_order = datetime.now() + timedelta(hours=1)
                if len(MY_PROFILES) == 0:
                    AddToSystemJournal('Script parado bag cheia')
                    quit('Stop')
                if profile == MY_PROFILES[-1]:
                    tailor_bods, blacksmith_bods = 0, 0

        sleep(1)