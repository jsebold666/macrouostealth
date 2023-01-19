import os
import io
import re
import time
import math
from math import floor
import json
from datetime import datetime, timedelta
from pprint import pprint
import copy

from modules.sounds import *
from modules.types import *
from modules.gumps import *
import modules.gumps as gumps

from modules.journal import in_journal
import modules.journal as journal

from modules.webhooks import *

try:
    from py_stealth import *
    import py_stealth as stealth
    from modules.types import CHECK, CHECK_COLOR
    import modules.types as types

    from modules.skills import is_shade, is_samurai, is_mage, is_healer
    import modules.skills as skills
except Exception as err:
    print("Error importing py_stealth: %s" % (err))
    exit()


try:
    from modules.spell_utils import *

    # from spell_utils import (
    #     is_char_a_mage,
    #     is_char_a_necro_mage,
    #     is_char_a_paladin,
    # )
except Exception as err:
    print("Error importing spell_utils: %s" % (err))
    exit()

# import spell_utils


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

# try:
#     from outlands_utils import (
#         OUTLANDS_AFK_GUMP_IDS,
#         OUTLANDS_AFK_GUMP_SECOND_PART,
#         OUTLANDS_AFK_GUMP_OK_BTN,
#     )
# except Exception as err:
#     print("Error importing outlands_utils: %s" % (err))
#     pass
# =======================================================================
# CONFIGURATION
# =======================================================================

PLAY_SOUNDS = True

# =======================================================================
# CONFIGURATION
# =======================================================================

DEBUG = True  # Enable Debug Globally
SUPER_DEBUG = True  # Enable Super Debug Globally


# =======================================================================
# DELAYS AND TIMERS
# =======================================================================

WAIT_TIME = 500  # Default Wait Time
TRAVEL_SPELL_WAIT_TIME = 2000
WAIT_LAG_TIME = 10000  # Default Wait Lag Time
STUCK_TIME = 10000  # Default Stuck Time
WORLD_SAVE_AVG_TIME = 10000


# =======================================================================
# VARIABLES
# =======================================================================

# usefull aliases
# variable to easy access stealth commonly used methods
char = Self()
CHAR = Self()
char_name = CharName()
CHAR_NAME = CharName()
backpack = Backpack()
BACKPACK = Backpack()
bank = ObjAtLayer(BankLayer())
BANK = ObjAtLayer(BankLayer())
ground = Ground()
GROUND = Ground()
dead = Dead()
DEAD = Dead()
char_max_hp = GetMaxHP(char)
char_max_mana = GetMaxMana(char)
char_max_stam = GetMaxStam(char)

# def char_hp():
#     return GetHP(char)
# def char_max_hp():
#     return GetMaxHP(char)
# def char_mana():
#     return GetMana(char)
# def char_max_mana():
#     return GetMaxMana(char)
# def char_stam():
#     return GetStam(char)
# def char_max_stam():
#     return GetMaxStam(char)

# IN_JAIL = False
amount_of_gold_in_bank = 0
amount_of_checks_in_bank = 0


def set_travel_method():
    # print("Setting travel method")
    while (
        is_number_repl_isdigit(GetSkillValue("Magery")) is False
        or is_number_repl_isdigit(GetSkillValue("Chivalry")) is False
    ):
        Wait(50)
    if GetSkillValue("Magery") >= 45:
        # debug("Setting travel spell to Recall")
        return "recall"
    elif GetSkillValue("Chivalry") >= 30:
        # debug("Setting travel spell to Sacred Journey")
        return "chiva"
    else:
        # debug(
        #     "common_utils.set_travel_method: Char doenst have enough skill to travel."
        # )
        return False


# Aux function just to replace "." to check if a var is a number (float or integer).
# Ref https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
def is_number_repl_isdigit(s):
    """ Returns True is string is a number. """
    return str(s).replace(".", "", 1).isdigit()


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
            if check_timer(start_time, WORLD_SAVE_AVG_TIME):
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
    # SetAlarm()
    AddToSystemJournal("Someone is attacking you.")
    UOSay("Guards")
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


def is_char_low_on_tithing_points(minimum=100):
    current_tithing_points = get_current_tithing_points()
    if current_tithing_points < minimum:
        print("Char is low on tithing points.")
        return True
    else:
        return False


def get_current_tithing_points():
    current_tithing_points = GetExtInfo()["Tithing_points"]
    return int(current_tithing_points)

def gotToAnk(ankh):
    if 0 < GetDistance(ankh) > 2:
        debug("Ank away for 2 titles")
        if NewMoveXY(GetX(ankh), GetY(ankh), True, 1, True):
            debug("Got to ank")
            Wait(CheckLag(3000))
        else:
            debug("Could not move closer to ank! Abort UNload!")
            return False
    else:
        debug("Char is already close to ank")

def gotToHouse3():
    SetMoveBetweenTwoCorners(0)
    SetMoveCheckStamina(0)
    SetMoveThroughCorner(0)
    SetMoveThroughNPC(0)
    SetMoveOpenDoor(True)
    debug("Init go square house")
    x = 1247
    y = 1204
    while x != GetX(Self()) or y != GetY(Self()):
        Wait(1000)
        NewMoveXY(x, y, False, 0, True)
        Wait(500)

def gotToHouse2():
    SetMoveBetweenTwoCorners(0)
    SetMoveCheckStamina(0)
    SetMoveThroughCorner(0)
    SetMoveThroughNPC(0)
    SetMoveOpenDoor(True)
    debug("Init go square house")
    x = 1249
    y = 1204
    while x != GetX(Self()) or y != GetY(Self()):
        Wait(1000)
        NewMoveXY(x, y, False, 0, True)
        Wait(500)

def gotToHouse():
    SetMoveBetweenTwoCorners(0)
    SetMoveCheckStamina(0)
    SetMoveThroughCorner(0)
    SetMoveThroughNPC(0)
    SetMoveOpenDoor(True)
    debug("Init go square house")
    x = 1249
    y = 1214
    while x != GetX(Self()) or y != GetY(Self()):
        OpenDoor()
        Wait(1000)
        NewMoveXY(x, y, False, 0, True)
        Wait(500)

def tithe_gold_to_shrine():
    # find an ank to donate money
    SetFindDistance(10)
    SetFindVertical(10)
    debug("entrou tithe")
    for x in ANKH_TYPES:
        debug("procurando %d" % (x))
        if FindType(x, Ground()):
            debug("achou achou saporra")
    if FindTypesArrayEx(ANKH_TYPES, [0xFFFF], [Ground()], False):
        ankh = FindItem()
        debug("Achou %s" % (get_item_name(ankh)))
        gotToAnk(ankh)
        # request tithe gold gump from ankh
        debug("setando context menu na ankh")
        SetContextMenuHook(ankh, TITHE_GOLD_POSITION)
        WaitGump(1000)
        debug("requested context menu")
        RequestContextMenu(ankh)

        # wait for the ankh donation gump to appear
        wait_gump_without_using_object(TITHE_GOLD_GUMP_ID)
        while not waitgumpid(TITHE_GOLD_GUMP_ID, ankh):
            debug("waiting for gump to appear")
            Wait(100)

        # click on tithe all gold
        debug("tithe gold gump abriu")
        wait_gump_and_press_btn(TITHE_GOLD_GUMP_ID, TITHE_ALL_GOLD_BTN)
        wait_gump_without_using_object(TITHE_GOLD_GUMP_ID)
        while not waitgumpid(TITHE_GOLD_GUMP_ID, ankh):
            debug("waiting for gump to appear")
            Wait(100)

        debug("tithe gold clickando OK DOAR")
        wait_gump_and_press_btn(TITHE_GOLD_GUMP_ID, TITHE_ALL_GOLD_OK_BTN)

        # confirm on journal donation succeeded
        tithe_gold_success_journal_msg = "devotion"
        wait_lag(30)
        if InJournal(tithe_gold_success_journal_msg) > -1:
            ClearJournal()
            debug("Donated gold to shrine!")
            return True
        else:
            return False
    else:
        debug("Não achou ankh para doar dinheiro")


# =======================================================================
# Dress Utils
# =======================================================================

# Store graphic of common leather suit to search in backpack for LRC pieces

EQUIPMENT_SET_TYPES = {
    "head": {
        "layer": HatLayer(),
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
            "floppy_hat": 0x1713,
            "ninja_hood": 0x278F,
            "glasses": 0x2FB8,
            "Jingasa": 0x2776,
            "pirate_hat": 0x171B,
        },
    },
    "neck": {
        "layer": NeckLayer(),
        "items": {
            "mempo": 0x277A,
            "platemail_gorget": 0x1413,  # jackals
            "leather_gorget": 0x13C7,
        },
    },
    "torso": {
        "layer": TorsoLayer(),
        "items": {
            "leather_tunic": 0x13CC,
            "leather_tunic2": 0x13DB,  # armor of fortune
            "ninja_jacket": 0x2793,
            "samurai_do": 0x27C6,
            "ancient_samurai_do": 0x277D,
            "heart_of_the_lion": 0x1415,
            "violet_courage": 0x1C04,
        },
    },
    "torsoH": {
        "layer": TorsoHLayer(),
        "items": {"sash": 0x1541},
    },
    "shirt": {
        "layer": ShirtLayer(),
        "items": {},
    },
    "legs": {
        "layer": LegsLayer(),
        "items": {},
    },
    "pants": {
        "layer": PantsLayer(),
        "items": {
            "leather_leggings": 0x13CB,
            "leather_ninja_pants": 0x2791,
            "leather_skirt": 0x1C08,
            "fey_leggings": 0x13BE,
            "chainmail_leggings": 0x13BE,  # banes
        },
    },
    "sleeves": {
        "layer": ArmsLayer(),
        "items": {
            "leather_sleeves": 0x13CD,
            "hiro_sode": 0x277E,
        },
    },
    "gloves": {
        "layer": GlovesLayer(),
        "items": {
            "leather_gloves": 0x13C6,
            "ringmail_gloves": 0x13EB,
            "platemail_gloves": 0x2792,  # stormgrip
        },
    },
    "left_hand": {
        "layer": LhandLayer(),
        "items": {
            "composite_bow": 0x26C2,
            "quarter_staff": 0x0E89,
            "black_staff": 0x0DF0,
            "metal_kite_shield": 0x1B74,
            "order_shield": 0x1BC4,
            "chaos_shield": 0x1BC3,
            "yumi": 0x27A5,
            "bow": 0x13B2,
        },
    },
    "right_hand": {
        "layer": RhandLayer(),
        "items": {
            "twinkling_scimitar": 0x2D33,
            "kryss": 0x1401,
            "boomstick": 0x2D25,
            "spellbook": 0xEFA,
        },
    },
    "waist_hand": {
        "layer": WaistLayer(),
        "items": {"apron": 0x153B},  # crimson cinture
    },
    "ring": {
        "layer": RingLayer(),
        "items": {"ring_gold": 0x108A, "ring_dark": 0x1F09},
    },
    "bracelet": {
        "layer": BraceLayer(),
        "items": {"bracelet_gold": 0x1086, "bracelet_dark": 0x1F06},
    },
    "shoes": {
        "layer": ShoesLayer(),
        "items": {"fur_boots": 0x2307, "botas_int": 0x170B},  # botas de inteligencia
    },
    "robe": {
        "layer": RobeLayer(),
        "items": {"robe": 0x1F03, "robe2": 0x1F04, "dress": 0x1F01, "shroud": 0x2684},
    },
    "cloak": {
        "layer": CloakLayer(),
        "items": {
            "cloak": 0x1515,
            "quiver_of_infinity": 0x2B02,  # quiver of infinity
            "quiver_of_blight": 0x2FB7,
        },
    },
    "ears": {
        "layer": EarLayer(),
        "items": {
            "earrings": 0x1087,  # brincos
        },
    },
    "talisman": {
        "layer": TalismanLayer(),
        "items": {
            "primer_on_arms": 0x2F59,
            "totem_of_the_void": 0x2F5B,
            "bloodwood_spirit": 0x2F5A,
        },
    },
    "eggs": {"layer": EggsLayer(), "items": {}},
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
    "robe": RobeLayer(),
    "cloak": CloakLayer(),
    "earrings": EarLayer(),
    "talisman": TalismanLayer(),
    "eggs": EggsLayer(),
}

CHAR_SET = {
    "head": {"item": 0, "layer": HatLayer()},
    "neck": {"item": 0, "layer": NeckLayer()},
    "torso": {"item": 0, "layer": TorsoLayer()},
    "torsoH": {"item": 0, "layer": TorsoHLayer()},
    "shirt": {"item": 0, "layer": ShirtLayer()},
    "legs": {"item": 0, "layer": LegsLayer()},
    "pants": {"item": 0, "layer": PantsLayer()},
    "sleeves": {"item": 0, "layer": ArmsLayer()},
    "gloves": {"item": 0, "layer": GlovesLayer()},
    "left_hand": {"item": 0, "layer": LhandLayer()},
    "right_hand": {"item": 0, "layer": RhandLayer()},
    "waist_hand": {"item": 0, "layer": WaistLayer()},
    "ring": {"item": 0, "layer": RingLayer()},
    "bracelet": {"item": 0, "layer": BraceLayer()},
    "shoes": {"item": 0, "layer": ShoesLayer()},
    "robe": {"item": 0, "layer": RobeLayer()},
    "cloak": {"item": 0, "layer": CloakLayer()},
    "ears": {"item": 0, "layer": EarLayer()},
    "talisman": {"item": 0, "layer": TalismanLayer()},
    "eggs": {"item": 0, "layer": EggsLayer()},
}

CHAR_LRC_SET = {
    "head": {"item": 0, "layer": HatLayer()},
    "neck": {"item": 0, "layer": NeckLayer()},
    "torso": {"item": 0, "layer": TorsoLayer()},
    "torsoH": {"item": 0, "layer": TorsoHLayer()},
    "shirt": {"item": 0, "layer": ShirtLayer()},
    "legs": {"item": 0, "layer": LegsLayer()},
    "pants": {"item": 0, "layer": PantsLayer()},
    "sleeves": {"item": 0, "layer": ArmsLayer()},
    "gloves": {"item": 0, "layer": GlovesLayer()},
    "left_hand": {"item": 0, "layer": LhandLayer()},
    "right_hand": {"item": 0, "layer": RhandLayer()},
    "waist_hand": {"item": 0, "layer": WaistLayer()},
    "ring": {"item": 0, "layer": RingLayer()},
    "bracelet": {"item": 0, "layer": BraceLayer()},
    "shoes": {"item": 0, "layer": ShoesLayer()},
    "robe": {"item": 0, "layer": RobeLayer()},
    "cloak": {"item": 0, "layer": CloakLayer()},
    "ears": {"item": 0, "layer": EarLayer()},
    "talisman": {"item": 0, "layer": TalismanLayer()},
    "eggs": {"item": 0, "layer": EggsLayer()},
}


# remover esta funcao depois para ficar soh com in_range, iguao ao UOS
def is_in_range(npc, distance):
    if GetDistance(npc) <= distance:
        return True
    else:
        return False


def in_range(npc, distance):
    npc_distance = GetDistance(npc)
    if 0 <= npc_distance <= distance:
        return True
    else:
        return False


def is_char_almost_dying():
    if GetHP(char) < GetMaxHP(char) * 0.4:
        return True
    else:
        return False


def is_weapon_equiped():
    weapon = 0

    # has to check rhand first, cause if char wears weapon and shield both layers will be eqiuped
    # and it will then assign the right hand objtm, and then the left hand as well, which is the shield
    if ObjAtLayer(RhandLayer()) > 0:
        weapon = ObjAtLayer(RhandLayer())
    elif ObjAtLayer(LhandLayer()) > 0:
        weapon = ObjAtLayer(LhandLayer())

    if weapon:
        if GetType(weapon) in WEAPON_TYPES:
            return True
    return False


def is_shield_equiped():
    shield_in_hand = ObjAtLayer(LhandLayer())

    if shield_in_hand > 0:
        if (GetType(shield_in_hand)) in SHIELD_TYPES:
            return True
    return False


def equip_weapon(weapon):
    if not weapon:
        debug("The weapon is not defined, so cant equip")
        return False

    if ObjAtLayer(LhandLayer()) == weapon or ObjAtLayer(RhandLayer()) == weapon:
        debug("The weapon is already equiped")
        return True

    if has_property(weapon, "Two-handed Weapon"):
        layer = LhandLayer()
    else:
        layer = RhandLayer()

    if ObjAtLayer(RhandLayer()) > 0:
        UnEquip(RhandLayer())
        wait_lag(600)
    if ObjAtLayer(LhandLayer()) > 0:
        if has_property(ObjAtLayer(LhandLayer()), "two-handed"):
            UnEquip(LhandLayer())
            wait_lag(600)

    if Equip(layer, weapon):
        wait_lag(600)
        debug("%s equiped" % (get_item_name(weapon)))
        return True

    return False


def equip_shield(shield):
    layer = LhandLayer()
    if not shield:
        debug("The shield is not defined, so cant equip")
        return False

        cast_remove_curse()
    if ObjAtLayer(LhandLayer()) == shield:
        # debug("The shield is already equiped")
        return True

    if ObjAtLayer(LhandLayer()) > 0:
        UnEquip(layer)
        wait_lag(600)

    if Equip(layer, shield):
        wait_lag(600)
        debug("%s equiped" % (get_item_name(shield)))

    return True


def is_set_equiped():
    equipped_layers = 0
    for layer_name in CHAR_WEARABLE_LAYERS:
        layer = CHAR_WEARABLE_LAYERS.get(layer_name)
        object_at_layer = ObjAtLayer(layer)
        if object_at_layer != 0:
            equipped_layers += 1

    # if number of layers verified match total number of layers, return true
    # the ideal would be the check to match the number of actual wearable_layers, but most chars dont use all layers, like shoes and ears, so 7 covers all basic set layers (tunic, legs, gorget, etc..)
    # print("equiped layers %s" % (equipped_layers))
    if equipped_layers >= 9:
        return True
    else:
        debug("Char only has %d equiped layers" % (equipped_layers))
        return False


def is_equipment_damaged(limit=4):
    # superDebug("Checking Eqp Durability")
    for layer_name in CHAR_WEARABLE_LAYERS:
        layer = CHAR_WEARABLE_LAYERS.get(layer_name)
        eqp = ObjAtLayer(layer)
        tooltip = GetTooltip(eqp)
        regexSearch = re.search("durability\s+(\d+).*", tooltip)
        if regexSearch is not None:
            if int(regexSearch.group(1)) <= limit:
                return eqp
    return False


def is_equipment_damaged2(item, limit1=0, limit2=255):
    tooltip = GetTooltip(item)
    regexSearch = re.search("durability\s+(\d+).*", tooltip)
    if regexSearch is not None:
        durability = str(regexSearch.group(0)).replace(" / ", "/").split(" ")[1]
        first = durability.split("/")[0]
        second = durability.split("/")[1]
        if int(first) == limit1 and int(second) <= limit2:
            debug("Found equipment with low durability!!! Eqp:" + tooltip)
            return item
    return False


def undress_char_set():
    print("Un-equiping char set")
    for layer in CHAR_WEARABLE_LAYERS:
        unequip(CHAR_WEARABLE_LAYERS.get(layer))
    return True


def unequip(layer):
    start_time = datetime.now()
    while ObjAtLayer(layer) > 0:
        if UnEquip(layer):
            print("%s undressed" % (layer))
            wait_lag(100)
        if check_timer(start_time, 5000):
            print("Timeout trying to unequip item in %s. Breaking..." % (layer))
            break


def equip_item(item, layer):
    start_time = datetime.now()
    while ObjAtLayer(layer) <= 0:
        Equip(layer, item)
        wait_lag(1)
        if check_timer(start_time, 5000):
            print("Timeout trying to equip item in %s. Breaking..." % (layer))
            return False
    return True


# ==============================================================
# MAIN CHAR SET UTILS
# ==============================================================
def save_char_set():
    print("Saving char set...")
    for set_slot in CHAR_SET:
        layer = EQUIPMENT_SET_TYPES[set_slot].get("layer")

        # if piece is saved and equipped
        if CHAR_SET[set_slot].get("item") != 0 and ObjAtLayer(layer) > 0:
            # if saved piece is different than the current one, save current piece
            if CHAR_SET[set_slot].get("item") != ObjAtLayer(layer):
                print(
                    "Equipped piece is different than saved one. Saving equipped piece for %s"
                    % (layer)
                )
                CHAR_SET[set_slot]["item"] = ObjAtLayer(layer)
            # if piece is already saved and equipped, theres nothing to be done
            # else:
            # print("Piece already saved for %s layer" % (layer))

        # if piece is not saved but is equipped, save it
        elif CHAR_SET[set_slot].get("item") == 0 and ObjAtLayer(layer) > 0:
            # print("Piece already dressed but not saved. Saving it")
            CHAR_SET[set_slot]["item"] = ObjAtLayer(layer)

    print("Char set saved!")
    return True


def dress_char_set(dress_set=CHAR_SET):
    print("Dressing main char set")
    for set_slot in dress_set:
        layer = EQUIPMENT_SET_TYPES[set_slot].get("layer")
        # layer = EQUIPMENT_SET_TYPES[set_slot]["layer"]
        saved_item = dress_set[set_slot].get("item")

        # if saved piece is equiped, were done for this layer
        if (
            set_slot != "left_hand" and set_slot != "right_hand"
        ):  # dress weapons for last
            if ObjAtLayer(layer) > 0 and ObjAtLayer(layer) == saved_item:
                print(
                    "%s is already equiped on %s"
                    % (get_item_name(ObjAtLayer(layer)), set_slot)
                )

            # if piece is saved but not equipped, equip it
            elif saved_item != 0:
                print("Equipping saved item in %s " % (set_slot))
                if ObjAtLayer(layer) > 0:
                    unequip(layer)
                equip_item(saved_item, layer)
    print("Equipping Weapon and/or shield")
    # Re-equiping weapon/shield
    if ObjAtLayer(EQUIPMENT_SET_TYPES["left_hand"].get("layer")) > 0:
        unequip(EQUIPMENT_SET_TYPES["left_hand"].get("layer"))
    if ObjAtLayer(EQUIPMENT_SET_TYPES["right_hand"].get("layer")) > 0:
        unequip(EQUIPMENT_SET_TYPES["right_hand"].get("layer"))

    if dress_set["left_hand"].get("item"):
        equip_item(
            dress_set["left_hand"].get("item"),
            EQUIPMENT_SET_TYPES["left_hand"].get("layer"),
        )

    if dress_set["right_hand"].get("item"):
        equip_item(
            dress_set["right_hand"].get("item"),
            EQUIPMENT_SET_TYPES["right_hand"].get("layer"),
        )

    find_save_and_equip_missing_set_pieces()


def save_and_dress_set():
    dress_char_set()
    save_char_set()


def find_char_shield():
    shield = 0
    if ObjAtLayer(LhandLayer()) > 0:
        shield = ObjAtLayer(LhandLayer())
    else:
        for shield_type in SHIELD_TYPES:
            if FindType(shield_type, Backpack()):
                shield = FindItem()
                break

    if shield:
        return shield
    debug("NAO ACHOPU SHIELD")
    return None


def find_save_and_equip_missing_set_pieces():
    for set_slot in CHAR_SET:
        layer_dressed = False
        # get the layers array for current set slot
        layer = EQUIPMENT_SET_TYPES[set_slot].get("layer")
        layer_name = EQUIPMENT_SET_TYPES[set_slot]["layer"]
        if ObjAtLayer(layer) <= 0:
            for item in EQUIPMENT_SET_TYPES[set_slot].get("items"):
                item_name = EQUIPMENT_SET_TYPES[set_slot]["items"][item]
                graphic = EQUIPMENT_SET_TYPES[set_slot]["items"].get(item)
                if FindType(graphic, Backpack()):
                    items_found = GetFindedList()
                    for found in items_found:
                        # add case to not dress death robes
                        if (
                            GetType(found) == ROBE_TYPE
                            and GetColor(found) == DEATH_ROBE_COLOR
                        ):
                            print("Found a robe but its a Death Robe. Ignoring...")
                            break
                        print(
                            "Found %s in backpack and equiping piece for %s."
                            % (get_item_name(found), set_slot)
                        )
                        item = found
                        if ObjAtLayer(layer) > 0:
                            unequip(layer)
                        equip_item(item, layer)
                        CHAR_SET[set_slot]["item"] = item
                        if ObjAtLayer(layer) == item:
                            layer_dressed = True
                        break  # break no final pra só vestir a primeira peça
                if (
                    layer_dressed is True
                ):  # para não tentar equipar de novo caso já tenha equipado
                    break


# ###################################################################
# LRC SET DRESS
# ###################################################################


def find_lrc_items_in_backpack_and_dress():  # ia colocar um 'maybe' só pra sacanear com o tau mas desisti, kkkkk.
    # undress_char_set()
    if FindType(-1, Backpack()):
        items_found = GetFindedList()
        undress_char_set()
        for item in items_found:
            if has_property(item, "lower reagent cost"):
                print("Found %s with LRC." % (get_item_name(item)))
                # layer = GetLayer(item)
                # print("layer %d" % (layer))
                # current_item_at_layer = ObjAtLayer(layer)
                # if current_item_at_layer > 0:
                #     print(
                #         "Undressing %s to dress %s with LRC"
                #         % (get_item_name(current_item_at_layer, get_item_name(item)))
                #     )
                #     unequip(layer)
                Equip(1, item)
                wait_lag(500)


# =======================================================================
# ITEM UTILITIES
# =======================================================================


# finds item with any color
def count(item_type, container=backpack):
    if FindType(item_type, container):
        return FindItem()
    else:
        return False


# finds item with color 0
def count_common(item_type, container=backpack, recurse=True):
    if FindTypeEx(item_type, 0, container, recurse):
        return FindItem()
    else:
        return False


# finds item with any color != 0
def count_colored(item_type, item_color=0, container=backpack, recurse=True):
    if FindTypeEx(item_type, item_color, container, recurse):
        return FindItem()
    else:
        return False


def count_common_ground(item_type):
    return count_common(item_type, Ground())


def count_colored_ground(item_type, item_color):
    return count_colored(item_type, item_color, Ground())


# =====================================================================
# Quantity and count item utils
# =====================================================================


def get_item_name(item):
    item_details_str = GetTooltip(item)
    item_details_array = item_details_str.split("|")
    return item_details_array[0]
    # for item_name, item_props in enumerate(item_details_array):
    #     item_props_array = item_props.split(",")
    #     for property_str in item_props_array:
    #         prop_array = re.split('(-?\d*\.?\d+)', property_str)
    #         if "lower reagent cost " in prop_array:
    #             lrc_in_item = int(prop_array[1])
    #             lrc_total += lrc_in_item


def get_item_quantity(item_type, container_to_search_in):
    if FindType(item_type, container_to_search_in):
        return FindFullQuantity()
    else:
        return 0


def get_item_quantity(item_type, container_to_search_in):
    if FindType(item_type, container_to_search_in):
        return FindFullQuantity()
    else:
        return 0


def get_common_item_quantity(item_type, container_to_search_in):
    if FindTypeEx(item_type, 0, container_to_search_in, False):
        return FindFullQuantity()
    else:
        return 0


def get_colored_item_quantity(item_type, item_color, container_to_search_in):
    if FindTypeEx(item_type, item_color, container_to_search_in, False):
        return FindFullQuantity()
    else:
        return 0


# Count commonly used items in backpack


def count(
    item_graphic,
    item_color=0xFFFF,
    container_to_search_in=backpack,
    search_subcontainers=True,
):
    if FindTypeEx(
        item_graphic, item_color, container_to_search_in, search_subcontainers
    ):
        return FindFullQuantity()

    return 0


# Count commonly used items in ground


def count_boards_in_ground(bank):
    return CountGround(BOARD_TYPE)


def make_check(amount=1000000):
    amount_of_gold_in_bank = count_colored(
        types.CHECK, types.CHECK_COLOR, ObjAtLayer(BankLayer())
    )
    if amount_of_gold_in_bank > 1100000:
        debug(
            "Char has %d gold in the bank. Making check..." % (amount_of_gold_in_bank)
        )
        initial_amount_of_checks_in_bank = count_checks_in_bank()
        UOSay("check %d" % (amount))
        wait_lag(10)
        checks_in_bank = count_checks_in_bank()
        if checks_in_bank > initial_amount_of_checks_in_bank:
            return True
        else:
            debug("Char has enough money to make a 1kk check, but failed.")
            return False
    return False


def is_char_at_bank():
    UOSay("bank")
    wait_lag(10)
    bank_container = LastContainer()
    # FIXME: this is always returning true even if char is not at bank

    print("teste bank container %s" % (bank_container))
    if bank_container > 0:
        print("found bank?")
        return True
    else:
        print("didnt find")
        return False


def get_current_bank_balance():
    SetContextMenuHook(char, 2)
    WaitGump(1000)
    RequestContextMenu(char)

    wait_lag(50)
    wait_gump_without_using_object(3465474465)

    current_balance = 0

    for gump in range(GetGumpsCount()):
        idd = GetGumpID(gump)
        if idd == 3465474465:

            # gump do insurance menu
            infogump = GetGumpInfo(gump)
            current_balance = infogump["Text"][0][0]
        else:
            break

    # reset the context! important!
    SetContextMenuHook(0, 0)
    wait_lag(1)
    close_gumps()

    return int(current_balance)


def get_number_of_deaths_playable():
    number_of_deaths_playable = 0
    SetContextMenuHook(char, 2)
    WaitGump(1000)
    RequestContextMenu(char)
    wait_lag(1)
    # reset the context! important!
    SetContextMenuHook(0, 0)
    wait_gump_without_using_object(3465474465)

    for gump in range(GetGumpsCount()):
        idd = GetGumpID(gump)
        if idd == 3465474465:
            # gump do insurance menu
            infogump = GetGumpInfo(gump)
            number_of_deaths_playable = int(infogump["Text"][2][0])
        else:
            break

    close_gumps()
    wait_lag(1)
    close_gumps()
    return number_of_deaths_playable


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
HELP_REQUEST_CHOOSE_TOWN_GUMP_ID = 0x1E88CA33
HELP_REQUEST_CHARACTER_STUCK_BTN = 2
HELP_REQUEST_GUMP_ID = 0xB3423A1D


def open_help_request():
    HelpRequest()
    wait_lag(10)


def go_to_britain_via_help_request():
    open_help_request()
    wait_gump_and_press_btn(
        HELP_REQUEST_GUMP_ID, HELP_REQUEST_CHARACTER_STUCK_BTN, 5, 5
    )
    wait_lag(10)
    wait_gump_and_press_btn(HELP_REQUEST_CHOOSE_TOWN_GUMP_ID, 1, 5)
    wait_lag(10)

    close_gumps()

    initial_x = GetX(char)
    initial_y = GetY(char)
    while initial_x == GetX(char) and initial_y == GetY(char):
        debug("Waiting to be teleported to Brit")
        Wait(5000)


def go_to_britain_bank_vendor_mall_moongate():
    NewMoveXY(1534, 1673, True, 0, True)  # middle bridge on the East side of brit

    # cross the bridge into the West side on a straight line
    NewMoveXY(1490, 1673, True, 0, True)

    NewMoveXY(1458, 1676, True, 0, True)
    NewMoveXY(1444, 1681, True, 0, True)
    NewMoveXY(1444, 1695, True, 0, True)
    NewMoveXY(1415, 1688, True, 0, True)  # the VM moongate


def bandage_self():
    if not Dead():
        if skills.is_healer():
            if Poisoned() or GetHP(char) < GetMaxHP(char):
                if not is_buff_active("Healing"):
                    debug("** bandage self **", 0)
                    if FindType(BANDAGE_TYPE, Backpack()):
                        BandageSelf()
                    else:
                        debug("** no bandage **")


# ####################################################################
# SPELL UTILS
# ####################################################################

# SPELLS CASTING TIMES:
CAST_RECOVERY_TIME = 2000
GREATER_HEAL_CAST_TIME = 3000
RECALL_CAST_TIME = 3500
SACRED_JOURNEY_CAST_TIME = 3000
CLOSE_WOUNDS_CAST_TIME = 3000
HOLY_LIGHT_CAST_TIME = 4000
# NECRO SPELLS
VAMPIRIC_EMBRACE_CAST_TIME = 4000


def heal_self_until_max_hp():
    start_time = datetime.now()
    if Dead():
        print("Char cant heal while dead!")
        return False
    while GetHP(char) < GetMaxHP(char):
        print("Char is healing")
        check_mana()

        if Dead():
            print("Char died while healing to max hp")
            return False
        if skills.is_healer():
            bandage_self()
        else:

            if skills.is_samurai():
                cast_confidence()

            if skills.is_mage():
                mage_big_heal()
            elif skills.is_paladin():
                chivheal()

        if check_timer(start_time, 15000):
            print("Timeout while healing (15s). Breaking...")
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


def find_char_corpse(distance_to_search):
    SetFindDistance(distance_to_search)
    lowercased_char_name = char_name.lower()
    if FindType(CORPSE, ground):
        corpses_found = GetFindedList()
        for corpse in corpses_found:
            corpse_tooltip = GetTooltip(corpse).lower()
            # debug("TESTE CORPSE %s" % (corpse_tooltip))
            if corpse_tooltip.find(lowercased_char_name) >= 0:
                return corpse
            else:
                # NOTE: IMPORTANTE ignorar aqui senao o stealth tem que ficar toda hora scaneando 1 milhao de corpos no champ
                Ignore(corpse)
        return None


def click_on_char_corpse():
    if not Dead():
        char_corpse = find_char_corpse(2)
        if char_corpse:
            corpse_tooltip = GetTooltip(char_corpse)
            debug(" ** found char corpse: %s **" % (corpse_tooltip))
            UseObject(char_corpse)
            return True

    return False


def hide_char():
    if not Hidden():
        debug("** hiding **")
        if skills.is_shade():
            UseSkill("Hiding")
            Wait(1000)
        elif skills.is_mage():
            cast("invisibility", char)
            Wait(1000)
        else:
            UseSkill("Hiding")
            # SetWarMode(True)
            # SetWarMode(False)
            Wait(CheckLag(1000))


# =================================================================================
# USEFULL COMMON IN GAME UTILS
# =================================================================================


def wait_lag(wait_time=WAIT_TIME, lag_time=WAIT_LAG_TIME):
    Wait(wait_time)
    CheckLag(lag_time)
    return


def debug(message, message_color=66):
    if DEBUG:
        AddToSystemJournal(message)
        ClientPrintEx(char, message_color, 1, message)


def headmsg(message, message_color=66, object_id=CHAR):
    AddToSystemJournal(message)
    ClientPrintEx(object_id, message_color, 1, message)


def sysmsg(message, message_color=66):
    AddToSystemJournal(message)
    ClientPrintEx(0, message_color, 1, message)


def guildmsg(message, message_color=66):
    UOSay("\ %s" % (message))


def alliancemsg(message, message_color=66):
    UOSay("| %s" % (message))


def check_timer(starttime, time_limit_in_miliseconds):
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
        drop_item_type(itemTypeToDrop, color, dropX, dropY, qtdToDrop)
        wait_lag(100)
        if check_timer(starttime, 5000):
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

        if check_timer(starttime, 4000):
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


# ==========================================================================
# TRAVEL UTILS
# ==========================================================================


def enter_gate():
    # if gate is open, click it to enter
    if FindType(0x0F6C, Ground()):
        UseObject(FindItem())
        wait_gump_and_press_btn(3899019871, 2)


def has_char_location_changed(previous_x_location, previous_y_location):
    if GetX(char) != previous_x_location or GetY(char) != previous_y_location:
        return True
    else:
        return False


def move_char_to_random_direction():
    coord_x, coord_y = GetX(char), GetY(char)
    x, y = coord_x, coord_y
    start_time = datetime.now()
    while Connected() and not Dead() and not has_char_location_changed(x, y):
        for direction in range(1, 8):
            # walk 3 steps
            for i in range(0, 3):
                Step(direction, False)
                # wait_lag(10)
                Wait(CheckLag(3000))

            if has_char_location_changed(x, y):
                print("Moved char 1 tile.")
                return True
        if check_timer(start_time, 8000):
            print("Timeout trying to move char. Breaking..")
            break

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
            wait_gump_and_press_btn(RUNEBOOK_GUMP_ID, usingchiva[rune_number], True)
            wait_lag(SACRED_JOURNEY_CAST_TIME)
        elif travel_method == "recall":
            wait_gump_and_press_btn(RUNEBOOK_GUMP_ID, usingregs[rune_number], True)
            wait_lag(RECALL_CAST_TIME)
        elif travel_method == "gate":
            wait_gump_and_press_btn(RUNEBOOK_GUMP_ID, usinggate[rune_number], True)
            wait_lag(GATE_TRAVEL_CAST_TIME)
            enter_gate_maybe()
        elif travel_method == "charge":
            runebook_gump = wait_gump_and_press_btn(
                RUNEBOOK_GUMP_ID, usingcharges[rune_number], False
            )
            if runebook_gump:
                if "Text" in runebook_gump:
                    # checking if we got charges
                    if int(runebook_gump["Text"][0][0]) > 1:
                        wait_gump_and_press_btn(
                            RUNEBOOK_GUMP_ID, usingcharges[rune_number]
                        )
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
    while Connected() and not Dead() and not has_char_location_changed(char_x, char_y):
        check_mana()
        # starttime = datetime.now()

        if Dead():
            debug("DEAD ON MAIN RECALL! ABORT!")
            return False
        if Weight() >= MaxWeight() + 3:
            debug("OVERWEIGTH ON MAIN RECALL LOOP! ABORT!")
            return False

        if retry >= 1:
            debug("Travel retry -> %d x" % (retry))
        if retry > 10:
            debug("Travel EXITING -> More than %d retries..." % (retry))
            return False

        if travel(travel_method, runebook_name, rune_number):
            if journal.in_journal("location is blocked"):
                ClearJournal()
                # FIXME: have to move char a lot here
                # if char moves just 2 or 3 tiles, GetX and GetY doenst change
                # and script thinks recall failed
                # if runebook_name == "Home":
                debug("Location was blocked. Moving char and trying again")
                move_char_to_random_direction()
                # reset char pos so function doenst think recall succeeded
                char_x, char_y = GetX(char), GetY(char)

                # else:
                #     print(
                #         "Location was blocked. Returning true to to see if it wanst the char itself blocking the location..."
                #     )
                #     return True

        """if check_timer(starttime, 15000):
            print(
                "Char is stuck for more than 15 seconds waiting for location to change. Breaking..."
            )
            break"""  # O starttime tá dentro do while e também tem um limite de retry, não precisa desse break

        # increment retry counter
        retry += 1

    if has_char_location_changed(char_x, char_y):
        debug("Char reached the destination")
        wait_lag(10)
        return True

    else:
        return False


RUNEBOOK = 0x22C5
RUNEBOOK_GUMP_ID = 1431013363


def open_runebook(name):
    if Dead():
        return False

    if FindType(RUNEBOOK, Backpack()):
        runebooks_found = GetFindedList()
        for runebook in runebooks_found:
            splitedToolTip = GetTooltip(runebook).rsplit("|", 1)
            if len(splitedToolTip) > 0:
                if splitedToolTip[1] in (name):
                    start_time = datetime.now()

                    while not Dead() and not gumps.gump_exists(RUNEBOOK_GUMP_ID):
                        gumps.use_object_and_wait_gump(runebook, RUNEBOOK_GUMP_ID)
                        wait_lag(100)
                        if check_timer(start_time, 15000):
                            debug("Timeout while trying to open runebook. Breaking")
                            return False
                    if gumps.gump_exists(RUNEBOOK_GUMP_ID):
                        return True
        debug("Cant find %s runebook" % (name))
    else:
        debug("No runebooks found. Trying to open backpack...")
        wait_lag(5000)
        UseObject(Backpack())
        return False

    return False


# =============================================================================
# DROP ITEM ABSTRACIONS
# USUALLY YOU DONT CALL THESE. YOU USE HIGHER LEVEL ABSTRACTIONS FROM THE HELPERS
# =============================================================================


def drop_item_type(itemType, color, dropX=-1, dropY=-1, qtdToDrop=7):
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


def drop_item(item_id, amount, x, y, z):
    Drop(item_id, amount, x, y, z)


def drop_item_north_of_char(item_id, amount, container):
    drop_item(item_id, amount, GetX(Self()), GetY(Self()) - 1, GetZ(Self()))
    Wait(CheckLag(3000))


def drop_item_south_of_char(item_id, amount, container):
    drop_item(item_id, amount, GetX(Self()), GetY(Self()) + 1, GetZ(Self()))
    Wait(CheckLag(3000))


def drop_item_east_of_char(item_id, amount, container):
    drop_item(item_id, amount, GetX(Self()) + 1, GetY(Self()), GetZ(Self()))
    Wait(CheckLag(3000))


def drop_item_west_of_char(item_id, amount, container):
    drop_item(item_id, amount, GetX(Self()) - 1, GetY(Self()), GetZ(Self()))
    Wait(CheckLag(3000))


def drop_item_to_random_direction(item_id, amount=1, container=backpack):

    if amount == 0:
        debug("Amount of items to drop cant be zero.")

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
        # wait_lag(250)
        Wait(CheckLag(3000))
        if FindTypeEx(item_type, item_color, container, False):
            if FindFullQuantity() == original_amount:
                print("Trying to drop item of type %s South of char..." % (item_name))
                drop_item_south_of_char(item_id, amount, container)
                Wait(CheckLag(3000))
        if FindTypeEx(item_type, item_color, container, False):
            if FindFullQuantity() == original_amount:
                print("Trying to drop item of type %s east of char..." % (item_name))
                drop_item_east_of_char(item_id, amount, container)
                Wait(CheckLag(3000))
        if FindTypeEx(item_type, item_color, container, False):
            if FindFullQuantity() == original_amount:
                print("Trying to drop item of type %s North of char..." % (item_name))
                drop_item_north_of_char(item_id, amount, container)
                Wait(CheckLag(3000))

        if item_amount == original_amount:
            return False
        else:
            return True

        if check_timer(start_time_1, 6000):
            print("Timeout while trying to drop item. Breaking...")
            return False

    return True


# =============================================
# DROP ITEMS BY TYPE
# THESE WILL CALL ABOVE FUNCTIONS WITH TYPE


def drop_item_from_bank(item_id, amount_to_drop):
    return drop_item_to_random_direction(
        item_id, amount_to_drop, ObjAtLayer(BankLayer())
    )


# drop X items from packa (pass amount)
def drop_item_type_from_bank(item_type, amount_to_drop):
    if FindType(item_type, bank):
        return drop_item_to_random_direction(
            FindItem(), amount_to_drop, ObjAtLayer(BankLayer())
        )


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

        SetFindDistance(15)
        SetFindVertical(10)
        if FindTypeEx(
            COMMODITY_DEED_BOX_SOUTH, COMMODITY_DEED_BOX_COLOR, Ground(), False
        ) or FindTypeEx(
            COMMODITY_DEED_BOX_EAST, COMMODITY_DEED_BOX_COLOR, Ground(), False
        ):
            box = FindItem()
            box_found = True
            break

        if check_timer(start_time, 6000):
            print("Timeout searching for commodity deed box on the ground. Breaking...")
            break

    if box:
        return box
    else:
        return False

def findpet(pet):
    if IsObjectExists(pet):
        return True
    return False

def find_pet_on_ground(pet):
    if findpet(pet):
        while GetDistance(pet) > 2:
            debug("Mounting %s" % (GetName(pet)))
            UOSay("All Follow Me")
            Wait(3000)
            debug("Remounting...")
        UseObject(pet)
        Wait(1000)
    else:
        Disconnect()
        Wait(5000)
        Connect()
        
        while not Connected():
            Wait(5000)
        while GetDistance(pet) > 2:
            debug("Mounting %s" % (GetName(pet)))
            UOSay("All Follow Me")
            Wait(3000)
            debug("Remounting...")
        UseObject(pet)
        Wait(1000)


def find_ground(item_type, range=4):
    item = ""
    item_found = False
    start_time = datetime.now()
    while not item_found:
        print(f"Searching for item type {item_type} on ground")

        SetFindDistance(15)
        SetFindVertical(10)
        if FindTypeEx(item_type, 0, Ground(), False) or FindTypeEx(
            item_type, Ground(), False
        ):
            item = FindItem()
            item_found = True
            break

        if check_timer(start_time, 6000):
            print("Timeout searching for commodity deed box on the ground. Breaking...")
            break

    if item:
        return item
    else:
        return False


# ===========================================================
# LUMBER SCRIPT SPECIFIC HELPERS
# drop X items from packa (pass amount)
def drop(item_id, amount_to_drop=1):
    return drop_item_to_random_direction(item_id, amount_to_drop, backpack)


def drop_type(item_graphic, amount_to_drop=1):
    if FindTypeEx(item_graphic, 0, backpack, False):
        return drop_item_to_random_direction(FindItem(), amount_to_drop, backpack)


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
    if FindType(ORE, backpack):
        return drop_item_to_random_direction(FindItem(), amount_to_drop, backpack)


# ===========================================================
# SAMPIRE HELPERS

WEAPON_TYPES = [
    0x0000,  # black staff
    0x0E89,  # quarter staff
    0xE89,  # gnarled staff
    0x2D33,  # twinkling scimitar
    COMPOSITE_BOW,
    YUMI,
]

SHIELD_TYPES = [
    0x1B74,  # metal kite
    0x1BC4,  # order
    0x1BC3,  # chaos
]

CHAR_WEAPONS = {
    "demon_slayer": 0,
    "undead_slayer": 0,
    "dragon_slayer": 0,
}


def find_slayer_weapon(slayer_name):
    debug("Searching for %s slayer..." % (slayer_name))
    weapons_found = []
    if ObjAtLayer(RhandLayer()) > 0:
        weapon = ObjAtLayer(RhandLayer())
        weapons_found.append(weapon)
    elif ObjAtLayer(LhandLayer()) > 0:
        weapon = ObjAtLayer(LhandLayer())
        weapons_found.append(weapon)

    # search the backpack
    for weapon_type in WEAPON_TYPES:
        graphic = weapon_type

        if FindType(graphic, Backpack()):
            weapons_found += GetFindedList()
            # search for property
            if len(weapons_found) > 0:
                for item in weapons_found:
                    if has_property(item, slayer_name):
                        debug(
                            "Found %s %s and saving it"
                            % (slayer_name, get_item_name(item))
                        )
                        CHAR_WEAPONS[slayer_name] = item
                        return item

    return None


def use_curse_weapon_scroll():
    if FindType(CURSE_WEAPON_SCROLL_TYPE, Backpack()):
        UseType(CURSE_WEAPON_SCROLL_TYPE, 0x0000)


# ===========================================================
# CHAR UTILS


def get_possible_destinations(x, y, distance):
    calcX = 0
    calcY = 0
    possible_destinations = []
    for i in range(distance + 1):
        calcX = x + distance
        calcY = y + i
        if [calcX, calcY] not in pointsArr:
            pointsArr.append([calcX, calcY])

        calcX = x - distance
        calcY = y + i
        if [calcX, calcY] not in pointsArr:
            pointsArr.append([calcX, calcY])

        calcX = x + distance
        calcY = y - i
        if [calcX, calcY] not in pointsArr:
            pointsArr.append([calcX, calcY])

        calcX = x - distance
        calcY = y - i
        if [calcX, calcY] not in pointsArr:
            pointsArr.append([calcX, calcY])

        calcX = x + i
        calcY = y + distance
        if [calcX, calcY] not in pointsArr:
            pointsArr.append([calcX, calcY])

        calcX = x + i
        calcY = y - distance
        if [calcX, calcY] not in pointsArr:
            pointsArr.append([calcX, calcY])

        calcX = x - i
        calcY = y + distance
        if [calcX, calcY] not in pointsArr:
            pointsArr.append([calcX, calcY])

        calcX = x - i
        calcY = y - distance
        if [calcX, calcY] not in pointsArr:
            pointsArr.append([calcX, calcY])

    return possible_destinations


def get_oposite_direction(mob):
    mob_direction = CalcDir(GetX(char), GetY(char), GetX(mob), GetY(mob))
    if mob_direction == 0:
        return 4
    elif mob_direction == 1:
        return 5
    elif mob_direction == 2:
        return 6
    elif mob_direction == 3:
        return 7
    elif mob_direction == 4:
        return 0
    elif mob_direction == 5:
        return 1
    elif mob_direction == 6:
        return 2
    elif mob_direction == 7:
        return 3


def keep_distance_from_mob(mob, distance=4):

    oposite_direction = get_oposite_direction(mob)
    mob_x = GetX(mob)
    mob_y = GetY(mob)
    mob_z = GetZ(mob)
    mob_name = GetName(mob)
    if not is_dead(mob) and GetDistance(mob) < distance:

        debug("running from %s" % (mob_name))
        dest_x = GetX(mob) - distance
        dest_y = GetY(mob) - distance
        if IsWorldCellPassable(
            GetX(char), GetY(char), GetZ(char), dest_x, dest_y, WorldNum()
        )[0]:
            # NewMoveXY(dest_x, dest_y, True, 0, True)
            StepQ(CalcDir(GetX(char), GetY(char), dest_x, dest_y), True)
        return True


def in_sight(enemy):
    return is_in_sight(enemy)


def is_in_sight(enemy):
    LOSOptions = None  # LOS type RunUO MUST BE SET!
    LOS = CheckLOS(
        GetX(char),
        GetY(char),
        GetZ(char),
        GetX(enemy),
        GetY(enemy),
        GetZ(enemy),
        1,
        4,
        None,
    )
    # LOS = CheckLOS(GetX(Self()), GetY(Self()), GetZ(Self()), GetX(enemy), GetY(enemy), GetZ(enemy), 1, 2)
    if LOS:
        return True
    elif InJournal("Target cannot be seen") > 0:
        ClearJournal()
        return True
    else:
        return False


def is_out_of_sight(enemy):
    LOSOptions = None  # LOS type RunUO MUST BE SET!
    LOS = CheckLOS(
        GetX(char),
        GetY(char),
        GetZ(char),
        GetX(enemy),
        GetY(enemy),
        GetZ(enemy),
        1,
        4,
        None,
    )
    if not LOS:
        return True
    elif InJournal("Target cannot be seen") > 0:
        ClearJournal()
        return True
    else:
        return False


def identify_tile(x, y, relativeX, relativeY, tileType=[]):
    absRelativeX = abs(relativeX)
    absRelativeY = abs(relativeY)

    processedAbsRelativeX = absRelativeX + 2
    processedAbsRelativeY = absRelativeY + 2

    wantedPositionX = x + relativeX
    wantedPositionY = y + relativeY

    for xx in range(x - processedAbsRelativeX, x + processedAbsRelativeX):
        for yy in range(y - processedAbsRelativeY, y + processedAbsRelativeY):
            r = ReadStaticsXY(xx, yy, WorldNum())
            for result in r:
                # print(r)
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


def has_mobs_nearby(distance=4):
    SetFindDistance(distance)
    SetFindVertical(distance)
    if FindNotoriety(-1, 3) or FindNotoriety(-1, 4):
        return True
    else:
        return False


def find_bag_of_sending_in_backpack():
    if FindType(BAG, Backpack()):
        if get_item_name(FindItem()).find("bag of sending"):
            return FindItem()


def find_bags_of_sending_in_backpack():
    if FindType(BAG, Backpack()):
        if get_item_name(FindItem()).find("bag of sending"):
            return GetFindedList()


def count_bag_of_sending_charges():
    bag_of_sending = find_bag_of_sending_in_backpack()
    if bag_of_sending:
        charges = count_item_property(bag_of_sending, "charges")
        return charges
    else:
        return 0


def send_gold_to_bank(gold_ammount):
    bag_of_sending = find_bag_of_sending_in_backpack()
    if count_bag_of_sending_charges(bag_of_sending) > 1:
        bag_of_sending = find_bag_of_sending_in_backpack()
        if bag_of_sending:
            WaitTargetType(GOLD_TYPE)
            UseObject(bag_of_sending)
            Wait(1000)
            if Gold() < GOLD_LIMIT_TO_SEND_TO_BANK:
                print("Char enviou %d gold para o banco" % (Gold()))
                try:
                    PlayWav(CASH_SOUND)
                except:
                    pass
                return True
    return False


def is_mounted(id):
    if ObjAtLayer(HorseLayer()) > 0:
        return True
    else:
        return False


def is_dead(mob):
    # verifica primeiro se o mob ja nao morreu ou se afastou demais
    if not IsObjectExists(mob) or IsDead(mob) or GetDistance(mob) == -1:
        return True
    else:
        return False


PLAYER_GHOST_TYPES = [
    0x192,
    0x193,
    0x260,
    0x25F,
]


def is_player_ghost(mob):
    # verifica primeiro se o mob ja nao morreu ou se afastou demais
    if GetType(mob) in PLAYER_GHOST_TYPES:
        return True
    else:
        return False


ETHY_HORSE = 0x20DD
ETHY_POLAR_BEAR = 0x20E1
ETHY_LLAMA = 0x20F6
ETHY_REPTALON = 0x2D95
ETHY_SWAMP_DRAGON = 0x2619
ETHY_OSTARD = 0x2135
ETHY_CU_SHIDE = 0x2D96


ETHYS = {
    "polar_bear": 0x20E1,
    "reptalon": 0x2D95,
    "swamp_dragon": 0x2619,
    "ostard": 0x2135,
}


def dismount():
    UseObject(char)
    Wait(CheckLag(3000))


def mount(pet=0, ethy=0):
    # Remount PET
    if is_mounted(char):
        return False

    if (
        IsObjectExists(pet)
        and GetHP(PET) > 0
        and not is_buff_active("Dismount")
        and GetDistance(pet) < 2
    ):
        if GetHP(pet) > 0:
            debug("Mounting %s" % (GetName(pet)))
            UseObject(pet)
            return True
        else:
            debug("! Cant Mount: pet %s is dead !" % (GetName(pet)))
            return False
    else:
        if ethy:
            if FindType(ethy, Backpack()):
                debug("Mounting %s" % (get_item_name(ethy)))
                UseType2(ethy)
                return True
            # else:
            #     debug("! CANT FIND PET OR ETHY !")
        else:
            # debug("Searching for Ethys in backpack...")
            for ethy in ETHYS:
                ethy_type = ETHYS.get(ethy)
                if FindType(ethy_type, Backpack()):
                    debug("Mounting %s" % (get_item_name(ethy)))
                    UseType2(ethy_type)
                    return True
                # else:
                #     debug("! CANT FIND PET OR ETHY !")


"""
NOTORIETY LIST
1 - innocent(blue)
2 - guilded/ally(green)
3 - attackable but not criminal(gray)
4 - criminal(gray)
5 - enemy(orange)
6 - murderer(red)
"""

# port to common_utils of my sampire bot find_enemy function (has to have a different name to not conflict)
def get_enemy(
    distance=15,
    mob_types_to_ignore=[],
    notoriety_list=[3, 4],
    lure_distant_enemies=False,
):
    if not Dead():
        SetFindDistance(distance)
        SetFindVertical(15)
        Ignore(char)

        mobs = []
        for notoriety in notoriety_list:
            if FindNotoriety(-1, notoriety):
                mobs += GetFindedList()

        # se achou algo a gente filtra pra devolver o mais proximo
        if len(mobs) > 0:
            # mobs = filter_enemies_list(
            #     mobs, distance, mob_types_to_ignore, lure_distant_enemies
            # )

            for mob in mobs:
                if is_guildmate(mob):
                    Ignore(mob)
                    break

                if is_dead(mob):
                    Ignore(mob)
                    mobs.remove(mob)
                    break
                if GetType(mob) in mob_types_to_ignore:
                    ClientPrintEx(
                        mob,
                        49,
                        -1,
                        "[IGNORED]",
                    )
                    Ignore(mob)
                    mobs.remove(mob)
                    break

                # se o bixo esta muito longe pra bater, mas ainda dentro de visao, tenta atrair ele pra perto do char atacando
                if (
                    lure_distant_enemies is True
                    and GetHP(char) > (char_max_hp * 0.5)
                    and 2 <= GetDistance(mob)
                    and GetDistance(mob) > 1
                ):
                    Attack(mob)
                    ClientPrintEx(
                        mob, 43, 1, "* LURING * (%d tiles)" % (GetDistance(mob))
                    )
                    break
                # else:
                # ClientPrintEx(
                #     mob, 30, 1, "[scanning: %d tiles]" % (GetDistance(mob))
                # )

            mobs.sort(key=GetDistance)
            return next((mob for mob in mobs if GetDistance(mob) >= 0), None)

        else:
            return None


def get_enemies(distance=4):
    SetFindDistance(distance)
    SetFindVertical(distance)
    current_enemies = []
    if FindNotoriety(-1, 3):
        current_enemies = GetFindedList()
    if FindNotoriety(-1, 4):
        current_enemies += GetFindedList()
    return current_enemies


def get_nearby_mobs(
    distance=20,
    mob_types_to_ignore=[],
    notoriety_list=[3, 4, 5, 6],
    lure_distant_enemies=False,
):
    if not Dead():
        SetFindDistance(distance)
        SetFindVertical(30)
        Ignore(char)

        mobs = []
        for notoriety in notoriety_list:
            if FindNotoriety(-1, notoriety):
                mobs += GetFindedList()
                # for mob in mobs:
                #     mob_name = GetAltName(mob)
                #     debug("%s" % (mob_name))

        # se achou algo a gente filtra pra devolver o mais proximo
        if len(mobs) > 0:
            return mobs
        else:
            if FindTypesArrayEx(NPC_TYPES, [0xFFFF], [Ground()], False):
                # debug("PEGOU POR NPC_TYPES")
                Wait(1000)
                mobs += GetFindedList()
                if len(mobs) > 0:
                    return mobs

    return []


def count_enemies(
    distance=20,
    mob_types_to_ignore=[],
    notoriety_list=[3, 4],
):
    SetFindDistance(distance)
    SetFindVertical(15)
    Ignore(char)

    mobs = []
    for notoriety in notoriety_list:
        if FindNotoriety(-1, notoriety):
            mobs += GetFindedList()

    if len(mobs) > 0:
        return len(mobs)
    else:
        return 0


def use_primary_ability():
    if GetMana(char) >= 10:
        UsePrimaryAbility()


def use_secondary_ability():
    if GetMana(char) >= 10:
        UseSecondaryAbility()


def reset_context_menu():
    # resettng context or else everytime i click on char it clicks insure again
    SetContextMenuHook(0, 0)


def is_spawn_active():
    if not FindType(CHAMPION_SKULL, Ground()):
        return True
    return False


def is_player_summon(mob):
    mob_noto = GetNotoriety(mob)
    mob_type = GetType(mob)
    if mob_type in PLAYER_SUMMONS and mob_noto == 6:
        return True
    return False


def is_ghost_cam(mob):
    GHOST_CAM_PLAYERS = ["huodong"]
    mob_name = GetAltName(mob)
    for name in GHOST_CAM_PLAYERS:
        if mob_name.lower().find(name) > 0:
            return True
    return False


def is_pk(mob):
    if GetType(mob) in PLAYER_TYPES:
        if GetNotoriety(mob) == 6:
            return True

    return False


# move object made by Llama Vortex
def move_object(objid, qty=1, destination=Backpack(), x=0, y=0, z=0, delay=600):
    drop_delay = GetDropDelay()
    if not (50 < drop_delay < 2000):  # 3000
        drop_delay = 50 if drop_delay < 50 else 2000
    if drop_delay > delay:
        delay = 0
    SetDropDelay(drop_delay)
    source = GetParent(objid)
    if not DragItem(objid, qty):
        debug("You cant drag item!", objid)
        return False
    Wait(delay)
    moved = DropItem(destination, x, y, z)
    if moved:
        SetDropDelay(0)
    return moved


def is_guilded(player):
    player_name = GetAltName(player)
    # Char with guild
    if "[" in player_name:
        return True

    return False


def get_guild_name(player):
    player_name = GetAltName(player)
    player_guild_name = player_name.split("[")[1].strip()

    if player_guild_name:
        return player_guild_name

    return False


def is_guildmate(player):
    player_notoriety = GetNotoriety(player)
    if player_notoriety == 2:
        return True
    else:
        return False


MOONGATE_LOCATIONS = {
    "trammel": {
        "Moonglow": 0,
        "Britain": 1,
        "Jhelom": 2,
        "Yew": 3,
        "Minoc": 4,
        "Trinsic": 5,
        "Skara Brae": 6,
        "New Magincia": 7,
        "New Haven": 8,
    },
    "felluca": {
        "Moonglow": 0,
        "Britain": 1,
        "Jhelom": 2,
        "Yew": 3,
        "Minoc": 4,
        "Trinsic": 5,
        "Skara Brae": 6,
        "Magincia": 7,
        "Buccanneers Den": 8,
    },
}
# button order: facet selection, city selection, ok button
def moongate_travel():
    if _gump["Serial"] == _moongatesFound[0]:  # if its the right gump start clicking
        debug("Selecting moongate")
        NumGumpRadiobutton(0, 5, 0)
        Wait(500)
        NumGumpRadiobutton(0, _location, 1)
        Wait(500)
        NumGumpButton(0, 1)
        Wait(1000)
    else:
        debug("else")


def ress_in_miasma():
    debug("Ressing on miasma")
    if NewMoveXY(346, 1926, True, 0, True):
        if NewMoveXY(343, 1946, True, 0, True):
            if NewMoveXY(343, 1962, True, 0, True):
                if NewMoveXY(332, 1973, True, 0, True):
                    if NewMoveXY(329, 1974, True, 0, True):
                        Step(7)
                        Step(7)
                        Step(7)
                        NewMoveXY(
                            1727, 986, True, 0, True
                        )  # close to the healer outside
                        healer = find_npc_type("Healer")
                        if healer:
                            if GetDistance(healer) > 1:
                                debug("Getting closer to the healer")

                                while (
                                    not gumps.gump_exists(RESS_GUMP_ID)
                                    and GetDistance(healer) > 2
                                ):
                                    step_until_gump(
                                        CalcDir(
                                            GetX(char),
                                            GetY(char),
                                            GetX(healer),
                                            GetY(healer),
                                        ),
                                        RESS_GUMP_ID,
                                        1,
                                    )

    return
