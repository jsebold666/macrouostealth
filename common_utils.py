import io
import os

import time
import json
from datetime import datetime, timedelta
from pprint import pprint

from py_stealth import *

# requests
try:
    import requests
except ModuleNotFoundError:
    print("No 'requests' module found.\n Install it using 'pip install requests' ")
    exit()

# discord_webhook
try:
    from discord_webhook import DiscordWebhook
except ModuleNotFoundError:
    print(
        "No 'discord_webhook' module found.\n Install it using 'pip install discord_webhook' "
    )
    exit()

# =======================================================================
# CONFIGURATION
# =======================================================================

RESPOND_AFK_GUMP = True
PLAY_SOUNDS = True

# =======================================================================
# CONFIGURATION
# =======================================================================

DEBUG = True  # Enable Debug Globally
SUPER_DEBUG = True  # Enable Super Debug Globally


global AUTO_REEQUIP_SET
AUTO_REEQUIP_SET = True
global REFILL_TITHING_POINTS
REFILL_TITHING_POINTS = False

global AUTO_RECONNECT_CHAR
AUTO_RECONNECT_CHAR = False

# =======================================================================
# DELAYS AND TIMERS
# =======================================================================

WAIT_TIME = 500  # Default Wait Time
TRAVEL_SPELL_WAIT_TIME = 2000
WAIT_LAG_TIME = 10000  # Default Wait Lag Time
STUCK_TIME = 10000  # Default Stuck Time
WORLD_SAVE_AVG_TIME = 10000

# SPELLS CASTING TIMES:
GREATER_HEAL_CAST_TIME = 3000
RECALL_CAST_TIME = 3000
SACRED_JOURNEY_CAST_TIME = 2600
CLOSE_WOUNDS_CAST_TIME = 3000

# =======================================================================
# DISCORD WEBHOOK SETUP
# =======================================================================

SEND_DISCORD_DEATH_WARNINGS = True
SEND_DISCORD_AFK_WARNINGS = True

# configure these from insire the scripts that is calling
global DISCORD_WEBHOOK_DEATH_URL
DISCORD_WEBHOOK_DEATH_URL = ""

global DISCORD_WEBHOOK_AFK_URL
DISCORD_WEBHOOK_AFK_URL = "https://discord.com/api/webhooks/900760297307000872/P7USq3ECFRvKNk2w4zpHosk_0rThZ9a9eo_mpc_0wubDG-4II9oCXnX5ARdI1NYG19KC"

# msg that will be send when char dies
global DISCORD_DEATH_MSG
DISCORD_DEATH_MSG = ""

# msg that will be send if char detects AFK gumps
global DISCORD_AFK_MSG
DISCORD_AFK_MSG = ""

# =======================================================================
# AFK GUMP SETTINGS
# =======================================================================

AFK_GUMP = 0xC37345F3
GUMP_DEBUG_FILE = "/Scripts/gump-debug.txt"
AFK_ANSWER_API_URL = "http://150.136.251.245:5000/resolveAFKGump"


# =========================================================================
# REFILL TITHING POINS SETTINGS
# =========================================================================

ANKH_TYPE_LEFT = 0x2
ANKH_TYPE_RIGHT = 0x3
TITHE_GOLD_GUMP_ID = 3746635695
TITHE_GOLD_POSITION = 2
TITHE_ALL_GOLD_BTN = 4
TITHE_ALL_GOLD_OK_BTN = 5

# =======================================================================
# SOUNDS
# =======================================================================

ALARM_SOUND = StealthPath() + "\\Scripts\\sounds\\alarm.wav"
CASH_SOUND = StealthPath() + "\\Scripts\\sounds\\cash.wav"
WIN_SOUND = StealthPath() + "\\Scripts\\sounds\\arty.wav"


# =======================================================================
# VARIABLES
# =======================================================================

# variable to easy access stealth commonly used methods
char = Self()
char_name = CharName()
backpack = Backpack()
bank = ObjAtLayer(BankLayer())
ground = Ground()
dead = Dead()

IN_JAIL = False
GMGumpFound = False
GMGumpAnswered = False
amount_of_gold_in_bank = 0
amount_of_checks_in_bank = 0



# =======================================================================
# JAIL UTILS
# =======================================================================

JAIL_X_TOP_LEFT = 5270
JAIL_Y_TOP_LEFT = 1160
JAIL_X_BOTTOM_RIGHT = 5310
JAIL_Y_BOTTOM_RIGHT = 1190



# =======================================================================
# ITEM TYPES
# =======================================================================

NPC_TYPES = [0x0190, 0x0191]  # female and male npcs
COMMODITY_DEED_BOX_SOUTH = 0x9aa
COMMODITY_DEED_BOX_EAST = 0xe7d
COMMODITY_DEED_BOX_COLOR = 71

SMALL_FORGE_TYPE = 0xfb1
SMALL_FORGE_COLOR = 0

# Type of Log to chop on the backpack
LOG_TYPE = 0x1BDD
BOARD_TYPE = 0x1BD7
GOLD_TYPE = 0xEED
CHECK_TYPE = 0x14F0
CHECK_COLOR = 52

ROBE_TYPE = 0x1f03
DEATH_ROBE_COLOR = 2301

ORE_TYPE = 0x19b9

# =======================================================================
# Check Connection
# =======================================================================

def confirm_critical_loop_conditions():
    if Dead():
        return False
    if not Connected():
        return False

    return True

def connect_char_maybe():
    if not Connected():
        print("Character is not connected. Connecting...")
        Connect()
        while not Connected():
            Wait(500)
    if Connected():
        #adding pause after connecting to try to fix bug where char connects too fast and doenst start macroing
        Wait(1500)


def check_connection():
    if not Connected():
        AddToSystemJournal("No connection.")
        while not Connected():
            AddToSystemJournal("trying to connect...")
            Wait(5000)
            AddToSystemJournal("There is a connection.")
            close_gumps()
    return

def print_uptime():
    if Connected():
        uptime = ConnectedTime()
        print("Char is connected since: %s" % (uptime))
    else:
        print("Char is not connected yet.")

# protection if UOStealth don't find your name. LAG is the main reason
def get_char_name():
    if not CharName() or (CharName() == "Unknown Name"):
        print("Waiting for stealth to detect char name")
        while not CharName() or (CharName() == "Unknown Name"):
            Wait(500)
    else:
        char_name = CharName()
        print("Char name: %s" % (char_name))
        return char_name


def set_travel_method():
    print("Setting travel method")
    if GetSkillValue("Magery") >= 50:
        print("Setting travel spell to Recall")
        return "recall"
    elif GetSkillValue("Chivalry") >= 50:
        print("Setting travel spell to Sacred Journey")
        return "chiva"
    else:
        print("Char doenst have enough skill to travel.")
        return False


# =======================================================================
# Check World is Saving
# =======================================================================


def is_world_saving():
    world_saving_journal_msg = "is saving"

    # if being attacked, travel home, warn player and stop macro
    if InJournal(world_saving_journal_msg) > -1:
        ClearJournal()
        return True
    else:
        return False


def is_world_save_complete():
    world_save_complete_journal_msg = "save complete"

    # if being attacked, travel home, warn player and stop macro
    if InJournal(world_save_complete_journal_msg) > -1:
        ClearJournal()
        return True
    else:
        return False


def check_and_handle_world_save():
    start_time = datetime.now()
    if is_world_saving():
        while not is_world_save_complete():
            Wait(100)
            if checkTimeThreshold(start_time, WORLD_SAVE_AVG_TIME):
                print("Timeout exceeded waiting for world to save.")
                return False
        if is_world_save_complete():
            return True


# =======================================================================
# Check HP, say guards and alarm if HP low
# =======================================================================


def check_hp():
    if GetHP(char) == MaxLife():
        return
    SetAlarm()
    AddToSystemJournal("Someone is attacking you.")
    SendTextToUO("Guards")
    return


# =======================================================================
# Check MANA
# =======================================================================


def check_mana():
    if not Dead():
        # this was 20 and blocking new chars with low int in a loop
        # changed to 10 which is what sacred journey uses
        while Mana() < 10:
            UseSkill("Meditation")
            Wait(5000)
    else:
        print("DEAD ON check_mana! ABORT!")
        return


# =======================================================================
# Tithing Points
# =======================================================================


def get_current_tithing_points():
    current_tithing_points = GetExtInfo()["Tithing_points"]
    return int(current_tithing_points)


def tithe_gold_to_shrine():
    # find an ank to donate money
    SetFindDistance(2)
    if FindType(ANKH_TYPE_LEFT, ground) or FindType(ANKH_TYPE_RIGHT, ground):
        print("achou ankh")
        ankh = FindItem()

        # request tithe gold gump from ankh
        print("setando context menu na ankh")
        SetContextMenuHook(ankh, TITHE_GOLD_POSITION)
        WaitGump(1000)
        print("requested context menu")
        RequestContextMenu(ankh)

        # wait for the ankh donation gump to appear
        waitgumpidWithoutUseObject(TITHE_GOLD_GUMP_ID)
        while not waitgumpid(TITHE_GOLD_GUMP_ID, ankh):
            print("waiting for gump to appear")
            Wait(100)

        # click on tithe all gold
        print("tithe gold gump abriu")
        wait_gump_and_press_btn(TITHE_GOLD_GUMP_ID, TITHE_ALL_GOLD_BTN)
        waitgumpidWithoutUseObject(TITHE_GOLD_GUMP_ID)
        while not waitgumpid(TITHE_GOLD_GUMP_ID, ankh):
            print("waiting for gump to appear")
            Wait(100)

        print("tithe gold clickando OK DOAR")
        wait_gump_and_press_btn(TITHE_GOLD_GUMP_ID, TITHE_ALL_GOLD_OK_BTN)

        # confirm on journal donation succeeded
        tithe_gold_success_journal_msg = "devotion"
        wait_lag(30)
        if InJournal(tithe_gold_success_journal_msg) > -1:
            ClearJournal()
            print("Donated gold to shrine!")
            return True
        else:
            return False

# =======================================================================
# Dress Utils
# =======================================================================

# Store graphic of common leather suit to search in backpack for LRC pieces

EQUIPMENT_SET_TYPES = {
    "head": {
        "equipped": 0,
        "layers": [HatLayer()],
        "items": {
            "leather_cap": 0x1DB9,
            "bear_mask": 0x1545,
            "deer_mask": 0x1547,
            "wizards_hat": 0x1718,
            "cap": 0x1715,
            "straw_hat": 0x1717,
            "wide_brim_hat": 0x1714,
            "bone_helmet": 0x1451,
            "jester_hat": 0x171C,
            "floppy_hat": 0x1713
        },
    },
    "neck": {
        "equipped": 0,
        "layers": [NeckLayer()],
        "items": {
            "leather_gorget": 0x13C7,
            "mempo": 0x277A
        },
    },
   "torso": {
        "equipped": 0,
        "layers": [TorsoLayer()],
        "items": {
            "leather_tunic": 0x13CC,
            "ninja_jacket": 0x2793,
            "samurai_do": 0x27C6,
            "heart_of_the_lion": 0x1415,
            "violet_courage": 0x1C04,

        },
    },
    "shirt": {
        "equipped": 0,
        "layers": [ShirtLayer()],
        "items": {},
    },
    "torsoH": {
        "equipped": 0,
        "layers": [TorsoHLayer()],
        "items": {},
    },

    "legs": {
        "equipped": 0,
        "layers": [LegsLayer()],
        "items": {"leather_leggings": 0x13CB, "leather_skirt": 0x1C08, "hadaite": 0x278A},
    },
    "pants": {
        "equipped": 0,
        "layers": [PantsLayer()],
        "items": {
            "leather_leggings": 0x13CB,
            "leather_skirt": 0x1C08,
            "fey_leggings": 0x13BE
            },
    },
    "sleeves": {
        "equipped": 0,
        "layers": [ArmsLayer()],
        "items": {
            "leather_sleeves": 0x13CD,
            "Hirosode": 0x277E
        },
    },
    "gloves": {
        "equipped": 0,
        "layers": [GlovesLayer()],
        "items": {
            "leather_gloves": 0x13C6,
            "ringmail_gloves": 0x13EB
        },
    },
    "left_hand": {
        "equipped": 0,
        "layers": [LhandLayer()],
        "items": {
            "shield_of_invulnerability": 0x1BC4
        },
    },
    "right_hand": {
        "equipped": 0,
        "layers": [RhandLayer()],
        "items": {
            "boomstick": 0x2D25
        }
    },
    "waist_hand": {
        "equipped": 0,
        "layers": [WaistLayer()],
        "items": {}
    },
    "ring": {
        "equipped": 0,
        "layers": [RingLayer()],
        "items": {
            "ring_gold": 0x108A,
            "ring_dark": 0x1F09
        },
    },
    "bracelet": {
        "equipped": 0,
        "layers": [BraceLayer()],
        "items": {
            "bracelet_gold": 0x1086,
            "bracelet_dark": 0x1F06
        },
    },
    "shoes": {
        "equipped": 0,
        "layers": [ShoesLayer()], "items": {
            "fur_boots": 0x2307
        }
        },
    "robe": {
        "equipped": 0,
        "layers": [RobeLayer()],
        "items": {
            "robe": 0x1f3
        }
    },
    "cloak": {
        "equipped": 0,
        "layers": [CloakLayer()], "items": {}},
    "ears": {
        "equipped": 0,
        "layers": [EarLayer()], "items": {}},
    "talisman": {
        "equipped": 0,
        "layers": [TalismanLayer()],
        "items": {
            "totem_of_the_void": 0x2F5B,
            "bloodwood_spirit": 0x0000
        },
    },
    "eggs": {
        "equipped": 0,
        "layers": [TalismanLayer()], "items": {}},
}


CHAR_WEARABLE_LAYERS = {
    "hat": HatLayer(),
    "torso": TorsoLayer(),
    "torso_h": TorsoHLayer(),
    "shirt": ShirtLayer(),
    "legs": LegsLayer(),
    "pants": PantsLayer(),
    "arms": ArmsLayer(),
    "neck": NeckLayer(),
    "gloves": GlovesLayer(),
    "left_hand": LhandLayer(),
    "right_hand": RhandLayer(),
    "ring": RingLayer(),
    "waist": WaistLayer(),
    "bracelet": BraceLayer(),
    "shoes": ShoesLayer(),
    # "robe": RobeLayer(),
    "cloak": CloakLayer(),
    "earrings": EarLayer(),
    "talisman": TalismanLayer(),
    "eggs": EggsLayer(),
}

def check_if_set_saved_and_equip():
    set_saved = False
    array_of_eqps = []
    for set_slot in EQUIPMENT_SET_TYPES:
        # if piece is already equipped, theres nothing to be done
        if "equipped" in EQUIPMENT_SET_TYPES[set_slot] and EQUIPMENT_SET_TYPES[set_slot]["equipped"] != 0:
            #set is saved. equip it
            set_saved = True
            break
    if set_saved is True:
        for set_slot in EQUIPMENT_SET_TYPES:
            if "equipped" in EQUIPMENT_SET_TYPES[set_slot]:
                array_of_eqps.append([int(EQUIPMENT_SET_TYPES[set_slot]["layers"][0]), EQUIPMENT_SET_TYPES[set_slot]["equipped"]])
        equip_set(array_of_eqps)
        return True
    return False


def equip_set(array_of_eqps):
    start_time = datetime.now()
    # add check to array to avoid index out of range error
    if len(array_of_eqps) > 0:
        # iterate over dict of possible layers of equippment

        for eqp in array_of_eqps:
            # if layer is not equipped with piece saved in CHAR_SET, equip it
            while ObjAtLayer(eqp[0]) != eqp[1]:
                Wait(25)
                print(
                    "Equipping item: "+str(eqp[1])+" in layer: "+str(eqp[0])
                )
                Equip(eqp[0], eqp[1])
                Wait(25)
                if checkTimeThreshold(start_time, 4000):
                    print(
                        "More than 4 seconds trying to equip item. Breaking..."
                    )
                    break
        return

def equip_set_maybe():
    # check if suit is equiped and if not, equip it
    if AUTO_REEQUIP_SET:
        print("-------------------------------------")
        find_save_and_equip_char_set()
        print("Set equipped and saved.")
        print("-------------------------------------")
    else:
        print(
            "Could not find any usable piece in %s backpack. Please equip char manually"
            % (char_name)
        )

def find_save_and_equip_char_set():
    #print(EQUIPMENT_SET_TYPES)
    if check_if_set_saved_and_equip() is True:
        print("True")
        return True
    # get the item main item spot (head, chest, etc...)
    for set_slot in EQUIPMENT_SET_TYPES:
        # get the layers array for current set slot
        for layer in EQUIPMENT_SET_TYPES[set_slot]["layers"]:
            # if piece is already saved and equipped, theres nothing to be done
            if EQUIPMENT_SET_TYPES[set_slot].get("equipped") != 0 and ObjAtLayer(layer) > 0:
                break
            # if piece is saved but not equipped, equip it
            elif EQUIPMENT_SET_TYPES[set_slot].get("equipped") != 0 and ObjAtLayer(layer) == 0:
                print("Equipping saved item in %s slot." % (set_slot))
                item = EQUIPMENT_SET_TYPES[set_slot].get("equipped")
                print("teste item %s" % (item))
                Equip(layer, item)
                wait_lag(200)
                break
            # if piece is not saved but is equipped, save it
            elif EQUIPMENT_SET_TYPES[set_slot].get("equipped") == 0 and ObjAtLayer(layer) > 0:
                
                print("Piece already dressed but not saved. Saving it")
                #print(EQUIPMENT_SET_TYPES[set_slot]["equipped"] )
                EQUIPMENT_SET_TYPES[set_slot]["equipped"] = ObjAtLayer(layer)
                #print(ObjAtLayer(layer))
                #print(set_slot)
                #print(layer)
                #print(EQUIPMENT_SET_TYPES[set_slot]["equipped"] )
                break
            # if piece is not saved, not dressed, we'll search in every layer for a possible item to equip
            elif EQUIPMENT_SET_TYPES[set_slot].get("equipped") == 0 and ObjAtLayer(layer) <= 0:
                for item in EQUIPMENT_SET_TYPES[set_slot].get("items"):
                    if FindType(EQUIPMENT_SET_TYPES[set_slot]["items"].get(item), Backpack()):
                        print(
                            "Found %s in backpack and equipping it."
                            % (EQUIPMENT_SET_TYPES[set_slot]["items"][item])
                        )
                        item = FindItem()
                        EQUIPMENT_SET_TYPES[set_slot]["equipped"] = item
                        start_time = datetime.now()
                        while ObjAtLayer(layer) <= 0:
                            Equip(layer, item)
                            wait_lag(200)

                            if checkTimeThreshold(start_time, 4000):
                                print("Timeout trying to dress an item. Breaking..")
                                break
                    # else:
                    #     print(
                    #         "Could not find %s to equip on %s"
                    #         % (
                    #             item,
                    #             set_slot,
                    #         )
                    #     )
                        # print("Couldnt find any %s in backpack to equip in %s" %(set_slot, EQUIPMENT_SET_TYPES[set_slot]["layers"][layer]))

    return True


def dress_char_suit():
    # add check to array to avoid index out of range error
    if len(CHAR_WEARABLE_LAYERS) > 0:
        # iterate over dict of possible layers of equippment

        for layer in CHAR_WEARABLE_LAYERS:
            # if layer is not equipped with piece saved in CHAR_SET, equip it
            while ObjAtLayer(CHAR_WEARABLE_LAYERS.get(layer)) != CHAR_SET_PIECES.get(
                layer
            ):
                Wait(25)
                print(
                    "Equipping item: %s in layer: %s"
                    % (CHAR_SET_PIECES.get(layer), CHAR_WEARABLE_LAYERS.get(layer))
                )
                Equip(CHAR_WEARABLE_LAYERS.get(layer), CHAR_SET_PIECES.get(layer))
                Wait(25)
                # break loop if stuck for more than 3 seconds
                if checkTimeThreshold(start_time, 3000):
                    print(
                        "More than 8 seconds waiting to move gold to bank. Probably lag..."
                        % (CharName(), STORAGE_CONTAINER)
                    )
                    break

        return
    else:
        print("Cant find any suit piece to dress in char")
        return


def is_suit_equipped():
    equipped_layers = 0
    for x in wearable_layers:
        object_at_layer = ObjAtLayerEx(x, char)
        if object_at_layer != 0:
            equipped_layers += 1

    # if number of layers verified match total number of layers, return true
    # the ideal would be the check to match the number of actual wearable_layers, but most chars dont use all layers, like shoes and ears, so 7 covers all basic set layers (tunic, legs, gorget, etc..)
    print("equiped layers %s" % (equipped_layers))
    if equipped_layers >= 7:
        return True
    else:
        return False


def MyUnDress():
    for j in range(len(CHAR_WEARABLE_LAYERS)):
        print("UNEquiping")
        if UnEquip(CHAR_WEARABLE_LAYERS[j]):
            Wait(1000)
    return True

# =======================================================================
# Check Insured
# =======================================================================


def is_suit_insured():
    equipped_layers = []
    # first populate a list with only the layers with equipped items
    # its very important that suit is already equipped when char gets here
    for layer in CHAR_WEARABLE_LAYERS:
        if ObjAtLayer(CHAR_WEARABLE_LAYERS.get(layer)) > 0:
            equipped_layers.append(CHAR_WEARABLE_LAYERS.get(layer))

    # print("teste array euipped item")
    # print(equipped_layers)

    for i, layer in enumerate(equipped_layers):
        # obj = ObjAtLayerEx(equipped_layers, char)
        obj =  ObjAtLayer(equipped_layers[i])
        if obj != 0:
            ClickOnObject(obj)
            item_details = GetTooltip(obj)
            item_details_stringified = str(GetTooltip(obj))
            item_name = GetAltName(obj)
            # print("item details")
            # print(item_details)
            # print(item_details[0])
            # print(item_details[1])
            if item_details_stringified.find("Insured") < 0 and item_details_stringified.find("Blessed") < 0:
                print("Non Insured and non blessed wearable found! ")
                print("Item details: %s" % (item_details))
                print("Item name: %s" % (item_name))
                print("Blesses: %s" % (str(item_details_stringified.find("Blessed"))))
                print("Insured: %s" % (str(item_details_stringified.find("Insured"))))
                return False
    return True


# =======================================================================
# ITEM UTILITIES
# =======================================================================
def sell_item_to_npc(item_type, npc_id):
    start_time = datetime.now()
    AutoSell(item_type, 0, 999)
    SetContextMenuHook(npc_id, 2)

    # only sells common items with color 0
    while has_common_item_in_backpack(item_type):
        RequestContextMenu(npc_id)
        wait_lag(50)
        if checkTimeThreshold(start_time, 10000):
            print("Timeout trying to sell to NPC. Breaking...")
            break

    # reset context
    SetContextMenuHook(0, 0)
    # reset autosell
    AutoSell(0, 0, 0)
    close_gumps()


# finds item with any color
def has_item_in_backpack(item_type):
    if FindType(item_type, backpack):
        return FindItem()
    else:
        return False

# finds item with color 0
def has_common_item_in_backpack(item_type):
    if FindTypeEx(item_type, 0, backpack, True):
        return FindItem()
    else:
        return False

# finds item with any color != 0
def has_colored_item_in_backpack(item_type):
    if FindTypeEx(item_type, -1, Backpack(), True):
        return FindItem()
    else:
        return False

# =====================================================================
# Helper functions to find commonly used items in game
# =====================================================================

def has_gold_in_backpack():
    return has_item_in_backpack(GOLD_TYPE)

def has_gold_in_backpack():
    return has_item_in_backpack(GOLD_TYPE)

def has_common_item_in_ground(item_type):
    if FindType(item_type, Ground()):
        return FindItem()
    else:
        return False

# helpers for the lumber bot
def has_logs_in_backpack():
    return has_item_in_backpack(LOG_TYPE)

def has_common_boards_in_backpack():
    return has_common_item_in_backpack(BOARD_TYPE)

def has_boards_in_backpack():
    return has_item_in_backpack(BOARD_TYPE)

def has_colored_boards_in_backpack():
    return has_colored_item_in_backpack(BOARD_TYPE)

# helpers for the miner bot
def has_ores_in_backpack():
    return has_item_in_backpack(ORE_TYPE)

def has_common_ingots_in_backpack():
    return has_common_item_in_backpack(INGOT_TYPE)

def has_ingots_in_backpack():
    return has_item_in_backpack(INGOT_TYPE)

def has_colored_ingots_in_backpack():
    return has_colored_item_in_backpack(INGOT_TYPE)
# finds item with color 0



# =====================================================================
# Quantity and count item utils
# =====================================================================

def get_item_quantity(item_type, container_to_search_in):
    if FindType(item_type, container_to_search_in):
        return FindFullQuantity()
    else:
        return 0

def get_common_item_quantity(item_type, container_to_search_in):
    if FindTypeEx(item_type, 0, container_to_search_in, False):
        quantity = FindFullQuantity()
    else:
        return 0


def get_colored_item_quantity(item_type, item_color, container_to_search_in):
    if FindTypeEx(item_type, item_color, container_to_search_in, False):
        return FindFullQuantity()
    else:
        return 0

# Count commonly used items in backpack

def count_gold_in_backpack():
    return get_item_quantity(GOLD_TYPE, backpack)

def count_logs_in_backpack():
    return get_item_quantity(LOG_TYPE, backpack)

def count_boards_in_backpack():
    return get_item_quantity(BOARD_TYPE, backpack)


# Count commonly used items in bank

def count_gold_in_bank():
    return get_item_quantity(GOLD_TYPE, ObjAtLayer(BankLayer()))

def count_checks_in_bank():
    return get_colored_item_quantity(CHECK_TYPE, CHECK_COLOR, ObjAtLayer(BankLayer()))


# Count commonly used items in ground

def count_boards_in_ground(bank):
    return CountGround(BOARD_TYPE)


def make_check_maybe():
    amount_of_gold_in_bank = count_gold_in_bank()
    if amount_of_gold_in_bank > 1100000:
        print(
            "Char has %d gold in the bank. Making check..." % (amount_of_gold_in_bank)
        )
        initial_amount_of_checks_in_bank = count_checks_in_bank()
        UOSay("check 1000000")
        wait_lag(10)
        if count_checks_in_bank() > initial_amount_of_checks_in_bank:
            print("Char just made a 1kk check!")
            try:
                PlayWav(CASH_SOUND)
            except:
                pass
        else:
            print("Char has enought money to make a 1kk check, but failed.")


def is_char_at_bank():
    UOSay("bank")
    wait_lag(10)
    bank_container = LastContainer()
    # FIXME: this is always returning true even if char is not at bank

    print("teste bank container %s" %(bank_container))
    if bank_container > 0:
        print("found bank?")
        return True
    else:
        print("didnt find")
        return False


def get_char_current_balance():
    SetContextMenuHook(char, 2)
    WaitGump(1000)
    RequestContextMenu(char)

    wait_lag(50)
    waitgumpidWithoutUseObject(3465474465)

    current_balance = 0

    for gump in range(GetGumpsCount()):
        idd = GetGumpID(gump)
        if idd == 3465474465:

            # gump do insurance menu
            infogump = GetGumpInfo(gump)
            current_balance = infogump["Text"][0][0]
        else:
            break

    close_gumps()

    return int(current_balance)




def walkStepCheckingGump(direction, gumpID, times):
    SetMoveThroughNPC(True)
    for i in range(times):
        Step(direction, False)
        if GumpExists(gumpID):
            return
        Wait(18)


def remove_death_robe():
    # first lets move the robe to the backpack
    robe = 0
    if ObjAtLayer(RobeLayer()) > 0:
        robe_color = GetColor(ObjAtLayer(RobeLayer()))
        if robe_color == DEATH_ROBE_COLOR:
            print("Character is dressing a death robe. Moving it to backpack")
            robe = ObjAtLayer(RobeLayer())
            MoveItem(robe, 1, Backpack(), 0, 0, 0)
            wait_lag(100)

    elif FindTypeEx(ROBE_TYPE, 0, backpack, False):
        print("Death Robe found in backpack. Dropping it on the ground.")
        robe = FindItem()

    if robe != 0:
        drop_item_to_random_direction(robe, 1, backpack)
        wait_lag(10)
        print("Death Robe dropped on the ground")
        return True

# serial do healer de cove 0x8aacf
def ress():
    if Dead():

        print("%s is dead! Trying to ress." % (CharName()))
        CHAR_MURDERED_GUMP = 523845830
        # If char was murdered, there is a gump present we need to close first
        if GumpExists(CHAR_MURDERED_GUMP):
            print("%s was murdered by another player" % (CharName()))
            wait_gump_and_press_btn(CHAR_MURDERED_GUMP, 1, 5)

        currentX = GetX(char)
        currentY = GetY(char)

        while not InGump("Delucia") and not InGump("Cove"):
            HelpRequest()
            wait_lag(10)
            waitgumpidWithoutUseObject(0xB3423A1D, 5)
            wait_lag(10)
            wait_gump_and_press_btn(0xB3423A1D, 2, 5)
        wait_lag(10)
        waitgumpidWithoutUseObject(0x1E88CA33, 5)
        wait_lag(200)

        if InGump("Delucia"):
            AddToSystemJournal("T2A Ress")
            # T2A - DELUCIA RESS
            wait_gump_and_press_btn(0x1E88CA33, 2, 5)
            Wait(1000)
            close_gumps()

            while currentX == GetX(char) and currentY == GetY(char):
                AddToSystemJournal("Char paralyzed. Waiting to be teleported - T2A.")
                Wait(5000)
            AddToSystemJournal("Moving to Healer - T2A.")
            NewMoveXY(5208, 3993, True, 0, True)
            NewMoveXY(5201, 3997, True, 0, True)
            walkStepCheckingGump(7, 0xB04C9A31, 20)
            starttime = datetime.now()
            count = 0

            while not GumpExists(0xB04C9A31):
                count = count + 1
                print("Trying to ress again. try:" + str(count))

                # Gump nao existe.... sair e entrar no healer de novo
                walkStepCheckingGump(3, 0xB04C9A31, 10)

                # if ((InJournalBetweenTimes("cannot be resurrected", starttime, datetime.now())) > 0): #Healer não aceita ressurect!!! Esperar 5 minutos
                #    print("Healer não aceita ressurect!!! Esperar 5 minutos e tentar de novo")
                #    Wait(300000)
                Wait(5000)
                walkStepCheckingGump(10, 0xB04C9A31, 10)
                if datetime.now() >= starttime + timedelta(minutes=10):
                    print(
                        "SECURITY BREAK RESS!!! COULD NOT RESS AFTER "
                        + str(count)
                        + "TRIES! QUITING!"
                    )
                    SetARStatus(False)

                    Disconnect()
                    exit()
        else:
            AddToSystemJournal("Going to the healer in cove to ress")
            # FEL OR TRAM - COVE RESS
            wait_gump_and_press_btn(0x1E88CA33, 6, 5)
            Wait(1000)
            close_gumps()

            while currentX == GetX(char) and currentY == GetY(char):
                AddToSystemJournal("Char paralyzed. Waiting to be teleported.")
                Wait(5000)

            AddToSystemJournal("Moving to Healer.")
            # NewMoveXY(2249,1229,True,0,True)
            NewMoveXY(
                2247, 1229, True, 0, True
            )  # fix by ivan, move correctly to coves healer
            print("%s next to the Healer." % (CharName()))
            walkStepCheckingGump(6, 0xB04C9A31, 6)

            starttime = datetime.now()
            count = 0

            while not GumpExists(0xB04C9A31):
                count = count + 1
                print("Trying to ress again. try:" + str(count))
                # Gump nao existe.... sair e entrar no healer de novo
                walkStepCheckingGump(2, 0xB04C9A31, 6)
                # if ((InJournalBetweenTimes("cannot be resurrected", starttime, datetime.now())) > 0): #Healer não aceita ressurect!!! Esperar 5 minutos
                #    print("Healer não aceitou ressurect!!! Esperar 5 minutos e tentar de novo")
                #    Wait(300000)
                Wait(5000)
                walkStepCheckingGump(6, 0xB04C9A31, 6)
                if datetime.now() >= starttime + timedelta(minutes=10):
                    print(
                        "SECURITY BREAK RESS!!! COULD NOT RESS AFTER "
                        + str(count)
                        + "TRIES! QUITING!"
                    )
                    SetARStatus(False)

                    Disconnect()
                    exit()

        waitgumpidWithoutUseObject(0xB04C9A31, 5)

        wait_gump_and_press_btn(0xB04C9A31, 1, 5)
        wait_lag(100)

        remove_death_robe()

        equip_set_maybe()

        return


def heal_self_until_max_hp():
    check_mana()

    start_time = datetime.now()
    while GetHP(char) < GetMaxHP(char):
        check_mana()
        print("Char is healing")
        if GetSkillValue("Magery") >= 50:
            Cast("Greater Heal")
            WaitTargetSelf()
            wait_lag(GREATER_HEAL_CAST_TIME)
        elif GetSkillValue("Chivalry") >= 50:
            Cast("Close Wounds")
            WaitTargetSelf()
            wait_lag(CLOSE_WOUNDS_CAST_TIME)

        if checkTimeThreshold(start_time, 7000):
            print("Timeout while healing. Breaking...")
            break
    return


def heal_self():
    check_mana()
    if GetSkillValue("Magery") >= 50:
        Cast("Greater Heal")
        WaitTargetSelf()
        wait_lag(GREATER_HEAL_CAST_TIME)
        Cast("Greater Heal")
        WaitTargetSelf()
        wait_lag(GREATER_HEAL_CAST_TIME)
        Cast("Greater Heal")
        WaitTargetSelf()
        wait_lag(GREATER_HEAL_CAST_TIME)
    elif GetSkillValue("Chivalry") >= 50:
        Cast("Close Wounds")
        WaitTargetSelf()
        wait_lag(CLOSE_WOUNDS_CAST_TIME)
        Cast("Close Wounds")
        WaitTargetSelf()
        wait_lag(CLOSE_WOUNDS_CAST_TIME)
        Cast("Close Wounds")
        WaitTargetSelf()
        wait_lag(CLOSE_WOUNDS_CAST_TIME)


# =================================================================================
# Journal Utils
# =================================================================================


def is_char_being_attacked():
    under_attack_journal_msg = "is attacking you"

    if InJournal(under_attack_journal_msg) > -1:
        ClearJournal()
        return True
    else:
        return False


# =================================================================================
# Other Utils
# =================================================================================


def wait_lag(wait_time=WAIT_TIME, lag_time=WAIT_LAG_TIME):
    Wait(wait_time)
    CheckLag(lag_time)
    return


def debug(message):
    if DEBUG:
        print(message)
        ClientPrintEx(char, 66, 1, message)


def superDebug(message):
    if SUPER_DEBUG:
        print(message)
        ClientPrintEx(char, 66, 1, message)


def checkTimeThreshold(starttime, time_limit_in_miliseconds):
    currentTime = datetime.now()
    timeDifference = currentTime - starttime
    differenceInMiliseconds = timeDifference.total_seconds() * 1000
    if differenceInMiliseconds > time_limit_in_miliseconds:
        return True
    return False


def reduce_weight_to_travel(
        itemTypeToDrop, color=0xFFFF, qtdToDrop=7, dropX=-1, dropY=-1
):
    starttime = datetime.now()
    if itemTypeToDrop == BOARD_TYPE:
        qtdeToDrop = MaxWeight() - Weight()

    while Weight() > MaxWeight():
        check_connection()
        drop_item_to_reduce_weight(itemTypeToDrop, color, dropX, dropY, qtdToDrop)
        wait_lag(100)
        if checkTimeThreshold(starttime, 5000):
            print(
                "7 seconds passed since trying to drop item. Maybe the tile is blocked? Trying to move char to make sure"
            )
            # step 1 tile south just to make sure it isnt the char itself blocking the rune
            Step(4, False)
            wait_lag(100)
            Step(4, False)
            wait_lag(100)
            # reset time to start counter again
            starttime = datetime.now()

        if checkTimeThreshold(starttime, 4000):
            print(
                "7 seconds passed since trying to drop item. Maybe the tile is blocked? Trying to move char to make sure"
            )
            # step 1 tile south just to make sure it isnt the char itself blocking the rune
            Step(4, False)
            wait_lag(100)
            Step(4, False)
            wait_lag(100)
            # reset time to start counter again
            starttime = datetime.now()
    return


def drop_item_to_reduce_weight(itemType, color, dropX=-1, dropY=-1, qtdToDrop=7):
    counter = 0

    if Dead():
        print("DEAD ON DROPPING ITEM! ABORT!")
        return
    if Weight() < MaxWeight():
        return
    if FindTypeEx(itemType, color, Backpack(), False):
        print("Dropping %d %s" % (qtdToDrop, itemType))
        wait_lag(100)
        Drop(FindItem(), qtdToDrop, GetX(char) + dropX, GetY(char) + dropY, GetZ(char))
        wait_lag(100)

    return


# ===================================================================
# GUMP Utils
# ===================================================================


def close_gumps():

    while IsGump():
        if not Connected():
            return False
        if not IsGumpCanBeClosed(GetGumpsCount() - 1):
            return False
        # WaitGump('0')
        else:
            CloseSimpleGump(GetGumpsCount() - 1)
    return True


def waitgumpid(gumpid, object, timeout=15):
    maxcounter = 0
    UseObject(object)
    while maxcounter < timeout * 10:
        if IsGump():
            for currentgumpnumb in range(0, (GetGumpsCount())):
                currentgump = GetGumpInfo(currentgumpnumb)
                if (
                    "GumpID" in currentgump
                ):  # got to check if key exists or we might get an error
                    if currentgump["GumpID"] == gumpid:
                        return True
                if IsGumpCanBeClosed(currentgumpnumb):
                    CloseSimpleGump(currentgumpnumb)
        maxcounter += 1
        CheckLag(100000)
    return False


def waitgumpidWithoutUseObject(gumpid, timeout=15):
    maxcounter = 0
    while maxcounter < timeout * 10:
        if IsGump():
            for currentgumpnumb in range(0, (GetGumpsCount())):
                currentgump = GetGumpInfo(currentgumpnumb)
                if (
                    "GumpID" in currentgump
                ):  # got to check if key exists or we might get an error
                    if currentgump["GumpID"] == gumpid:
                        return True
                if IsGumpCanBeClosed(currentgumpnumb):
                    CloseSimpleGump(currentgumpnumb)
        maxcounter += 1
        CheckLag(100000)
    return False


def wait_gump_and_press_btn(gumpid, number=0, pressbutton=True, timeout=15):
    maxcounter = 0
    while maxcounter < timeout * 10:
        if IsGump():
            for currentgumpnumb in range(0, (GetGumpsCount())):
                currentgump = GetGumpInfo(currentgumpnumb)
                if (
                    "GumpID" in currentgump
                ):  # got to check if key exists or we might get an error
                    if currentgump["GumpID"] == gumpid:
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


def waitgumpid_checkbox(gumpid, number=0, pressbutton=True, value=0, timeout=15):
    maxcounter = 0
    while maxcounter < timeout * 10:
        if IsGump():
            for currentgumpnumb in range(0, (GetGumpsCount())):
                currentgump = GetGumpInfo(currentgumpnumb)
                if (
                    "GumpID" in currentgump
                ):  # got to check if key exists or we might get an error
                    if currentgump["GumpID"] == gumpid:
                        if pressbutton:
                            NumGumpCheckBox(currentgumpnumb, number, value)
                        else:
                            return currentgump
                        return True
                if IsGumpCanBeClosed(currentgumpnumb):
                    CloseSimpleGump(currentgumpnumb)
        maxcounter += 1
        CheckLag(100000)
    return False


def waitgumpid_textentry(gumpid, textEntryId=0, value="", timeout=15):
    maxcounter = 0
    while maxcounter < timeout * 10:
        if IsGump():
            for currentgumpnumb in range(0, (GetGumpsCount())):
                currentgump = GetGumpInfo(currentgumpnumb)
                if (
                    "GumpID" in currentgump
                ):  # got to check if key exists or we might get an error
                    if currentgump["GumpID"] == gumpid:
                        print("ACHOU TEXT ENTRIE!")
                        NumGumpTextEntry(currentgumpnumb, textEntryId, value)
                        return True
                if IsGumpCanBeClosed(currentgumpnumb):
                    CloseSimpleGump(currentgumpnumb)
        maxcounter += 1
        CheckLag(100000)
    return False


def GumpExists(gumpid):
    for i in range(GetGumpsCount()):
        if gumpid and gumpid == GetGumpID(i):
            return True
    return False


def get_in_gump_field_value(gump_text):
    found = None
    t = 1
    while found == None:
        # print ("while")
        for i in range(GetGumpsCount()):
            infogump = GetGumpInfo(i)
            # print ("for")
            index = i
            if not found and len(infogump["XmfHtmlGump"]) > 0:
                # for j in infogump['XmfHtmlGump']:
                #    GetClilocByID(x['ClilocID']).upper()
                # print("HTML")
                found = next(
                    (
                        GetClilocByID(x["ClilocID"]).upper()
                        for x in infogump["XmfHtmlGump"]
                        if gump_text.upper() in GetClilocByID(x["ClilocID"]).upper()
                    ),
                    None,
                )
                break
            if not found and len(infogump["XmfHTMLGumpColor"]) > 0:
                # print("HTML color")
                found = next(
                    (
                        GetClilocByID(x["ClilocID"]).upper()
                        for x in infogump["XmfHTMLGumpColor"]
                        if gump_text.upper() in GetClilocByID(x["ClilocID"]).upper()
                    ),
                    None,
                )
                break
            elif not found and len(infogump["Text"]) > 0:
                # print("text")
                found = next(
                    (
                        x[0].upper()
                        for x in infogump["Text"]
                        if text.upper() in x[0].upper()
                    ),
                    None,
                )
                break
        Wait(100)
        t += 1
        if t > 10:
            return found
        CheckLag()
        # if value != 999:
        #     NumGumpButton(GetGumpsCount() - 1, value)
    return found


def InGump(text, value=999):
    found = None
    t = 1
    while found == None:
        # print ("while")
        for i in range(GetGumpsCount()):
            infogump = GetGumpInfo(i)
            # print ("for")
            index = i
            if not found and len(infogump["XmfHtmlGump"]) > 0:
                # for j in infogump['XmfHtmlGump']:
                #    GetClilocByID(x['ClilocID']).upper()
                # print("HTML")
                found = next(
                    (
                        GetClilocByID(x["ClilocID"]).upper()
                        for x in infogump["XmfHtmlGump"]
                        if text.upper() in GetClilocByID(x["ClilocID"]).upper()
                    ),
                    None,
                )
                break
            if not found and len(infogump["XmfHTMLGumpColor"]) > 0:
                # print("HTML color")
                found = next(
                    (
                        GetClilocByID(x["ClilocID"]).upper()
                        for x in infogump["XmfHTMLGumpColor"]
                        if text.upper() in GetClilocByID(x["ClilocID"]).upper()
                    ),
                    None,
                )
                break
            elif not found and len(infogump["Text"]) > 0:
                # print("text")
                found = next(
                    (
                        x[0].upper()
                        for x in infogump["Text"]
                        if text.upper() in x[0].upper()
                    ),
                    None,
                )
                break
        Wait(100)
        t += 1
        if t > 10:
            return found
        CheckLag()
    if value != 999:
        NumGumpButton(GetGumpsCount() - 1, value)
    return found


def InGumpRegexIN_UPPERCASE(regex):
    t = 1
    while True:
        # print ("while")
        for i in range(GetGumpsCount()):
            print("loop")
            infogump = GetGumpInfo(i)
            # print ("for")
            index = i

            if len(infogump["XmfHtmlGump"]) > 0:
                print("HTMLGump")
                for gump_line in infogump["XmfHtmlGump"]:
                    print(str(GetClilocByID(gump_line["ClilocID"])))
                    regexSearch = re.search(
                        regex, GetClilocByID(gump_line["ClilocID"]).upper()
                    )
                    if regexSearch is not None:
                        return regexSearch

            if len(infogump["XmfHTMLGumpColor"]) > 0:
                print("XmfHTMLGumpColor")
                for x in infogump["XmfHTMLGumpColor"]:
                    print(str(GetClilocByID(x["ClilocID"])))
                    regexSearch = re.search(regex, GetClilocByID(x["ClilocID"]).upper())
                    if regexSearch is not None:
                        return regexSearch

            elif len(infogump["Text"]) > 0:
                print("Text")
                for x in infogump["Text"]:
                    print(x[0])
                    regexSearch = re.search(regex, x[0].upper())
                    if regexSearch is not None:
                        return regexSearch
        Wait(100)
        t += 1
        if t > 5:
            return False
        CheckLag()


# ==========================================================================
# TRAVEL UTILS
# ==========================================================================


def define_travel_spell_wait_time():
    global TRAVEL_SPELL_WAIT_TIME
    TRAVEL_SPELL_WAIT_TIME = 3000


def enter_gate_maybe():
    # if gate is open, click it to enter
    if FindType(0x0F6C, Ground()):
        UseObject(FindItem())
        wait_gump_and_press_btn(3899019871, 2)


def has_char_location_changed(previous_x_location, previous_y_location):
    if GetX(char) != previous_x_location or GetY(char) != previous_y_location:
        return True
    else:
        return False


def is_current_rune_blocked():
    location_is_blocked_journal_msg = "location is blocked"

    if InJournal(location_is_blocked_journal_msg) > 0:
        ClearJournal()
        return True
    else:
        return False


def move_char_to_random_direction():
    coord_x, coord_y = GetX(char), GetY(char)
    x, y = coord_x, coord_y
    start_time = datetime.now()
    while not has_char_location_changed(x, y) and confirm_critical_loop_conditions():
        for direction in range(1, 8):
            # walk 3 steps
            for i in range(0, 3):
                Step(direction, False)
                wait_lag(10)

            if has_char_location_changed(x, y):
                print("Moved char 1 tile.")
                return True
        if checkTimeThreshold(start_time, 4000):
            print("Timeout trying to move char. Breaking..")

    if has_char_location_changed(x, y):
        print("Moved char 1 tile.")
        return True
    else:
        return False


def travel(travel_method, runebook_name, rune_number):
    wait_lag(1)
    usingregs = list(
        (range(-1, 100, 6))
    )  # 5, 11, 17, 23, 29, 35, 41, 47, 53, 59, 65, 71, 77, 83, 89, 95
    usingcharges = list(
        (range(-4, 98, 6))
    )  # 2, 8, 14, 20, 26, 32, 38, 44, 50, 56, 62, 68, 74, 80, 86, 92
    usinggate = list(
        range(0, 102, 6)
    )  # 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 96
    usingchiva = list(range(1, 103, 6))  #

    if open_runebook(runebook_name):
        if Dead():
            print("DEAD ON RECALL! ABORT!")
            return False
        if Weight() >= MaxWeight() + 3:
            print("OVERWEIGTH ON RECALL LOOP! ABORT!")
            return False

        # Only print info if its the Woods runebooks.
        if runebook_name != "Home":
            print("Travelling to rune %s on %s runebook" % (rune_number, runebook_name))

        starttime = datetime.now()

        # click on the respective runebook button, depending on travel method
        if travel_method == "chiva":
            wait_gump_and_press_btn(1431013363, usingchiva[rune_number], True)
            wait_lag(SACRED_JOURNEY_CAST_TIME)
        elif travel_method == "recall":
            wait_gump_and_press_btn(1431013363, usingregs[rune_number], True)
            wait_lag(RECALL_CAST_TIME)
        elif travel_method == "gate":
            wait_gump_and_press_btn(1431013363, usinggate[rune_number], True)
            Wait(wait_time)
            wait_lag(GATE_TRAVEL_CAST_TIME)
            enter_gate_maybe()
        elif travel_method == "charge":
            runebook_gump = wait_gump_and_press_btn(
                1431013363, usingcharges[rune_number], False
            )
            if runebook_gump:
                if "Text" in runebook_gump:
                    # checking if we got charges
                    if int(runebook_gump["Text"][0][0]) > 1:
                        wait_gump_and_press_btn(1431013363, usingcharges[rune_number])
                        # less than minimum charges
                    else:
                        print(
                            "Runebook %s is out of charges. Refill runebook with scrolls"
                            % (runebook_name)
                        )
                        return False
        else:
            debug("Cant Travel if TRAVEL method is not defined")
            return False

        return True


# Usage: runebook("runebook name", "recall/gate/charges", rune number)
def travel_to(runebook_name, travel_method, rune_number, wait_time=4000):

    # store char pos before recalling to see if position changed, indicating sucessfull recall
    retry = 0

    current_rune_blocked = False
    char_x, char_y = GetX(char), GetY(char)
    while not has_char_location_changed(char_x, char_y) and not Dead():
        check_mana()
        starttime = datetime.now()

        if retry >= 1:
            print("Travel retry -> %d x" % (retry))
        if retry > 10:
            print("Travel EXITING -> More than %d retries..." % (retry))
            return False

        if travel(travel_method, runebook_name, rune_number):
            if is_current_rune_blocked():
                ClearJournal()
                # FIXME: have to move char a lot here
                # if char moves just 2 or 3 tiles, GetX and GetY doenst change
                # and script thinks recall failed
                if runebook_name == "Home":
                    print("Location was blocked. Moving char and trying again")
                    move_char_to_random_direction()
                    # reset char pos so function doenst think recall succeeded
                    char_x, char_y = GetX(char), GetY(char)

                else:
                    print(
                        "Location was blocked. Returning true to start lumbering to see if it wanst the char itself blocking the location..."
                    )
                    return True

        if checkTimeThreshold(starttime, 15000):
            print(
                "Char is stuck for more than 15 seconds waiting for location to change. Breaking..."
            )
            break

        # increment retry counter
        retry += 1

    if has_char_location_changed(char_x, char_y):
        #print("Char reached the destination")
        wait_lag(10)
        return True

    if current_rune_blocked:
        return False

    else:
        return False


def open_runebook(name):
    if Dead():
        return False

    if FindType(0x22C5, Backpack()):
        founds = GetFindedList()
        for found in founds:
            splitedToolTip = GetTooltip(found).rsplit("|", 1)
            if len(splitedToolTip) > 0:
                if splitedToolTip[1] in (name):
                    start_time = datetime.now()
                    while not waitgumpid(1431013363, found):
                        Wait(100)
                        if checkTimeThreshold(start_time, 15000):
                            print("Timeout while trying to open runebook. Breaking")
                    return True
    else:
        print("Runebook not found. Trying to open backpack...")
        Wait(10000)
        UseObject(Backpack())
        return False
    return False


# ======================================================================
# Telegram Utils
# ======================================================================
def send_afk_gump_warning(webhook_url, message):
    telegram_bot_url = "https://api.telegram.org/bot%s/warn_afk_gump" % (
        telegram_bot_token
    )
    response = requests.request("POST", webhook_url, headers=headers, data=payload)

    print(response.text.encode("utf8"))
    return response


# ======================================================================
# Discord Utils
# ======================================================================

def send_discord_death_warning():
    if DISCORD_WEBHOOK_DEATH_URL and DISCORD_DEATH_MSG:
        webhook = DiscordWebhook(DISCORD_WEBHOOK_DEATH_URL, content=str(DISCORD_DEATH_MSG))
        webhook.execute()
    return

def send_discord_afk_gump_warning(charFunction=""):
    if DISCORD_AFK_MSG:
        webhook = DiscordWebhook(DISCORD_WEBHOOK_AFK_URL, content=str(DISCORD_AFK_MSG))
        webhook.execute()
        return
    else:
        send_discord_message(
            DISCORD_WEBHOOK_AFK_URL,
            "**(GUMP) @everyone - GUMP DE AFK CHECK DETECTADO!  [Char: "
            + str(CharName())
            + str(charFunction)
            + "]**",
        )

def send_discord_jail_warning(charFunction=""):
    send_discord_message(
        DISCORD_WEBHOOK_AFK_URL,
        "**(JAIL) @everyone - GM RODANDO! CHAR NA JAIL! [Char: "
        + str(CharName())
        + str(charFunction)
        + "]**",
    )


def send_discord_msg_2(url, msg):
    webhook = DiscordWebhook(url, content=str(msg))
    webhook.execute()
    return

def send_discord_message(webhook_url, message):
    webhook = DiscordWebhook(url=webhook_url, content=str(message))
    webhook.execute()

    return


"""def send_discord_message(webhook_url, message, username = "Freddy Krueger", messageColor = "16411130", avatarURL = "https://vignette.wikia.nocookie.net/dcheroesrpg/images/b/b2/Freddy_Krueger.jpg"):
    jsonPayload = {}
    jsonPayload['username'] = username
    jsonPayload['avatar_url'] = avatarURL

    jsonPayload['embeds'] =  []
    embeds = {}
    embeds['description'] = message
    embeds['color'] = messageColor
    jsonPayload['embeds'].append(embeds)

    payload = json.dumps(jsonPayload)

    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", webhook_url, headers=headers, data = payload)
    print(response.text.encode('utf8'))"""


def send_discord_message_multi_lines(
    webhook_url,
    arrayOfMessages,
    username="Freddy Krueger",
    messageColor="16411130",
    avatarURL="https://vignette.wikia.nocookie.net/dcheroesrpg/images/b/b2/Freddy_Krueger.jpg",
):
    jsonPayload = {}
    jsonPayload["username"] = username
    jsonPayload["avatar_url"] = avatarURL

    jsonPayload["embeds"] = []
    for message in arrayOfMessages:
        embeds = {}
        embeds["description"] = message
        embeds["color"] = messageColor
        jsonPayload["embeds"].append(embeds)

    payload = json.dumps(jsonPayload)

    headers = {
        "Content-Type": "application/json",
    }
    response = requests.request("POST", webhook_url, headers=headers, data=payload)
    print(response.text.encode("utf8"))


# ===================================================================
# GM check Utils
# ===================================================================
def is_gm_present():
    global ctime, GMWav, gmcnt
    if gmcnt < 1 :

        if (InJournalBetweenTimes('here?', ctime, datetime.datetime.now()) != -1) :
            PlayWav(GMWav)
            gmcnt += 1
            return True
        if (InJournalBetweenTimes('John:', ctime, datetime.datetime.now()) != -1) :
            PlayWav(GMWav)
            gmcnt += 1
            return True
        if (InJournalBetweenTimes('Styx:', ctime, datetime.datetime.now()) != -1) :
            PlayWav(GMWav)
            gmcnt += 1
            return True
        if (InJournalBetweenTimes('EOS:', ctime, datetime.datetime.now()) != -1) :
            PlayWav(GMWav)
            gmcnt += 1
            return True
        if (InJournalBetweenTimes('GM controlling:', ctime, datetime.datetime.now()) != -1) :
            PlayWav(GMWav)
            gmcnt += 1
            return True
        if (InJournalBetweenTimes('attending', ctime, datetime.datetime.now()) != -1) :
            PlayWav(GMWav)
            gmcnt += 1
            return True
        if (InJournalBetweenTimes('Larson:', ctime, datetime.datetime.now()) != -1) :
            PlayWav(GMWav)
            gmcnt += 1
            return True
        if (InJournalBetweenTimes('Lynae:', ctime, datetime.datetime.now()) != -1) :
            PlayWav(GMWav)
            gmcnt += 1
            return True
        if (InJournalBetweenTimes('Selene:', ctime, datetime.datetime.now()) != -1) :
            play_sound(GM)
            gmcnt += 1
            return True

def perform_routine_checks():
    checkGMGump("lumber")
    check_if_in_jail("lumber")
    check_and_handle_world_save()


def CheckAFK(charFunction=""):
    checkGMGump(charFunction)
    check_if_in_jail(charFunction)
    # while GumpExists(afk_gump):
    #    msg_disco(ProfileName() + ' * AFK GUMP *')
    #    Wait(30000)


def checkGMGump(charFunction=""):
    global GMGumpFound
    if IsGump():
        captcha_response = ""
        print("IsGump")
        print(GetGumpID(GetGumpsCount() - 1))
        print(GetGumpInfo(GetGumpsCount() - 1))
        if GetGumpsCount() > 0:
            id = GetGumpID(GetGumpsCount() - 1)
            if id == AFK_GUMP or id == 0xb3601a01:
                print("Found GUMP")
                print("######FOUND AFK CHECK GUMP ID#########")
                if PLAY_SOUNDS:
                    try:
                        PlayWav(ALARM_SOUND)
                    except:
                        pass
                if GMGumpFound is not True:
                    GMGumpFound = True
                    if SEND_DISCORD_AFK_WARNINGS:
                        send_discord_afk_gump_warning()
                    

                debug("Gumps Count:" + str(GetGumpsCount()))
                # id = GetGumpID(GetGumpsCount()-1)
                debug("Gump Id:" + str(id))
                # gumpFullInfo = GetGumpFullInfo(GetGumpsCount()-1)
                gumpInfo = GetGumpInfo(GetGumpsCount() - 1)
                # with open('gump-debug.txt','w') as file:
                debugGumpFile = open(StealthPath() + GUMP_DEBUG_FILE, "a+")
                # print(gumpInfo)
                debugGumpFile.writelines(
                    "\n\n\n---------------GUMP FOUND! Char:"
                    + str(CharName())
                    + "----------------"
                )
                debugGumpFile.writelines(
                    "\n-------" + str(datetime.now()) + "-------\n"
                )
                json.dump(gumpInfo, debugGumpFile)

                gumpFullLines = GetGumpFullLines(GetGumpsCount() - 1)
                print(gumpFullLines)
                debugGumpFile.writelines("\n-------FULL LINES-------\n")
                json.dump(gumpFullLines, debugGumpFile)
                for gump in range(GetGumpsCount() - 1):
                    idd = GetGumpID(gump)

                    debugGumpFile.writelines("\n-------ID - for-------\n")
                    gumpInfo = GetGumpInfo(gump)
                    json.dump(gumpInfo, debugGumpFile)

                    gumpFullLines = GetGumpFullLines(gump)
                    debugGumpFile.writelines("\n-------FULL LINES - for-------\n")
                    json.dump(gumpFullLines, debugGumpFile)

                debugGumpFile.close()

                if RESPOND_AFK_GUMP:
                    # TRYING TO PRESS CHECKBOX
                    print("PRESSING CHECKBOX")
                    Wait(2000)  # waiting 2 seconds just to pretend
                    button = gumpInfo["GumpButtons"][0]["ReturnValue"]
                    wait_gump_and_press_btn(id, int(button), True, 5)
                    # Wait (600000) # Wait for 10 Minutes
                    
                    Wait(4000)
                    gumpInfo = GetGumpInfo(GetGumpsCount() - 1)
                    Wait(1000)
                    print("Got new Gump Info")
                    print(gumpInfo)
                    debugGumpFile = open(StealthPath() + GUMP_DEBUG_FILE, "a+")
                    # print(gumpInfo)
                    debugGumpFile.writelines(
                        "\n\n\n---------------GUMP FOUND 2! Char:"
                        + str(CharName())
                        + "----------------"
                    )
                    debugGumpFile.writelines(
                        "\n-------" + str(datetime.now()) + "-------\n"
                    )
                    json.dump(gumpInfo, debugGumpFile)
                    debugGumpFile.close()

                    print("Getting CAPTCHA!")
                    retry = 0
                    while not captcha_response.isdigit():
                        print("Trying to solve CAPTCHA for the %d TIME!!" % (retry))
                        captcha_response = requests.post(
                            url=AFK_ANSWER_API_URL, data=json.dumps(gumpInfo)
                        )
                        captcha_response = captcha_response.text
                        retry += 1
                        print("RESPONSE FROM API:"+captcha_response)
                        if retry > 5:
                            print("****TOO MANY RETRIES TRYING TO SOLVE GUMP! BREAKING!***")
                            break
                        Wait(4300)
                    if retry <= 5:
                        waitgumpid_textentry(id, 1, captcha_response, 5)
                        print("AFTER ENTRYING TEXT!!")
                        Wait(4300)
                        wait_gump_and_press_btn(id, 1, True, 5)
                        print("AFTER PRESSING OKAY BUTTON!!")
                    else:
                        waitgumpid_textentry(id, 1, "00", 5)
                        print("Answered '00' on purpose to try to change the gump")
                        Wait(4300)
                        wait_gump_and_press_btn(id, 1, True, 5)
                

            else:
                close_gumps()
    else:
        GMGumpFound = False

#################################################################
# JAIL UTILS
#################################################################

# checks if char is in jail, prints a msg in log and warns in discord
def check_if_in_jail(charFunction):
    if is_char_in_jail():
        if PLAY_SOUNDS:
            try:
                PlayWav(ALARM_SOUND)
            except:
                pass
        print("########IN JAIL!!!########")
        send_discord_jail_warning()
        IN_JAIL = True
        return True


# checks if char is in jail, prints a msg in log and warns in discord
def is_char_in_jail():
    currentX = GetX(char)
    currentY = GetY(char)

    if (currentX >= JAIL_X_TOP_LEFT) and (currentX <= JAIL_X_BOTTOM_RIGHT):
        if (currentY >= JAIL_Y_TOP_LEFT) and (currentY <= JAIL_Y_BOTTOM_RIGHT):
            return True
    else:
        return False


# checks if char is in jail, prints a msg in log and warns in discord
def is_char_is_jail(charFunction=""):
    currentX = GetX(char)
    currentY = GetY(char)

    if (currentX >= JAIL_X_TOP_LEFT) and (currentX <= JAIL_X_BOTTOM_RIGHT):
        if (currentY >= JAIL_Y_TOP_LEFT) and (currentY <= JAIL_Y_BOTTOM_RIGHT):
            if IN_JAIL is not True:
                IN_JAIL = True
                return True
    else:
        return False


# checks if char is in jail, prints a msg in log and warns in discord
def escape_jail(charFunction=""):
    currentX = GetX(char)
    currentY = GetY(char)

    if (currentX >= JAIL_X_TOP_LEFT) and (currentX <= JAIL_X_BOTTOM_RIGHT):
        if (currentY >= JAIL_Y_TOP_LEFT) and (currentY <= JAIL_Y_BOTTOM_RIGHT):
            UOSay("I have been warned")
            if FindType(GATE_TYPE, Ground()):
                escape_gate = FindItem()
                UseObject(escape_gate)
                wait_gump_and_press_btn(GATE_GUMP, GATE_CONFIRM_BTN)
    else:
        return False


#############################################################################
# NPC UTILS
#############################################################################


# search for an array of possible npcs
def find_npc_types(types):
    npc = ""
    for index, type in enumerate(types):
        if npc:
            break
        npc = find_npc_type(types[index])


    if npc:
        return npc
    else:
        return False

def find_npc_type(type):
    npc = ""
    npc_found = False
    start_time = datetime.now()
    while not npc_found:
        print("Searching for NPC %s" % (type))
        SetFindDistance(25)

        found_npcs = FindTypesArrayEx(NPC_TYPES, [0xFFFF], [Ground()], False)
        if found_npcs:
            npcs_found = GetFindedList()


        if len(npcs_found) > 0:
            for found in npcs_found:
                if npc_found:
                    break

                vendor_name = GetAltName(found)
                wait_lag(10)
                is_npc_vendor = vendor_name.find(type) != -1

                if is_npc_vendor:
                    print("NPC %s found. Name: %s" % (type, vendor_name))
                    npc = found
                    npc_found = True # break the loop
                    return npc

            if checkTimeThreshold(start_time, 5000):
                print("Timeout waiting to find vendor %s. Breaking..." % (type))
                break
        else:
            print("Couldnt find any NPCs around...")


    if npc:
        return npc
    else:
        return False


def is_char_at_vendor(vendor_type):
    SetFindDistance(25)

    if FindTypesArrayEx(NPC_TYPES, [0xFFFF], [Ground()], False):
        npcs_found = GetFindedList()
        if len(npcs_found) > 0:
            for found in npcs_found:
                start_time = datetime.now()
                vendor_name = GetAltName(found)
                check_and_handle_world_save()
                wait_lag(1)
                is_vendor = vendor_name.find(vendor_type) != -1

                if is_vendor:
                    npc = found
                    return True

                check_and_handle_world_save()

                if checkTimeThreshold(start_time, 6000):
                    print("Timeout waiting checking vendor name. Breaking...")
                    break
            return True
        else:
            return False
    return False


def get_npc_distance(npc):
    return GetDistance(npc)

# =============================================================================
# DROP ITEM ABSTRACIONS
# USUALLY YOU DONT CALL THESE. YOU USE HIGHER LEVEL ABSTRACTIONS FROM THE HELPERS
# =============================================================================

def drop_item(item_id, amount, x, y, z):
    Drop(item_id, amount, x, y, z)

def drop_item_north_of_char(item_id, amount, container):
    drop_item(item_id, amount, GetX(Self()), GetY(Self()) + 1, GetZ(Self()))
    wait_lag(10)

def drop_item_south_of_char(item_id, amount, container):
    drop_item(item_id, amount, GetX(Self()), GetY(Self()) - 1, GetZ(Self()))
    wait_lag(10)

def drop_item_east_of_char(item_id, amount, container):
    drop_item(item_id, amount, GetX(Self()) + 1, GetY(Self()), GetZ(Self()))
    wait_lag(10)

def drop_item_west_of_char(item_id, amount, container):
    drop_item(item_id, amount, GetX(Self()) - 1, GetY(Self()), GetZ(Self()))
    wait_lag(10)

def drop_item_to_random_direction(item_id, amount, container):

    item_type = GetType(item_id)
    item_color = GetColor(item_id)
    item_name = str(GetAltName(item_id))
    start_time_1 = datetime.now()
    while FindTypeEx(item_type, item_color, container, False):
        item_amount = FindFullQuantity()
        original_amount = item_amount
        start_time_2 = datetime.now()
        print("Trying to drop item of type %s West of char..." % (item_name))
        drop_item_west_of_char(item_id, amount, container)
        wait_lag(10)
        if FindTypeEx(item_type, item_color, container, False):
            if FindFullQuantity() == original_amount:
                print("Trying to drop item of type %s South of char..." % (item_name))
                drop_item_south_of_char(item_id, amount, container)
                wait_lag(10)
        if FindTypeEx(item_type, item_color, container, False):
            if FindFullQuantity() == original_amount:
                print("Trying to drop item of type %s east of char..." % (item_name))
                drop_item_east_of_char(item_id, amount, container)
                wait_lag(200)
        if FindTypeEx(item_type, item_color, container, False):
            if FindFullQuantity() == original_amount:
                print("Trying to drop item of type %s North of char..." % (item_name))
                drop_item_north_of_char(item_id, amount, container)
                wait_lag(200)

        if item_amount == original_amount:
            return False
        else:
            return True

        if checkTimeThreshold(start_time_1, 6000):
            print("Timeout while trying to drop item. Breaking...")
    return False

# =============================================
# DROP ITEMS BY TYPE
# THESE WILL CALL ABOVE FUNCTIONS WITH TYPE

def drop_item_from_bank(item_id, amount_to_drop):
    return drop_item_to_random_direction(item_id, amount_to_drop, ObjAtLayer(BankLayer()))

# drop X items from packa (pass amount)
def drop_item_type_from_bank(item_type, amount_to_drop):
    if FindType(item_type, bank):
        return drop_item_to_random_direction(FindItem(), amount_to_drop, ObjAtLayer(BankLayer()))

def drop_item_from_backpack(item_id, amount_to_drop):
    return drop_item_to_random_direction(item_id, amount_to_drop, backpack)

# drop X items from packa (pass amount)
def drop_item_type_from_backpack(item_type, amount_to_drop):
    if FindType(item_type, backpack):
        return drop_item_to_random_direction(FindItem(), amount_to_drop, backpack)


def find_commodity_deed_box_on_ground():
    box = ""
    box_found = False
    start_time = datetime.now()
    while not box_found:
        print("Searching for Commodity Deed Boxes on the ground")

        SetFindDistance(4)
        SetFindVertical(10)
        if FindTypeEx(COMMODITY_DEED_BOX_SOUTH, COMMODITY_DEED_BOX_COLOR, Ground(), False) or FindTypeEx(COMMODITY_DEED_BOX_EAST, COMMODITY_DEED_BOX_COLOR, Ground(), False):
            box = FindItem()
            box_found = True
            break

        if checkTimeThreshold(start_time, 6000):
            print("Timeout searching for commodity deed box on the ground. Breaking...")
            break

    if box:
        return box
    else:
        return False

def find_forge_on_ground():
    forge = ""
    forge_found = False
    start_time = datetime.now()
    while not forge_found:
        print("Searching for Commodity Deed Boxes on the ground")

        SetFindDistance(4)
        SetFindVertical(10)
        if FindTypeEx(SMALL_FORGE_TYPE, SMALL_FORGE_COLOR, Ground(), False) or FindTypeEx(SMALL_FORGE_TYPE, Ground(), False):
            forge = FindItem()
            forge_found = True
            break

        if checkTimeThreshold(start_time, 6000):
            print("Timeout searching for commodity deed box on the ground. Breaking...")
            break

    if forge:
        return forge
    else:
        return False

# ===========================================================
# LUMBER SCRIPT SPECIFIC HELPERS
# drop X items from packa (pass amount)
def drop_common_logs_from_backpack(amount_to_drop):
    if FindTypeEx(LOG_TYPE, 0, backpack, False):
        return drop_item_to_random_direction(FindItem(), amount_to_drop, backpack)

def drop_logs_from_backpack(amount_to_drop):
    if FindTypeEx(LOG_TYPE, -1, backpack, False):
        return drop_item_to_random_direction(FindItem(), amount_to_drop, backpack)

def drop_colored_logs_from_backpack(amount_to_drop):
    if FindTypeEx(LOG_TYPE, -1, backpack, False):
        item_color = GetColor(FindItem())
        if item_color != 0:
            return drop_item_to_random_direction(FindItem(), amount_to_drop, backpack)

def drop_common_boards_from_backpack(amount_to_drop):
    if FindTypeEx(BOARD_TYPE, 0, backpack, False):
        return drop_item_to_random_direction(FindItem(), amount_to_drop, backpack)

def drop_boards_from_backpack(amount_to_drop):
    if FindTypeEx(BOARD_TYPE, -1, backpack, False):
        return drop_item_to_random_direction(FindItem(), amount_to_drop, backpack)

def drop_colored_boards_from_backpack(amount_to_drop):
    if FindTypeEx(BOARD_TYPE, -1, backpack, False):
        item_color = GetColor(FindItem())
        if item_color != 0:
            return drop_item_to_random_direction(FindItem(), amount_to_drop, backpack)

# ===========================================================
# MINING SCRIPT SPECIFIC HELPERS
# drop X items from packa (pass amount)
def drop_ores_from_backpack(amount_to_drop):
    if FindType(ORE_TYPE, backpack):
        return drop_item_to_random_direction(FindItem(), amount_to_drop, backpack)