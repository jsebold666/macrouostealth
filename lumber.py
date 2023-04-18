"""
UO STEALTH AUTO LUMBERJACKING BOT
by gugutz.

Version: 1.1.0
Based on original script by scripting master Quaker
"""

import sys
import os
from datetime import datetime, timedelta
from random import randrange


try:
    from py_stealth import *

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


ClearSystemJournal()

char = Self()
bank = ObjAtLayer(BankLayer())
backpack = Backpack()
####################################################################
# CONFIGURATION

# protection if UOStealth don't find your name. LAG is the main reason
connection.get_char_name()

PLAY_SOUNDS = False

config = {}
config[CharName()] = {
    # general options
    "sell_wood": True,
    "unload_boards_at_bank": True,
    "store_checks_at_home": False,
    "wood_storage_container": 0,
    "auto_reequip_set": True,
    "auto_refill_tithing_points": True,
    "minimum_tithing_points": 3000,
    "fast_cash": False,
    "sell_board_stock": True,
    # !!!!!!!  CHANGE DISCORD WEBHOOK HERE  !!!!!!!
    "discord_webhook_url": "https://discord.com/api/webhooks/844530195041615882/oqpkPJFBfFPVbghMpbEVUw615VHcqOxEXABZZ1PdIjuFqesRttsSu5yDxmztaW-Um9Vm",
    "jail_and_afk_discord_webhook_url": "https://discord.com/api/webhooks/844530195041615882/oqpkPJFBfFPVbghMpbEVUw615VHcqOxEXABZZ1PdIjuFqesRttsSu5yDxmztaW-Um9Vm",
    # relative X Y to target tress
    "relative_x": 0,
    "relative_y": -1,
    # if char should lock skill at 64.9 to get only boards that sells
    "lock_skill_at_64_9": True,
    "skip_bad_runes": True,
    "skip_runes_where_char_was_attacked": True,
    "skip_runes_where_char_died": True,
    "drop_money_to_main_char": True,
    # drop money config
    "main_char_name": "gugutz",
    "drop_money_secret_msg": "vendor bbuy sell",
    # runebook names
    "home_runebook": "Home",
    "wood_runebooks": ["Wood1", "Wood2"],
    "banks_runebook": "Banks",
    "carpenters_runebook": "Carps",
    # rune positions in Home runebook
    "rune_positions": {"vendor": 1, "bank": 2, "home": 3, "shrine": 4},
    "recall_to_escape_attacks": True,
    "place_to_escape_attacks": "home",  # home or bank
}

try:
    import lumber_config

    utils.debug("Found config file. Searching for character config...")

    if "general_config" in lumber_config.config:
        utils.debug("FOUND EXTERNAL DEFAULT CONFIGURATION")
        config[CharName()] = lumber_config.config["general_config"]
    if CharName() in lumber_config.config:
        utils.debug("FOUND CHAR %s CONFIG" % (CharName()))
        # config = lumber_config.config
        config[CharName()].update(lumber_config.config[CharName()])
except Exception as err:
    utils.debug("Error importing config: %s" % (err))
    utils.debug("**USING DEFAULT SCRIPT CONFIG **")
    pass


####################################################################
# AUTO CONFIGURABLE OPTIONS (DONT TOUCH THESE!!!)


RELATIVE_X = config[CharName()].get("relative_x")
RELATIVE_Y = config[CharName()].get("relative_y")
RELATIVE_TARGET_TILE = [RELATIVE_X, RELATIVE_Y]

SELL_BOARDS_STOCK = config[CharName()].get("sell_board_stock")
SKIP_BAD_RUNES = config[CharName()].get("skip_bad_runes")
SKIP_RUNES_WHERE_CHAR_WAS_ATTACKED = config[CharName()].get(
    "skip_runes_where_char_was_attacked"
)
SKIP_RUNES_WHERE_CHAR_DIED = config[CharName()].get("skip_runes_where_char_died")

UNLOAD_BOARDS_AT_BANK = config[CharName()].get("unload_boards_at_bank")
STORE_CHECKS_AT_HOME = config[CharName()].get("store_checks_at_home")
WOOD_STORAGE_CONTAINER = config[CharName()].get("wood_storage_container")

# if bot should lock still in 64.9 to only get utils.boards from trees
LOCK_SKILL_AT_64_9 = config[CharName()].get("lock_skill_at_64_9")
# sell boards or store them in house
SELL_WOOD = config[CharName()].get("sell_wood")
FAST_CASH = config[CharName()].get("fast_cash")
# Should char should try to re-equip after death?
AUTO_REEQUIP_SET = config[CharName()].get("auto_reequip_set")
USE_BANK_RUNEBOOK = False
USE_CARPENTER_RUNEBOOK = False
HOME_RUNEBOOK_NAME = config[CharName()].get("home_runebook")
WOOD_RUNEBOOKS = config[CharName()].get("wood_runebooks")
BANK_RUNEBOOK_NAME = config[CharName()].get("home_runebook")
CARPENTER_RUNEBOOK_NAME = config[CharName()].get("carpenters_runebook")
# Rune Positions
VENDOR_RUNE_POSITION = config[CharName()]["rune_positions"].get("vendor")
BANK_RUNE_POSITION = config[CharName()]["rune_positions"].get("bank")
HOME_RUNE_POSITION = config[CharName()]["rune_positions"].get("home")
SHRINE_RUNE_POSITION = config[CharName()]["rune_positions"].get("shrine")


# NEEDS A FOURTH RUNE IN HOME RUNEBOOK FOR THE SHRINE
AUTO_REFILL_TITHING_POINTS = config[CharName()].get("auto_refill_tithing_points")
MINIMUM_TITHING_POINTS = config[CharName()].get("minimum_tithing_points")

SEND_DISCORD_DEATH_WARNINGS = True
SEND_DISCORD_AFK_WARNINGS = True
AUTO_RECONNECT = True

DROP_MONEY_TO_MAIN_CHAR = True
MAIN_CHAR_NAME = "seila"
DROP_ALL_MONEY_MSG = config[CharName()].get("drop_money_secret_msg")

DISCORD_WEBHOOK_URL = config[CharName()].get("discord_webhook_url")

RECALL_TO_ESCAPE_ATTACKS = config[CharName()].get("recall_to_escape_attacks")
PLACE_TO_ESCAPE_ATTACKS = config[CharName()].get("place_to_escape_attacks")

BOT_MINIMUM_BALANCE = 100000  # Runebook names

# ======================================================================
# SCRIPT VARIABLES (DONT CHANGE THESE)
# ======================================================================

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


runes_where_char_was_attacked = {}
runes_where_char_died = {}
bad_runes = {}
for runebook in WOOD_RUNEBOOKS:
    if SKIP_RUNES_WHERE_CHAR_WAS_ATTACKED:
        runes_where_char_was_attacked[runebook] = []
    if SKIP_RUNES_WHERE_CHAR_DIED:
        runes_where_char_died[runebook] = []
    if SKIP_BAD_RUNES:
        bad_runes[runebook] = []

# security sets
current_runebook = "Wood1"
current_rune = 1


# ======================================================================
# IN-GAME ITEM TYPES (GRAPHICS)
# ======================================================================


# Create constant to hold the char axe
global CHAR_AXE
CHAR_AXE = 0


def confirm_script_loop_conditions():
    if Dead():
        return False
    if not Connected():
        return False

    return True


# ======================================================================
# BANK UTILS
# ======================================================================


def print_char_balance():
    utils.debug("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    utils.debug("** BALANCE **")
    if CURRENT_BALANCE > 0:
        utils.debug("** Current balance: %d" % (CURRENT_BALANCE))
    if CHECKS_IN_BANK > 0:
        utils.debug("** Checks in bank: %d" % (CHECKS_IN_BANK))
    else:
        utils.debug("** No Checks in Bank")

    amount_of_checks_in_backpack = count_colored(
        types.CHECK, types.CHECK_COLOR, Backpack()
    )
    if amount_of_checks_in_backpack > 0:
        utils.debug("** Checks in backpack: %d" % (amount_of_checks_in_backpack))
    utils.debug("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")


def refill_tithing_points():
    exit = False
    if not Dead() and Connected() and TRAVEL == "chiva":
        current_tithing_points = utils.get_current_tithing_points()
        msg = ""
        if current_tithing_points < 15:
            try:
                PlayWav(ALARM_WAV)
            except:
                pass
            if regions.in_region("britain_bank"):
                msg = f"**LUMBER NO TITHE** @everyone {char_name} has {current_tithing_points} tithe waiting at Britain Bank to be rescued"
                utils.debug("Char is already close to Britain Bank to be rescued")
                utils.debug("Attend to the bots needs and replay the script")
            elif not regions.in_region("britain_bank"):
                msg = "**LUMBER NO TITHE** @everyone %s has %d tithe and CANT TRAVEL! Taking char to Britain bank moongate and exiting Macro..."
                utils.go_to_britain_via_help_request()
                utils.go_to_britain_bank_vendor_mall_moongate()

            send_discord_message(DISCORD_WEBHOOK_URL, msg)
            exit = True

        if current_tithing_points < MINIMUM_TITHING_POINTS:
            if AUTO_REFILL_TITHING_POINTS:
                utils.debug("*LOW TITHE* Char is low on tithing points.")
                utils.debug("Going to the bank to get money to tithe gold")

                # check and solve char weight first
                if count(types.LOG):
                    utils.debug(
                        "Dropping logs from backpack to withdraw gold to the shrine"
                    )
                    utils.drop_type(utils.count(types.LOG), 999)
                if count(types.BOARD):
                    utils.debug(
                        "Dropping boards from backpack to withdraw gold to the shrine"
                    )
                    utils.drop_type(count(types.BOARD), 999)
                if Weight() >= MaxWeight():
                    utils.debug("Char is overweight. Reducing weight to go tithe gold")
                    reduce_weight_to_travel()

                # amount_to_withdraw = (MaxWeight() - Weight()) * 200
                gold_in_backpack = count(types.GOLD)
                value_to_withdraw = 30000 - gold_in_backpack
                if value_to_withdraw > 0:
                    recall_bank()
                    UOSay(f"withdraw {value_to_withdraw}")
                recall_to_shrine()
                utils.tithe_gold_to_shrine()
                return True

            exit = True

        if exit:
            utils.debug("****************************")
            utils.debug(">>> NO TITHING POINTS FOR TRAVEL:")
            utils.debug(msg)
            # disable exit traceback for a clean log
            utils.debug(
                "The script also supports auto refilling tithing points when this happens"
            )
            utils.debug("Just mark a rune to a shrine and put it your Home Runebook")
            # disable exit traceback for a clean log
            sys.tracebacklimit = 0
            exit(
                "No tithing points to travel. Refill char tithing points and replay the script."
            )


# ======================================================================
# JOURNAL UTILS
# ======================================================================


def confirm_lumber_success():
    lumber_success_journal_msgs = "You hack at | You put some | You chop some "

    # if we get a msg in journal saying wood is out, mark spot as invalid
    if InJournal(lumber_success_journal_msgs) > -1:
        ClearJournal()
        return True
    else:
        return False


def is_spot_out_of_wood():
    spot_out_of_wood_journal_msgs = "There is nothing here | There's not enough |"
    if InJournal(spot_out_of_wood_journal_msgs) > 0:
        ClearJournal()
        return True
    else:
        return False


def cant_place_wood_in_backpack():
    cant_place_wood_in_backpack_msg = "place any wood into your backpack"

    # if we get a msg in journal saying wood is out, mark spot as invalid
    if InJournal(cant_place_wood_in_backpack_msg) > 0:
        ClearJournal()
        return True
    else:
        return False


def is_spot_valid():
    fail_to_lumber_journal_msgs = (
        "There is nothing here |"
        "Invalid tile to chop |"
        "You cannot mine |"
        "You have no line |"
        "That is too far |"
        "Try mining elsewhere |"
        "You can't mine |"
        "someone |"
        "Target cannot be |"
        "use an axe on that |"
        "axe must be equipped |"
    )

    if InJournal(fail_to_lumber_journal_msgs) > -1:
        ClearJournal()
        return False
    else:
        return True


# ======================================================================
# Travel utils (recall to home, bank, vendor)
# ======================================================================


def return_to_previous_lumber_spot():
    # uses in-memory values for runebook and runenumber
    utils.debug("Returning to previous lumber spot")
    utils.travel_to(current_runebook, TRAVEL, current_rune, 4000)


def recall_carpenter():
    turn_logs_into_boards()
    utils.travel_to(HOME_RUNEBOOK_NAME, TRAVEL, VENDOR_RUNE_POSITION)
    # while not is_char_at_vendor("carpenter"):
    #     if USE_CARPENTER_RUNEBOOK:
    #         utils.debug("Travelling to random rune in Carpenter Runebook")
    #         utils.travel_to(CARPENTER_RUNEBOOK_NAME, TRAVEL, randrange(17))
    #     else:
    #         utils.travel_to(HOME_RUNEBOOK_NAME, TRAVEL, VENDOR_RUNE_POSITION)
    # return True


def recall_bank():
    reduce_weight_to_travel()
    # while not is_char_at_bank():
    if USE_BANK_RUNEBOOK:
        utils.travel_to(BANK_RUNEBOOK_NAME, TRAVEL, randrange(17))
    else:
        utils.debug("Going to the bank.")
        utils.travel_to(HOME_RUNEBOOK_NAME, TRAVEL, BANK_RUNE_POSITION)

    return True


def recall_home():
    utils.debug("Going home.")
    utils.travel_to(HOME_RUNEBOOK_NAME, TRAVEL, HOME_RUNE_POSITION)


def recall_to_shrine():
    utils.debug("Going to the shrine.")
    utils.travel_to(HOME_RUNEBOOK_NAME, TRAVEL, SHRINE_RUNE_POSITION)


# ======================================================================
# FindItem checks
# ======================================================================

# Checks if char has boards in backpack to avoid pointless travels to vendor
def get_boards_from_ground_maybe():
    SetFindDistance(2)
    SetFindVertical(10)
    start_time = datetime.now()

    boards_on_ground = CountGround(types.BOARD)
    if FAST_CASH:
        colors_to_search = 0
    else:
        colors_to_search = -1

    limit_to_pick = MaxWeight() - Weight()
    while confirm_script_loop_conditions() and FindTypeEx(
        types.BOARD, colors_to_search, Ground(), False
    ):
        if limit_to_pick > 0:
            if Weight() <= WEIGHT_LIMIT:
                if FAST_CASH:
                    resource_color = GetColor(FindItem())
                    if resource_color == 0:
                        Grab(FindItem(), limit_to_pick)
                        utils.wait_lag(600)
                        # MoveItem(FindItem(), limit_to_pick, Backpack(), 0, 0, 0)
                    else:
                        utils.debug(
                            "FAST CASH is on. Ignoring colored boards found on the ground."
                        )
                else:
                    utils.debug(
                        "Found %d boards on the ground and moving to backpack"
                        % (boards_on_ground)
                    )
                    # MoveItem(FindItem(), limit_to_pick, Backpack(), 0, 0, 0)
                    Grab(FindItem(), limit_to_pick)
                    utils.wait_lag(600)
            else:
                utils.debug(
                    "Found boards on the ground but char is overweight to get it"
                )
                break
        else:
            utils.debug(
                "Char doenst have room in backpack to pick up boards on the ground"
            )
            break

        if utils.check_timer(start_time, 4000):
            utils.debug("Timeout while getting boards from ground. Breaking...")
            break

    # causing recursion problem?
    # if Weight() >= WEIGHT_LIMIT:
    #     begin_sell_and_unload_maybe()

    if boards_on_ground == 0:
        return True
    else:
        return False


def find_char_axe():
    for axe in types.AXES:
        axe_found = False

        if (
            ObjAtLayer(RhandLayer()) != 0
            and (GetType(ObjAtLayer(RhandLayer()))) == types.AXES[axe]
        ):
            utils.debug("Axe found on right hand!. Type: %s" % (axe))
            axe_found = ObjAtLayer(RhandLayer())

        elif (
            ObjAtLayer(LhandLayer()) != 0
            and (GetType(ObjAtLayer(LhandLayer()))) == types.AXES[axe]
        ):
            utils.debug("Axe found on left hand!. Type: %s" % (axe))
            axe_found = ObjAtLayer(LhandLayer())

        # If didnt find axe on hands so far, search for an axe in backpack and equip
        else:
            utils.debug("Searching for %s in backpack." % (axe))
            if FindTypeEx(types.AXES[axe], 0xFFFF, Backpack(), True):
                axe_found = FindItem()
                utils.debug(
                    "Found %s in backpack. Setting main axe."
                    % (utils.get_item_name(axe_found))
                )

    if axe_found is not None:
        # global CHAR_AXE
        # CHAR_AXE = axe_found
        return axe_found
    # else:
    #     utils.debug("Couldnt find an axe on the character or its backpack.")
    # utils.debug("Please buy an axe and play macro again")
    # exit()


def equip_char_axe():
    global CHAR_AXE
    while confirm_script_loop_conditions() and not CHAR_AXE:
        CHAR_AXE = find_char_axe()
        Wait(CheckLag(3000))

    layer = RhandLayer()

    if ObjAtLayer(RhandLayer()) > 0:
        utils.debug("Unequiping Right Hand")
        UnEquip(RhandLayer())
        Wait(CheckLag(3000))
    if ObjAtLayer(LhandLayer()) > 0:
        utils.debug("Unequiping Left Hand")
        UnEquip(LhandLayer())
        Wait(CheckLag(3000))

    if Equip(layer, CHAR_AXE):
        utils.debug("Axe equiped")
        Wait(CheckLag(3000))


def is_axe_equipped():
    item_in_hand = ObjAtLayer(LhandLayer())

    if item_in_hand > 0:
        for axe in types.AXES:
            if (GetType(item_in_hand)) == types.AXES[axe]:
                return True
    elif ObjAtLayer(RhandLayer()) > 0:
        for axe in types.AXES:
            if (GetType(item_in_hand)) == types.AXES[axe]:
                return True
    else:
        return False


# ======================================================================
# Sell Boards
# ======================================================================


def sell_boards_to_carpenter():
    global NPC_VENDOR
    global NPC_VENDOR_NAME
    utils.debug("Going to the vendor to sell boards.")
    # adding this wait here baecause char was getting stuck on "You Must wait to perform another action"
    utils.wait_lag(50)

    reduce_weight_to_travel()
    recall_carpenter()

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


def sell_board_stock(container_to_search_for_stock):
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
            # NOTE: teste fix recursion bug
            # begin_sell_and_unload_maybe()
            sell_boards_to_carpenter()
            recall_bank()
            deposit_gold_in_bank()
        else:
            break

    if not FindTypeEx(types.BOARD, 0, container_to_search_for_stock, True):
        utils.debug("Sold all wood stock in wood storage container!")
        return True

    return False


def print_script_stats():
    # this is an expensive check, so we avoid until  were done cleaning the wood stock in bank
    global CURRENT_BALANCE
    CURRENT_BALANCE = utils.get_current_bank_balance()
    global CHECKS_IN_BANK
    CHECKS_IN_BANK = count_colored(types.CHECK, types.CHECK_COLOR, bank)
    utils.debug("------------------------------------------------")
    utils.debug("** SCRIPT STATISTICS **")
    utils.debug("Connected since: %s" % (ConnectedTime()))
    utils.debug("Disconnections: %d" % (number_of_disconnections))
    if last_disconnection != "":
        utils.debug("Last disconnection: %d" % (last_disconnection))

    utils.debug("Tithing points: %d" % (current_tithing_points))
    print_amount_of_checks_maybe()
    print_current_profit()
    print_char_balance()

    utils.debug("------------------------------------------------")


# ======================================================================
# UNLOAD types.GOLD IN BANK
# ======================================================================


def store_checks_at_home():
    global WOOD_STORAGE_CONTAINER
    if STORE_CHECKS_AT_HOME:
        start_time = datetime.now()
        while confirm_script_loop_conditions() and FindTypeEx(
            types.CHECK, types.CHECK_COLOR, ObjAtLayer(BankLayer()), False
        ):
            checks_in_bank = FindCount()
            utils.debug(
                "Found %d checks in bank. Grabbing to take home..." % (checks_in_bank)
            )
            check = FindItem()
            utils.debug("Grabbing checks...")
            Grab(check, 1)
            utils.wait_lag(2000)

            if utils.check_timer(start_time, 6000):
                utils.debug("Timeout trying to grab checks from bank. Breaking.")
                break

        utils.wait_lag(1000)
        if FindTypeEx(types.CHECK, types.CHECK_COLOR, backpack, False):
            amount_of_checks_in_backpack = FindCount()
            utils.debug("Checks in backpack: %d" % (amount_of_checks_in_backpack))
            recall_home()
            if not WOOD_STORAGE_CONTAINER:
                utils.debug("Trying to find wood storage container")
                WOOD_STORAGE_CONTAINER = find_and_set_storage_container()

            if WOOD_STORAGE_CONTAINER:
                # open the container once so we can count the checks
                utils.debug("Opening Storage Container")
                UseObject(WOOD_STORAGE_CONTAINER)
                utils.wait_lag(1000)

                initial_amount_of_checks_at_home = count_colored(
                    types.CHECK, types.CHECK_COLOR, WOOD_STORAGE_CONTAINER
                )
                start_time = datetime.now()
                while confirm_script_loop_conditions() and FindTypeEx(
                    types.CHECK, types.CHECK_COLOR, Backpack(), False
                ):
                    check = FindItem()
                    utils.debug("Moving checks to storage container")
                    MoveItem(check, 1, WOOD_STORAGE_CONTAINER, 0, 0, 0)
                    utils.wait_lag(2000)

                    if utils.check_timer(start_time, 10000):
                        utils.debug(
                            "Timeout trying to move checks to home container. Breaking."
                        )
                        break

                checks_at_home_after_deposit = count_colored(
                    types.CHECK, types.CHECK_COLOR, WOOD_STORAGE_CONTAINER
                )
                if checks_at_home_after_deposit > initial_amount_of_checks_at_home:
                    try:
                        send_discord_message(
                            DISCORD_WEBHOOK_URL,
                            "**HOME BALANCE** %s brought home another check! Checks at home: %d"
                            % (char_name, checks_at_home_after_deposit),
                        )
                    except:
                        pass

    return False


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


def deposit_gold_in_bank():
    utils.wait_lag(50)
    UOSay("bank")
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

        store_checks_at_home()

        get_boards_from_ground_maybe()
        sell_board_stock(bank)

        if DROP_MONEY_TO_MAIN_CHAR:
            drop_money_to_main_char_maybe()

        # print statistics
        print_script_stats()

    return True


# ======================================================================
# UNLOAD types.BOARD AT HOME OR BANK
# ======================================================================


def find_and_set_storage_container():
    global WOOD_STORAGE_CONTAINER
    start_time = datetime.now()
    while confirm_script_loop_conditions() and not WOOD_STORAGE_CONTAINER:
        WOOD_STORAGE_CONTAINER = utils.find_commodity_deed_box_on_ground()
        if utils.check_timer(start_time, 6000):
            utils.debug("Timeout searcing for commodity deed on the ground...")
            break
    if WOOD_STORAGE_CONTAINER:
        return WOOD_STORAGE_CONTAINER


def unload_boards_maybe():

    turn_logs_into_boards()

    container_to_unload = ""

    # drop boards in bank
    global WOOD_STORAGE_CONTAINER
    if UNLOAD_BOARDS_AT_BANK:
        if not WOOD_STORAGE_CONTAINER:
            WOOD_STORAGE_CONTAINER = bank
        utils.debug("Unloading boards in bank")
        utils.wait_lag(100)
        UOSay("bank")
        utils.wait_lag(10)
    else:
        find_and_set_storage_container()
        utils.debug("Unloading boards at home")
        utils.wait_lag(100)
        UseObject(WOOD_STORAGE_CONTAINER)
        utils.wait_lag(10)

    starttime = datetime.now()
    while confirm_script_loop_conditions() and FindTypesArrayEx(
        LUMBER_RESOURCES_TYPES, [0xFFFF], [Backpack()], False
    ):
        if MoveItem(FindItem(), 65000, WOOD_STORAGE_CONTAINER, 0, 0, 0):
            # even thought were in a while, MoveItem involves packet trades, so we wait_lag
            # delay here must be 100, or else char will get stuck trying to move item to bank
            utils.wait_lag(600)
        if utils.check_timer(starttime, 8000):
            utils.debug("Timeout trying to move item to wood storage. Breaking...")
            utils.wait_lag(10)
            UOSay("bank")
            break

    drop_money_to_main_char_maybe()
    get_boards_from_ground_maybe()

    # # recursive call to unload again if found boards on the ground
    # if count(types.BOARD):
    #     unload_boards_maybe()

    # add check to garantee tithing poinst wont run out while char is selling wood stock
    refill_tithing_points()

    if SELL_WOOD and SELL_BOARDS_STOCK:
        sell_board_stock(WOOD_STORAGE_CONTAINER)

    return True


##################################################################
def TypeQuantity(type, color=0x0000, container=Backpack()):
    FindTypeEx(type, color, container, True)
    return FindFullQuantity()


##################################################################
def identify_tile(x, y, relativeX, relativeY, tileType=[]):
    absRelativeX = abs(relativeX)
    absRelativeY = abs(relativeY)

    processedAbsRelativeX = absRelativeX + 2
    processedAbsRelativeY = absRelativeY + 2

    wantedPositionX = x + relativeX
    wantedPositionY = y + relativeY

    for xx in range(x - processedAbsRelativeX, x + processedAbsRelativeX):
        for yy in range(y - processedAbsRelativeY, y + processedAbsRelativeY):
            result = ReadStaticsXY(xx, yy, WorldNum())
            for result in result:
                # utils.debug(r)
                if result:
                    if (result["X"] == wantedPositionX) and (
                        result["Y"] == wantedPositionY
                    ):
                        # If array of tiletype is set, we need to check for a specific tile type!
                        if tileType:
                            if result["Tile"] in tileType:
                                return result
                        # if not, return the first tile
                        else:
                            return result


def handle_char_being_attacked():
    if is_char_being_attacked() or GetHP(Self()) < GetMaxHP(Self()):
        utils.debug(
            "%s is being attacked at %d on %s runebook. Trying to escape to bank"
            % (char_name, current_rune, current_runebook)
        )
        if SKIP_RUNES_WHERE_CHAR_WAS_ATTACKED:
            # put the book name on the list if needed first

            runes_where_char_was_attacked[current_runebook].append(current_rune)

        UOSay("guards")
        recall_bank()
        UOSay("guards")
        if is_char_at_bank():
            utils.debug("Char escaped to the bank successfully")

        if Dead():
            if SKIP_RUNES_WHERE_CHAR_DIED:
                utils.debug(
                    "Char died while trying to escape. Will skip rune %d next lumber cicle."
                    % (current_rune)
                )
                runes_wher_char_died[current_runebook].append(current_rune)
            else:
                utils.debug("Char died while trying to escape.")
            return False

    utils.wait_lag(500)
    return True


def check_gm_present():
    if gm.is_gm_present():
        try:
            PlayWav(ALARM_WAV)
            webhooks.send_discord_message(
                DISCORD_WEBHOOK_URL,
                "**LUMBER GM CLOSE** @everyone a GM is talking to %s !" % (char_name),
            )
        except:
            pass
        # simulate talk and disconnect faking lag
        Wait(5000)
        UOSay("Iska")
        Wait(2000)
        UOSay("Dru mastchef itch nur mordr?. :)")
        Step(3)
        Wait(4000)
        Step(1)
        Step(2)
        Step(3)
        Step(4)
        Step(5)
        UOSay("lag")
        Disconnect()
        exit()


##################################################################

# skill lock states
# 0 - skill will increase,
# 1 - skill will decrease,
# 2 - skill locked.
def check_lumber_skill_level():
    if LOCK_SKILL_AT_64_9:
        if GetSkillValue("Lumberjacking") >= 64.8:
            start_time = datetime.now()
            while GetSkillLockState("Lumberjacking") != 2:
                utils.debug("* LOCKING LUMBERJACKING AT 64.8.")
                ChangeSkillLockState("Lumberjacking", 2)
                Wait(1000)
                if check_timer(start_time, 5000):
                    utils.debug("5 seconds trying to lock skill, check what happened!!")


def lumber():

    # get tree tile to target and get wood
    tile = identify_tile(
        GetX(Self()), GetY(Self()), RELATIVE_X, RELATIVE_Y, types.TREES
    )

    equip_axe()

    if confirm_script_loop_conditions() and tile:
        check_afk_gump()
        check_gm_present()
        while confirm_script_loop_conditions() and Weight() < WEIGHT_LIMIT:
            # perform_routine_checks()
            spot_valid = True
            spot_out_of_wood = False
            time_char_started_loop = datetime.now()

            if TargetPresent():
                CancelTarget()

            temp_weight = Weight()
            previous_weight = temp_weight
            while (
                confirm_script_loop_conditions()
                and spot_valid
                and Weight() < MaxWeight()
            ):

                if Weight() > previous_weight:
                    previous_weight = Weight()
                    break

                # check_lumber_skill_level()

                # keep clicking on axe until target appears
                while confirm_script_loop_conditions() and not TargetPresent():
                    UseObject(ObjAtLayer(LhandLayer()))
                    # using wait_lag here cause Wait produces "you must wait to perform another action"
                    Wait(1)

                if TargetPresent():
                    TargetToTile(tile["Tile"], tile["X"], tile["Y"], tile["Z"])
                    # just for the log appears on the journal.
                    utils.wait_lag(0)

                    mobs_nearby = utils.get_nearby_mobs(20, [], [3, 4, 6])
                    # mobs_nearby = utils.get_nearby_mobs(10, [], 6)
                    if len(mobs_nearby) > 0:
                        for mob in mobs_nearby:
                            mob_name = GetName(mob)
                            if npc.is_npc(mob):
                                utils.debug("Found NPC %s. Ignoring it..." % (mob_name))
                                Ignore(mob)
                            elif utils.is_pk(mob):
                                utils.debug(
                                    "PK %s close to char. Escaping..." % (mob_name)
                                )
                                if RECALL_TO_ESCAPE_ATTACKS:
                                    if PLACE_TO_ESCAPE_ATTACKS == "home":
                                        recall_home()
                                    else:
                                        recall_bank()

                                    utils.debug(
                                        "Waiting 5 minutes to return to previous lumber spot..."
                                    )
                                    Wait(300000)
                                    return_to_previous_lumber_spot()
                                    break

                                try:
                                    send_discord_message(
                                        DISCORD_WEBHOOK_URL,
                                        "**LUMBER PK** @everyone % tried to kill %s, but failed. Bot escaped."
                                        % (mob_name, char_name),
                                    )
                                except:
                                    pass
                                return False
                            elif GetType(mob) in types.AGRESSIVE_MOBS:
                                utils.debug(
                                    "There are agressive monsters nearby. Escaping..."
                                )
                                # try:
                                #     send_discord_message(
                                #         DISCORD_WEBHOOK_URL,
                                #         "**LUMBER IN RISK** @everyone %s close to %s. Bot escaped."
                                #         % (mob_name, char_name),
                                #     )
                                # except:
                                #     pass
                                return False

                    # if weight changed, it confirms previous lumber was succesfull
                    if Weight() > previous_weight:
                        utils.debug(f"Lumbering (W: {Weight()}/{MaxWeight()})")
                        previous_weight = Weight()

                    if is_spot_out_of_wood():
                        utils.debug(
                            f"{current_runebook} - Rune {current_rune} out of wood"
                        )
                        return False

                    if not is_spot_valid():
                        utils.debug(
                            "Rune %d from %s runebook is invalid. Travelling to next rune."
                            % (current_rune, current_runebook)
                        )
                        spot_valid = False
                        if SKIP_BAD_RUNES:
                            bad_runes[current_runebook].append(current_rune)
                        return False

                # char is overweighted with logs in backpack, turn logs into boards to lower weight
                while (
                    confirm_script_loop_conditions()
                    and count(types.LOG)
                    and Weight() >= WEIGHT_LIMIT
                ):
                    turn_logs_into_boards()

                if spot_out_of_wood or not spot_valid:
                    return False

                if utils.check_timer(time_char_started_loop, 50000):
                    utils.debug("Timeout lumbering (50s on the same tree). Breaking...")
                    return False

                # check_lumber_skill_level()

        return True

    else:
        utils.debug("Invalid tile to chop")
        utils.debug("Skipping this rune next time")
        if SKIP_BAD_RUNES:
            if current_runebook not in bad_runes:
                bad_runes[current_runebook] = []
            bad_runes[current_runebook].append(current_rune)
        return False


##############################################################################


def drop_special_resources_on_ground_maybe():
    if FAST_CASH:

        for resource in types.SPECIAL_LUMBER_RESOURCES:
            resource_name = types.SPECIAL_LUMBER_RESOURCES.get("resource")
            resource_type = types.SPECIAL_LUMBER_RESOURCES[resource].get("graphic")
            resource_color = types.SPECIAL_LUMBER_RESOURCES[resource].get("color")

            if FindTypeEx(resource_type, resource_color, backpack, False):
                found = FindItem()
                resource_amount = FindFullQuantity()
                utils.debug(f">> FAST CASH is on. Dropping {resource} on the ground")
                utils.drop(found, resource_amount)
                utils.wait_lag(100)


def turn_logs_into_boards():

    drop_special_resources_on_ground_maybe()

    start_time = datetime.now()

    # get list of all boards in backpac
    while confirm_script_loop_conditions() and FindType(types.LOG, Backpack()):
        equip_axe()
        utils.debug("Turning logs into boards")
        logs_found_in_backpack = GetFindedList()
        for log in logs_found_in_backpack:

            # Use axe to make boards out of logs
            while confirm_script_loop_conditions() and not TargetPresent():
                UseObject(CHAR_AXE)
                WaitForTarget(600)
                if Dead():
                    utils.debug("Dead while turning logs into boards")
                    break
            if TargetPresent():
                WaitTargetObject(log)
                utils.wait_lag(300)

            # 5 seconds seems ideal here
            if utils.check_timer(start_time, 8000):
                utils.debug("Timeout while making boards. Breaking...")
                break

        if utils.check_timer(start_time, 12000):
            utils.debug("12 seconds inside make boards while. Breaking...")
            break

        # search again to begin another cycle
        FindType(types.LOG, Backpack())
        logs_found_in_backpack = GetFindedList()

    return True


def check_suit_insurance():
    if confirm_script_loop_conditions() and insurance.is_set_insured() is False:
        utils.debug("****************************")
        utils.debug(">>> ABORTING:")
        utils.debug(
            "One or more set items is not insured or cannot not be reinsured after ressurect!"
        )
        SetARStatus(False)
        Disconnect()
        # disable exit traceback for a clean log
        sys.tracebacklimit = 0
        utils.debug("****************************")
        exit("Exiting: No money for insurance.")


def print_current_profit():
    current_profit = CURRENT_BALANCE - initial_balance
    if current_profit > 0:
        utils.debug("%s current profit so far: %s gold." % (char_name, current_profit))


def print_amount_of_checks_maybe():
    amount_of_checks_in_bank = count(types.CHECK, types.CHECK_COLOR, bank)
    if amount_of_checks_in_bank > 0:
        utils.debug("Char has %d checks in the bank." % (amount_of_checks_in_bank))


def equip_axe():
    if not is_axe_equipped():
        utils.debug("Axe is not equipped.")
        equip_char_axe()
        return True
    return False


def drop_checks_on_ground():
    initial_amount_of_checks_in_bank = count_checks_in_bank()
    if count_checks_in_bank() > 0:
        utils.debug(
            "Main char %s asked for all checks in bank. Dropping %d checks in the ground"
            % (MAIN_CHAR_NAME, CHECKS_IN_BANK)
        )
        start_time = datetime.now()
        while confirm_script_loop_conditions() and FindTypeEx(
            types.CHECK, types.CHECK_COLOR, bank, True
        ):
            check = FindItem()
            if drop_item_from_bank(check, 1):
                utils.debug("Dropped check sucessfully.")
            else:
                utils.debug("Failed dropping check")

            if utils.check_timer(start_time, 6000):
                utils.debug("Timeout trying to drop check to main char. Breaking.")
                break

    else:
        utils.debug(
            "Main char %s asked for all checks in bank, but char %s doenst have any checks in bank."
            % (MAIN_CHAR_NAME, char_name)
        )
    return False


def make_check_of_current_gold_in_bank_maybe():
    amount_of_gold_in_bank = count_colored(CHECK, types.CHECK_COLOR, bank)
    if amount_of_gold_in_bank > BOT_MINIMUM_BALANCE + 100000:
        check_value = amount_of_gold_in_bank - BOT_MINIMUM_BALANCE
        utils.debug("Making check of %d to drop to main char." % (check_value))
        UOSay("check %s" % (check_value))
        send_discord_message(
            DISCORD_WEBHOOK_URL,
            "**CHECK** @everyone %s made a %d check!" % (char_name, check_value),
        )

        utils.wait_lag(10)
    else:
        utils.debug(
            "Char only have %d in bank and cant make a check yet..."
            % (amount_of_gold_in_bank)
        )


# Checks if char has boards in backpack to avoid pointless travels to vendor
def drop_money_to_main_char_maybe():
    if InJournal("vendor buy sell bank guards recdus") > 0:
        utils.debug(
            "Main char asked for money. Making checks and dropping in the ground"
        )
        ClearJournal()
        make_check_of_current_gold_in_bank_maybe()
        utils.wait_lag(100)
        while (
            confirm_script_loop_conditions()
            and count_colored(types.CHECK, types.CHECK_COLOR, bank) > 0
        ):
            drop_checks_on_ground()
            utils.wait_lag(100)
    else:
        utils.debug("Didnt detect money request msg. Continuing...")


def begin_sell_and_unload_maybe():
    if Weight() > MaxWeight():
        utils.debug("Overweight before going to unload. Reducing Weight")
        reduce_weight_to_travel()

    if SELL_WOOD:
        if count_common(types.BOARD):
            sell_boards_to_carpenter()
        recall_bank()
        deposit_gold_in_bank()
    else:
        go_to_storage_container()

    unload_boards_maybe()
    refill_tithing_points()


def reduce_weight_to_travel():
    # aqui tem que ser maior apenas, igual o char ainda pode viajar
    if Weight() > MaxWeight():
        turn_logs_into_boards()
        amount_to_drop = Weight() - MaxWeight()
        utils.debug("Dropping %d boards to travel." % (amount_to_drop))
        utils.drop_type(types.BOARD, amount_to_drop)


def handle_death():
    global FIRST_RUN

    # notify on discord
    try:
        if PLAY_SOUNDS:
            PlayWav(ALARM_SOUND)
        if FIRST_RUN:
            debug(
                f"**LUMBER DEAD** | {ProfileName()} ({char_name}) started macro dead. Going to ress ",
            )
            # webhooks.send_discord_message(
            #     DISCORD_WEBHOOK_URL,
            #     f"**LUMBER DEAD** | {ProfileName()} ({char_name}) started macro dead. Going to ress ",
            # )
        else:
            webhooks.send_discord_message(
                DISCORD_WEBHOOK_URL,
                f"**LUMBER DEAD** | {ProfileName()} ({char_name}) dead in {CURRENT_RUNEBOOK} -> Rune {CURRENT_RUNE}",
            )
    except:
        pass

    # set to skip rune so char wont die again on this spot
    if not FIRST_RUN and SKIP_RUNES_WHERE_CHAR_DIED:
        utils.debug(
            "Char died on rune %d from %s runebook. Will skip this rune on next lumber cicle."
            % (current_rune, current_runebook)
        )
        runes_where_char_died[current_runebook].append(current_rune)

    ress.ress()
    utils.remove_death_robe()
    if AUTO_REEQUIP_SET:
        if not utils.is_set_equiped():
            utils.dress_char_set()
        utils.save_char_set()


# ======================================================================
# PREPARE TO START
# ======================================================================

connection.connect()
char_name = connection.get_char_name()
if char_name:
    debug("Char name: %s" % (char_name))

TRAVEL = utils.set_travel_method()
if not TRAVEL:
    debug("****************************")
    debug(">>> SCRIPT FATAL ERROR:")
    debug(">> Char doenst have a way to travel.")
    debug(">> Train magery or chivalry, get regs or tithe and try again")
    debug(f">> Char Magery: {GetSkillValue('Magery')}")
    debug(f">> Char Chivalry: {GetSkillValue('Chivalry')}")
    debug(f">> Char Tithing Points: {utils.get_current_tithing_points()}")
    # disable exit traceback for a clean log
    sys.tracebacklimit = 0
    debug("****************************")
    exit("Check errors above")

utils.debug("***************")
utils.debug("STARTING MACRO")


def check_afk_gump():
    if is_afk_gump():
        utils.debug("***********************")
        utils.debug("!!! AFK GUMP DETECTED !!!")
        utils.debug("Sending discord msg...")
        webhooks.send_discord_message(
            DISCORD_WEBHOOK_URL, "**AFK GUMP** on {Profile()} / {CharName()}"
        )
        if afk_check.solve_afk_gump():
            utils.debug("AFK Gump Solved!")
            return true
    else:
        # utils.debug("Gump detected was NOT an AFK Gump")
        # utils.debug("Leaving as is...")
        return False
        # close_gumps()


def check_jail():
    if jail.is_char_in_6_hours_jail():
        utils.debug("** JAIL 6 HOURS **")
        try:
            send_discord_message(
                DISCORD_WEBHOOK_URL,
                "**LUMBER JAIL 6 HOURS ** @everyone %s is in 6 HOURS JAIL. Starting jail timer..."
                % (char_name),
            )
        except:
            pass
        Wait(100000)
        UOSay("I will not commit a bannable offense again")
        utils.debug(
            "** Char started 6 hours jail timer and will now exit macro to wait... **"
        )
        exit()
        return True

    if jail.is_char_in_jail():
        if PLAY_SOUNDS:
            try:
                PlayWav(ALARM_SOUND)
                send_discord_message(
                    DISCORD_WEBHOOK_URL,
                    "**LUMBER JAIL** @everyone %s is in jail and is gonna escape"
                    % (char_name),
                )
            except:
                pass
        Wait(1000000)
        jail.escape_jail()


def go_to_storage_container():
    if UNLOAD_BOARDS_AT_BANK:
        recall_bank()
    else:
        recall_home()


def append_to_death_log(text_log):
    if types.LOG_DEATHS:
        toolTip = GetTooltip(reward)
        rewardsLog = open(
            StealthPath() + "/Scripts/" + DEATH_types.LOG_FILE.format(datetime.today()),
            "a+",
        )
        rewardsLog.writelines(
            "{0} | {1} | {2} | ID:{3} \n".format(
                CharName(), toolTip, str(datetime.now()), reward
            )
        )
        rewardsLog.close()


##############################################################################
# main routine.

if __name__ == "__main__":
    global FIRST_RUN
    FIRST_RUN = True
    # clear char log just in case
    ClearJournal()

    connection.connect()

    # trying to fix overnight disconect and stuck bug
    SetPauseScriptOnDisconnectStatus(False)
    SetARStatus(True)

    gumps.close_gumps()
    start_cordinates = (GetX(Self()), GetX(Self()))
    time_char_started_macro = datetime.now()

    if Dead():
        utils.debug("Char started macro dead. Trying to ress")
        handle_death()

    check_jail()

    # get char initial bank balance
    initial_balance = 0
    if confirm_script_loop_conditions():
        initial_balance = utils.get_current_bank_balance()
        utils.debug("Initial bank balance: %s" % (initial_balance))
    else:
        initial_balance = 0

    while True:
        utils.debug("while true")
        if Dead():
            handle_death()
        if not Connected():
            number_of_disconnections += 1
            if AUTO_RECONNECT:
                if not FIRST_RUN:
                    utils.debug(
                        "Char was disconnected during macro. Trying to reconnect..."
                    )
                    utils.debug(
                        "Number of disconnections: %d" % (number_of_disconnections)
                    )
                connection.connect()

        while confirm_script_loop_conditions():

            FIRST_RUN = False
            CURRENT_BALANCE = initial_balance
            amount_of_checks_in_bank = 0
            utils.remove_death_robe()
            if AUTO_REEQUIP_SET:
                if not utils.is_set_equiped():
                    utils.dress_char_set()
                utils.save_char_set()
            equip_axe()
            refill_tithing_points()
            utils.remove_death_robe()
            check_suit_insurance()

            for runebook in WOOD_RUNEBOOKS:
                if not confirm_script_loop_conditions():
                    break
                utils.debug(f">>> {runebook.upper()} runebook start")
                # if char is connected for more than 1 hour, start printing uptime
                if ConnectedTime() > time_char_started_macro + timedelta(minutes=60):
                    connection.print_uptime()
                current_runebook = runebook

                # travel to every rune in the runebook
                for runenumber in range(1, 17):
                    if not confirm_script_loop_conditions():
                        break
                    if GetHP(Self()) < GetMaxHP(Self()):
                        utils.heal_self_until_max_hp()

                    current_rune = runenumber

                    # ---------------------------------------------------
                    # main chop wood loop. will only loop while char is not overweighted with logs
                    while confirm_script_loop_conditions() and Weight() < WEIGHT_LIMIT:
                        check_afk_gump()
                        check_jail()
                        # check_lumber_skill_level()
                        # check if rune is bad first before travelling
                        if SKIP_BAD_RUNES and runenumber in bad_runes.get(runebook):
                            utils.debug(
                                "Rune %d on %s runebook is marked as bad rune. Skipping it"
                                % (runenumber, runebook)
                            )
                            break
                        elif (
                            SKIP_RUNES_WHERE_CHAR_WAS_ATTACKED
                            and runenumber
                            in runes_where_char_was_attacked.get(runebook)
                        ):
                            utils.debug(
                                "%s died on last visit to rune %d on %s runebook. Skillping it."
                                % (char_name, runenumber, runebook)
                            )
                            break
                        elif (
                            SKIP_RUNES_WHERE_CHAR_DIED
                            and runenumber in runes_where_char_died.get(runebook)
                        ):
                            utils.debug(
                                "%s died on last visit to rune %d on %s runebook. Skipping it."
                                % (char_name, runenumber, runebook)
                            )
                            break
                        else:
                            if utils.travel_to(runebook, TRAVEL, runenumber, 4000):
                                utils.wait_lag(1)
                                get_boards_from_ground_maybe()
                                if TargetPresent():
                                    CancelTarget()

                                utils.debug(
                                    f"Starting Lumbering (W: {Weight()}/{MaxWeight()})"
                                )
                                if lumber():
                                    continue
                                else:
                                    break

                            else:
                                utils.debug(
                                    f"Failed traveling to {runenumber}. Skipping to next rune."
                                )
                                break

                    # handle when char started macro ready to sell but overweight to travel
                    while (
                        confirm_script_loop_conditions()
                        and count(types.BOARD)
                        and not count(types.LOG)
                        and Weight() > MaxWeight()
                    ):
                        utils.debug(
                            "Char is ready to sell but is overweight. Dropping some boards to travel."
                        )
                        # magic number 1 here is to not leave char exacly at MaxWeight()
                        drop_special_resources_on_ground_maybe()
                        reduce_weight_to_travel()

                    # ---------------------------------------------------
                    # char is overweighted but doenst have any more logs in bag, go sell
                    # add final maxweight condition to avoid travlling overweighted
                    while (
                        confirm_script_loop_conditions()
                        and count_common(types.BOARD)
                        and not count(types.LOG)
                        and Weight() >= WEIGHT_LIMIT
                        and Weight() <= MaxWeight()
                    ):
                        utils.debug("Char is over the weight limit with only boards")

                        # char tava indo pro vendor com log comum
                        turn_logs_into_boards()
                        refill_tithing_points()
                        begin_sell_and_unload_maybe()
                        return_to_previous_lumber_spot()
                        get_boards_from_ground_maybe()
                        if not lumber():
                            utils.debug("Lumbering failed.")
                            break

                    # char gets stuck if is overweight with only special boards
                    while (
                        confirm_script_loop_conditions()
                        and utils.count_colored(types.BOARD)
                        and not utils.count_common(types.BOARD)
                        and not utils.count(types.LOG)
                        and Weight() >= WEIGHT_LIMIT
                        and Weight() <= MaxWeight()
                    ):
                        utils.debug(
                            "Char is full of only special boards. Going to unload them"
                        )
                        # if fast_cash is on, we can reduce weight by dropping non selleables
                        drop_special_resources_on_ground_maybe()
                        go_to_storage_container()
                        begin_sell_and_unload_maybe()
                        refill_tithing_points()
                        return_to_previous_lumber_spot()
                        get_boards_from_ground_maybe()
                        if not lumber():
                            utils.debug("Lumbering failed.")
                            break

                    # char is overweighted with logs, turn logs into boards to lower weight
                    while (
                        confirm_script_loop_conditions()
                        and utils.count(types.LOG)
                        and Weight() >= WEIGHT_LIMIT
                    ):
                        turn_logs_into_boards()
                        lumber()

                    # char is just overweighted, with no logs and boards
                    while (
                        confirm_script_loop_conditions()
                        and Weight() >= WEIGHT_LIMIT
                        and not utils.count_common(types.BOARD)
                        and not utils.count(types.LOG)
                    ):
                        utils.debug(
                            "Char is overweight without wood resources. Going to unload."
                        )
                        reduce_weight_to_travel()
                        refill_tithing_points()
                        go_to_storage_container()
                        deposit_gold_in_bank()

            utils.debug("finished another runebook")
            utils.wait_lag(10)
