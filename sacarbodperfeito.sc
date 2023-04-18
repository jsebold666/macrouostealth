from stealth import *
import sys
import os
from datetime import datetime, timedelta
from random import randrange
try:
    from modules.common_utils import (
            debug,
            count,
            count_common,
            count_colored,
            wait_lag,
            remove_death_robe,
            is_set_equiped,
            dress_char_set,
            save_char_set,
            check_timer,
            get_item_name,
            get_nearby_mobs,
            drop_type,
            drop,
            make_check,
            find_commodity_deed_box_on_ground,
            go_to_britain_via_help_request,
            go_to_britain_bank_vendor_mall_moongate,
        )
    import modules.common_utils as utils

    from modules.types import (
            GOLD,
            BOARD,
            LOG,
            HATCHET,
            SPECIAL_LUMBER_RESOURCES,
            TREES,
            LUMBER_RESOURCES_TYPES,
            AXES,
            CHECK,
            CHECK_COLOR,
            AGRESSIVE_MOBS,
        )
    import modules.types as types  
    import modules.common_utils as utils

    from modules.connection import get_char_name, print_uptime
    import modules.connection as connection

    from modules.ress import ress
    import modules.ress as ress

    from modules.webhooks import send_discord_message
    import modules.webhooks as webhooks

    from modules.afk_check import is_afk_gump
    import modules.afk_check as afk

    from modules.gm import is_gm_present
    import modules.gm as gm

    from modules.jail import is_char_in_6_hours_jail, is_char_in_jail, escape_jail
    import modules.jail as jail

    from modules.gumps import close_gumps
    import modules.gumps as gumps

    from modules.insurance import is_set_insured
    import modules.insurance as insurance

    from modules.npc_and_vendors import is_npc, find_vendor, sell_item_to_npc
    import modules.npc_and_vendors as npc

    from modules.regions import in_region
    import modules.regions as regions

except Exception as err:
    debug("****************************")
    debug(">>> PYTHON IMPORT ERROR:")
    debug(f"Error importing macro module: {err}")
    # disable exit traceback for a clean log
    sys.tracebacklimit = 0
    debug("****************************")
    exit("Check errors above")   

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/932216381712265226/YL-zUeH6Ujgqpa2ODqp2MjA9UOoE5XySWAHbDF8_rW3DCU6DoncPHbMFSwPHlj40tqv7'

Profiles = ['said36-1', 'said36-2', 'said36-3', 'said36-4', 'said36-5', 'said36-6', 'said36-7',
            'Maquinote-1', 'Maquinote-2', 'Maquinote-3', 'Maquinote-4', 'Maquinote-5', 'Maquinote-6', 'Maquinote-7']

Tailor = 266315  # Deandra the Tailor
Blacksmith = 266286  # Rhiamon the Blacksmith


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
    GetBod()
    GetBod()
    RunTo(978, 514)  # Blacksmith reached
    GetBod()
    GetBod()
    RunTo(987, 518)
    RunTo(988, 518)
    GoThroughDoor(991, 518)
    RunTo(991, 520)
    RunTo(991, 521)
    GoThroughDoor(991, 524)
    RunTo(992, 527)


def GetBod():
    NPC_VENDOR = npc.find_vendor("blacksmith")
    RequestContextMenu(npc)
    SetContextMenuHook(npc, 1)
    Wait(1000)
    WaitGump('1')
    Wait(2000)


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
             try:
                webhooks.send_discord_message(
                    DISCORD_WEBHOOK_URL,
                    "**bod de bs coletada com sucesso** %s com sucesso %d"
                    % (char_name),
                )
            except:
                pass

def SortBodsFix():
    '''
    Deben haber dos libros unos para tailor y otro para bs.
    :return:
    '''
    tbook = 'tbook' # Nombre del libro de tailor
    bsbook = 'bsbook' # Nombre del libro de bs
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
            GetBod()
            GetBod()
            SortBods()
            DisconnectChar()
        while dt > datetime.now():
            Wait(30000)
        dt = datetime.now() + timedelta(hours=1)