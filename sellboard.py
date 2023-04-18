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
       
first_run = True
CURRENT_BALANCE = 0
CHECKS_IN_BANK = 0
current_tithing_points = utils.get_current_tithing_points()
CHAR_BANK_LOCATION = ""
CHAR_BANK_ID = ""
MAX_WEIGHT = MaxWeight()
WEIGHT_LIMIT = MaxWeight() - 5
NPC_VENDOR = ""
NPC_VENDOR_FOUND = False
NPC_VENDOR_NAME = ""
bank = ObjAtLayer(BankLayer())
number_of_disconnections = 0
last_disconnection = ""

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/928045914965291138/rqeIFhtb_d8J_KB5iMF1AVsT9tw5J3EUochwmK0VuDNgwJIkzUa4z69JisEG5QYpBQRU'

SELL_WOOD = True

def move_gold_to_bank(bank):
    FindType(types.GOLD, Backpack())
    amount_of_gold_being_unloaded = FindFullQuantity()
    utils.debug(
        "** DEPOSITING ** Unloading %d gold in bank" % (amount_of_gold_being_unloaded)
    )

    starttime = datetime.now()
    while confirm_script_loop_conditions() and FindType(types.GOLD, Backpack()):
        MoveItem(FindItem(), 65000, bank, 0, 0, 0)
        utils.wait_lag(600)
        if utils.check_timer(starttime, 8000):
            utils.debug(
                "More than 8 seconds waiting to move gold to bank. Probably lag..."
            )
            break

    return True
    
def confirm_script_loop_conditions():
    if Dead():
        return False
    if not Connected():
        return False

    return True

def deposit_gold_in_bank():
    utils.wait_lag(50)

    utils.wait_lag(50)
    bank = ObjAtLayer(BankLayer())

    if bank and SELL_WOOD:
        if count(types.GOLD):
            move_gold_to_bank(bank)
        else:
            utils.debug(
                "Char is in bank without gold in backpack. Something went wrong"
            )

        if utils.make_check(1000000):
            utils.debug("%s just made a 1kk check!" % (char_name))
            checks_in_bank = count_colored(CHECK, types.CHECK_COLOR, bank)
            try:
                PlayWav(CASH_SOUND)
                webhooks.send_discord_message(
                    DISCORD_WEBHOOK_URL,
                    "**1KK CHECK** %s just made a 1kk check! Checks in bank: %d"
                    % (char_name, checks_in_bank),
                )
            except:
                pass


        Sell()

        if DROP_MONEY_TO_MAIN_CHAR:
            drop_money_to_main_char_maybe()

        # print statistics
        print_script_stats()

    return True

def sell_boards_to_carpenter():
    global NPC_VENDOR
    global NPC_VENDOR_NAME
    utils.debug("Going to the vendor to sell boards.")
    # adding this wait here baecause char was getting stuck on "You Must wait to perform another action"
    utils.wait_lag(50)

    carpenter = ""

  
    if not NPC_VENDOR:
        NPC_VENDOR = npc.find_vendor("carpenter")
        utils.wait_lag(10)
    else:
        # get npc name once
        if not NPC_VENDOR_NAME:
            NPC_VENDOR_NAME = GetAltName(NPC_VENDOR)
        utils.debug("Reusing previous vendor: %s " % (NPC_VENDOR_NAME))

    # to print how much was sold afterwards
    boards_in_backpack = count_common(types.BOARD)

    if NPC_VENDOR:
        start_time = datetime.now()

        while confirm_script_loop_conditions() and count_common(types.BOARD) > 0:
            if utils.check_timer(start_time, 60000):
                utils.debug("Timeout selling boards to vendor...")
                break

            NPC_DISTANCE_LIMIT = 10
            initial_npc_distance = GetDistance(NPC_VENDOR)
            while (
                confirm_script_loop_conditions()
                and GetDistance(NPC_VENDOR) >= NPC_DISTANCE_LIMIT
            ):
                if utils.check_timer(start_time, 20000):
                    utils.debug("Timeout waiting for vendor to get closer Breaking...")
                    break

                if NewMoveXY(GetX(NPC_VENDOR), GetY(NPC_VENDOR), True, 4, True):
                    utils.debug("Moving towards vendor to lower its distance from char")
                utils.debug(
                    "Waiting for vendor to get closer... \nCurrent vendor distance: %d"
                    % (GetDistance(NPC_VENDOR))
                )
                if GetDistance(NPC_VENDOR) != initial_npc_distance:
                    utils.debug(
                        "Vendor moved. Current vendor distance: %d tiles"
                        % (GetDistance(NPC_VENDOR))
                    )
                    initial_npc_distance = GetDistance(NPC_VENDOR)

                Wait(500)

            npc.sell_item_to_npc(types.BOARD, NPC_VENDOR)
            utils.wait_lag(100)
            utils.debug("**SELLING** Selling boards to carpenter")

    if not utils.count(types.BOARD):
        gold_in_backpack = count(types.GOLD)
        if gold_in_backpack > 0:
            utils.debug(
                "Sold %d boards for %d." % (boards_in_backpack, gold_in_backpack)
            )
        return True

    return False


def Sell():
    UOSay('Bank')
    while True:
        AddToSystemJournal('Vai chamar o bank') 
       
        
        bank = ObjAtLayer(BankLayer())
        container_to_search_for_stock = bank
        while confirm_script_loop_conditions() and FindTypeEx(
            types.BOARD, 0, container_to_search_for_stock, True
        ):
            amount_of_boards_to_sell = FindFullQuantity()

            if amount_of_boards_to_sell > 0:
                utils.debug(
                    "Found stock of %d boards in bank." % (amount_of_boards_to_sell)
                )
                start_time = datetime.now()
                while confirm_script_loop_conditions() and not FindTypeEx(
                    types.BOARD, 0, Backpack(), True
                ):
                    if FindTypeEx(types.BOARD, 0, container_to_search_for_stock, True):
                        amount_of_boards_to_carry = MaxWeight() - Weight()
                        utils.debug(
                            "Moving %d boards in backpack to sell"
                            % (amount_of_boards_to_carry)
                        )
                        MoveItem(FindItem(), amount_of_boards_to_carry, Backpack(), 0, 0, 0)
                        utils.wait_lag(600)
                        if utils.check_timer(start_time, 8000):
                            utils.debug(
                                "More than 8 seconds trying to move boards to backpack. Breaking..."
                            )
                            break
                utils.wait_lag(10)

                sell_boards_to_carpenter()
                deposit_gold_in_bank()
            else:
                break
        if not FindTypeEx(types.BOARD, 0, container_to_search_for_stock, True):
            utils.debug("Sold all wood stock in wood storage container!")
        return True

    return False

Sell()