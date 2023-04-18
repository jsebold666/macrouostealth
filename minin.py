####################################################################
# MINING AND ECRU HUNTER BOT FOR UOSTEALTH
# Version: 0.1.0
# Made by gugutz.
# Based on original script by Quaker and Mark
####################################################################

# O que é necessário para rodar:
# use o comando abaixo no prompt ou shell.
# -> pip install discord_webhook
# -> se der erro de SSH, baixar o Win64OpenSSL_Light-1_1_1d.exe
#
# ##################################################################
# FEATURES
# * FAST_GEMS_MODE: Keep only gems on backpack, increasing Ecru rate
# * Support fire beelte for smelting and guarding
# * Auto searches for Forges and Commodity Deed Boxes on the ground
# * External configuration: supports specific char configuration

import sys
import os
from datetime import datetime, timedelta
from discord_webhook import DiscordWebhook

from py_stealth import *

try:
    from py_stealth import *

    from modules.types import (
        BAG,
        GOLD,
        TINKER_TOOLS,
        SHOVEL,
        INGOT,
        ORE,
        AGRESSIVE_MOBS,
        ANY_COLOR,
        SMALL_FORGE,
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
        find_pet_on_ground,
        drop_type,
        drop,
        make_check,
        find_commodity_deed_box_on_ground,
        is_mounted,
        dismount,
        is_pk,
        go_to_britain_via_help_request,
        go_to_britain_bank_vendor_mall_moongate,
        move_char_to_random_direction,
    )
    import modules.common_utils as utils

    from modules.connection import get_char_name
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
except Exception as err:
    AddToSystemJournal("****************************")
    AddToSystemJournal(">>> PYTHON IMPORT ERROR:")
    AddToSystemJournal(f"Error importing macro module: {err}")
    # disable exit traceback for a clean log
    sys.tracebacklimit = 0
    AddToSystemJournal("****************************")
    exit("Check errors above")

ClearSystemJournal()

char = Self()
bank = ObjAtLayer(BankLayer())
backpack = Backpack()
####################################################################
# CONFIGURATION

# protection if UOStealth don't find your name. LAG is the main reason
char_name = connection.get_char_name()

config = {}
config[CharName()] = {
    # general options
    "ore_storage_container": 0,
    "pet_id": 0,
    "skip_bad_runes": True,
    "skip_runes_where_char_died": True,
    "skip_runes_where_char_was_attacked": True,
    "recall_to_escape_attacks": True,
    "wait_home_if_attacked": False,
    "place_to_escape_attacks": "home",
    "discord_webhook_url": "https://discord.com/api/webhooks/967780402922151958/jKDXJeKoeFfOxPCItC9bR0nQbfcDO4ZR505Hi3rLmU0M9oUd2su53K_okHI4Gz-138S7",
    "discord_webhook_afk_url": "https://discord.com/api/webhooks/967780402922151958/jKDXJeKoeFfOxPCItC9bR0nQbfcDO4ZR505Hi3rLmU0M9oUd2su53K_okHI4Gz-138S7",
    "auto_reequip_set": True,
    "auto_refill_tithing_points": True,
    "minimum_tithing_points": 3000,
    # runebook names
    "home_runebook": "Home",
    "ore_runebooks": ["Ore1", "Ore2", "Ore3"],
    "travel_spell": "",
    # rune positions in Home runebook
    "rune_positions": {"home": 1, "shrine": 2},
    "fast_ecru_mode": True,
}
try:
    import mine_config

    utils.debug("Found config file. Searching for character config...")

    if "general_config" in mine_config.config:
        utils.debug("FOUND EXTERNAL DEFAULT CONFIGURATION")
        config[CharName()] = mine_config.config["general_config"]
    if CharName() in mine_config.config:
        utils.debug("FOUND CHAR %s CONFIG" % (CharName()))
        config[CharName()].update(mine_config.config[CharName()])

except Exception as err:
    utils.debug("Error importing config: %s" % (err))
    utils.debug("**USING DEFAULT SCRIPT CONFIG **")
    pass

####################################################################
# AUTO CONFIGURABLE OPTIONS (DONT TOUCH THESE!!!)

PLAY_SOUNDS = False
AUTO_RECONNECT = True
PET = config[CharName()].get("pet_id")
ORE_STORAGE_CONTAINER = config[CharName()].get("ore_storage_container")
FAST_GEMS_MODE = config[CharName()].get("fast_ecru_mode")
FORGE = config[CharName()].get("forge_id")
AUTO_REFILL_TITHING_POINTS = config[CharName()].get("auto_refill_tithing_points")
MINIMUM_TITHING_POINTS = config[CharName()].get("minimum_tithing_points")
AUTO_REEQUIP_SET = config[CharName()].get("auto_reequip_set")

TRAVEL_SPELL = config[CharName()].get("travel_spell")
HOME_RUNEBOOK_NAME = config[CharName()].get("home_runebook")
MINE_RUNEBOOKS = config[CharName()].get("ore_runebooks")
BANK_RUNEBOOK_NAME = config[CharName()].get("bank_runebook")
HOME_RUNE_POSITION = config[CharName()]["rune_positions"].get("home")
SHRINE_RUNE_POSITION = config[CharName()]["rune_positions"].get("shrine")
VENDOR_RUNE_POSITION = config[CharName()]["rune_positions"].get("vendor")
BANK_RUNE_POSITION = config[CharName()]["rune_positions"].get("bank")

SKIP_RUNES_WHERE_CHAR_DIED = config[CharName()].get("skip_runes_where_char_died")
SKIP_BAD_RUNES = config[CharName()].get("skip_bad_runes")
RECALL_TO_ESCAPE_ATTACKS = config[CharName()].get("recall_to_escape_attacks")
WAIT_HOME_IF_ATTACKED = config[CharName()].get("wait_home_if_attacked")
PLACE_TO_ESCAPE_ATTACKS = config[CharName()].get("place_to_escape_attacks")
SKIP_RUNES_WHERE_CHAR_WAS_ATTACKED = config[CharName()].get(
    "skip_runes_where_char_was_attackd"
)
BOT_MINIMUM_BALANCE = 100000  # Runebook names

DISCORD_WEBHOOK_URL = config[CharName()].get("discord_webhook_url")

# ======================================================================
# SCRIPT VARIABLES AND TYPES
# ======================================================================

number_of_disconnections = 0
last_disconnection = ""

ECRU_CITRINE = 0x3195
VERITE_COLOR = 2207
VALORITE_COLOR = 2219
MAX_ECRUS_IN_BACKPACK = 1
FIRE_BEETLE_TYPE = 0xA9


GEMS = [
    0x3192,
    0x3193,  # ?
    0x3194,  # ?
    0x3195,  # ecru citrine
    0x3197,
    0x3198,
]

CURRENT_BALANCE = 0
CHECKS_IN_BANK = 0
CHAR_BANK_LOCATION = ""
CHAR_BANK_ID = ""
MAX_WEIGHT = MaxWeight()
WEIGHT_LIMIT = MaxWeight() - 60

if SKIP_RUNES_WHERE_CHAR_WAS_ATTACKED:
    runes_where_char_was_attacked = {}
    for runebook in MINE_RUNEBOOKS:
        runes_where_char_was_attacked[runebook] = []
if SKIP_RUNES_WHERE_CHAR_DIED:
    runes_where_char_died = {}
    for runebook in MINE_RUNEBOOKS:
        runes_where_char_died[runebook] = []
if SKIP_BAD_RUNES:
    bad_runes = {}
    for runebook in MINE_RUNEBOOKS:
        bad_runes[runebook] = []

# security sets
global CURRENT_RUNEBOOK
global CURRENT_RUNE
CURRENT_RUNEBOOK = "Ore1"
CURRENT_RUNE = 1

global MINIMUM_TINKER_TOOLS_ON_STORAGE
MINIMUM_TINKER_TOOLS_ON_STORAGE = len(config)
if MINIMUM_TINKER_TOOLS_ON_STORAGE < 5:
    MINIMUM_TINKER_TOOLS_ON_STORAGE = 5
MINIMUM_SHOVELS_IN_BACKPACK = 5


TINKERMENU_TINKERTOOLS = 23
TINKERMENU_SHOVEL = 72
WAIT_TIME = 500  # Default Wait Time
WAIT_LAG_TIME = 10000  # Default Wait Lag Time


def confirm_script_loop_conditions():
    if Dead():
        return False
    if not Connected():
        return False

    return True


def print_script_stats():
    utils.debug("------------------------------------------------")
    utils.debug("Connected since: %s" % (ConnectedTime()))
    utils.debug("Disconnections: %d" % (number_of_disconnections))
    if last_disconnection != "":
        utils.debug("Last disconnection: %d" % (last_disconnection))

    utils.debug("Tithing points: %d" % (current_tithing_points))
    utils.debug("------------------------------------------------")


def confirm_script_loop_conditions():
    if Dead():
        return False
    if not Connected():
        return False

    return True


# ##############################################
# NEW HELPER FUNCTIONS
# ##############################################


def check_afk_gump():
    if is_afk_gump():
        utils.debug("***********************")
        utils.debug("!!! AFK GUMP DETECTED !!!")
        utils.debug("Sending discord msg...")
        webhooks.send_discord_message(
            DISCORD_WEBHOOK_URL, "**AFK GUMP** on {Profile()} / {CharName()}"
        )
        if afk.solve_afk_gump():
            utils.debug("AFK Gump Solved!")
            return true
    else:
        utils.debug("Gump detected was NOT an AFK Gump")
        utils.debug("Leaving as is...")
        return False
        # close_gumps()


def check_jail():
    if jail.is_char_in_6_hours_jail():
        print("** JAIL 6 HOURS **")
        try:
            if PLAY_SOUNDS:
                PlayWav(ALARM_SOUND)
            send_discord_message(
                DISCORD_WEBHOOK_URL,
                "**MINER JAIL 6 HOURS ** @everyone %s is in 6 HOURS JAIL. Starting jail timer..."
                % (char_name),
            )
        except:
            pass
        Wait(1000)
        UOSay("I will not commit a bannable offense again")
        exit()
        return True

    if jail.is_char_in_jail():
        try:
            if PLAY_SOUNDS:
                PlayWav(ALARM_SOUND)
            send_discord_message(
                DISCORD_WEBHOOK_URL,
                "**MINER JAIL** @everyone %s is in jail and is gonna escape"
                % (char_name),
            )
        except:
            pass
        Wait(1000)
        jail.escape_jail()


def open_storage():
    if ORE_STORAGE_CONTAINER:
        if (
            GetDistance(ORE_STORAGE_CONTAINER) <= 2
            and GetDistance(ORE_STORAGE_CONTAINER) != -1
        ):
            # Open Container
            UseObject(ORE_STORAGE_CONTAINER)
            utils.wait_lag(100)
        else:
            utils.debug("Moving closer to the container")
            if NewMoveXY(
                GetX(ORE_STORAGE_CONTAINER), GetY(ORE_STORAGE_CONTAINER), True, 1, True
            ):
                utils.wait_lag(100)
            else:
                utils.debug("Too far from Container! Abort UNload!")
                return False
    else:
        find_and_save_ore_container_maybe()


def find_and_save_ore_container_maybe():
    global ORE_STORAGE_CONTAINER
    if ORE_STORAGE_CONTAINER:
        utils.debug("Reusing previously found commodity box")
        return ORE_STORAGE_CONTAINER
    else:
        start_time = datetime.now()
        while not ORE_STORAGE_CONTAINER:
            ORE_STORAGE_CONTAINER = utils.find_commodity_deed_box_on_ground()
            utils.wait_lag(10)
            if utils.check_timer(start_time, 6000):
                utils.debug("Timeout while searching for ore container. Breaking...")
                break
            if ORE_STORAGE_CONTAINER:
                utils.debug("** Found and set storage container")


def find_and_save_forge_maybe():
    global FORGE
    if FORGE:
        utils.debug("Reusing previously found forge")
        return FORGE
    else:
        start_time = datetime.now()
        while not FORGE:
            FORGE = utils.find_ground(types.SMALL_FORGE)
            utils.wait_lag(10)
            if check_timer(start_time, 6000):
                utils.debug("Timeout while searching for forge. Breaking...")
                break


def return_to_previous_mine_spot():
    global CURRENT_RUNEBOOK
    global CURRENT_RUNE
    remount()
    # uses in-memory values for runebook and runenumber
    utils.debug("Returning to previous mining spot")
    utils.travel_to(CURRENT_RUNEBOOK, TRAVEL_SPELL, CURRENT_RUNE, 4000)


def get_ores_from_ground_maybe():
    SetFindDistance(2)
    SetFindVertical(10)
    start_time = datetime.now()

    ores_on_ground = CountGround(types.ORE)
    if FAST_CASH:
        colors_to_search = 0
    else:
        colors_to_search = -1

    limit_to_pick = MaxWeight() - Weight()
    while FindTypeEx(types.ORE, colors_to_search, Ground(), False):
        if limit_to_pick > 0:
            if Weight() <= WEIGHT_LIMIT:
                utils.debug(
                    "Found %d ores on the ground and moving to backpack"
                    % (ores_on_ground)
                )
                MoveItem(FindItem(), limit_to_pick, Backpack(), 0, 0, 0)
                utils.wait_lag(100)
            else:
                utils.debug("Found ores on the ground but char is overweight to get it")
                break
        else:
            utils.debug(
                "Char doenst have room in backpack to pick up ores on the ground"
            )
            break

        if check_timer(start_time, 4000):
            utils.debug("Timeout while getting ores from ground. Breaking...")
            break

    if Weight() >= WEIGHT_LIMIT:
        begin_sell_and_unload_maybe()

    if ores_on_ground == 0:
        return True
    else:
        return False


def reduce_weight_to_travel_maybe():
    if Weight() >= MaxWeight():
        # reduce_weight_to_travel(BOARD_TYPE,0,1)
        amount_to_drop = Weight() - MaxWeight()
        drop_type(types.ORE, amount_to_drop)


def begin_sell_and_unload_maybe():
    if (
        confirm_script_loop_conditions()
        and utils.count(types.ORE)
        and Weight() >= WEIGHT_LIMIT
    ):
        reduce_weight_to_travel_maybe()

    travel_to_home()

    while confirm_script_loop_conditions() and utils.count(types.ORE):
        smelt_ores()


# ======================================================================
# JOURNAL UTILS
# ======================================================================


def is_target_in_sight():
    cannot_be_seen_journal_msgs = "cannot be seen"

    # if we get a msg in journal saying wood is out, mark spot as invalid
    if InJournal(cannot_be_seen_journal_msgs) > -1:
        ClearJournal()
        return True
    else:
        return False


def confirm_mine_success():
    mine_success_journal_msgs = "You hack at | You put some | You chop some "

    # if we get a msg in journal saying wood is out, mark spot as invalid
    if InJournal(mine_success_journal_msgs) > -1:
        ClearJournal()
        return True
    else:
        return False


def is_spot_out_of_ore():
    spot_out_of_ore_journal_msgs = "no metal here to mine"

    if InJournal(spot_out_of_ore_journal_msgs) > 0:
        ClearJournal()
        return True
    else:
        return False


def cant_place_ore_in_backpack():
    cant_place_ore_in_backpack_msg = "XXX PEGAR MSG CORRETA XXX"

    if InJournal(cant_place_ore_in_backpack_msg) > 0:
        ClearJournal()
        return True
    else:
        return False


def is_spot_valid():
    fail_to_mine_journal_msgs = (
        "There is nothing here |"
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

    if InJournal(fail_to_mine_journal_msgs) > -1:
        ClearJournal()
        return False
    else:
        return True


def get_ores_from_ground_maybe():
    SetFindDistance(2)
    SetFindVertical(10)
    ores_on_ground = CountGround(types.ORE)
    start_time = datetime.now()
    limit_to_pick = MaxWeight() - Weight()
    while ores_on_ground > 0 and Weight() <= WEIGHT_LIMIT:
        if limit_to_pick > 0:
            utils.debug(
                "Found %d ores on the ground and moving to backpack" % (ores_on_ground)
            )
            MoveItem(FindItem(), 65000, Backpack(), 0, 0, 0)
            utils.wait_lag(0)
        else:
            utils.debug(
                "Char doenst have room in backpack to pick up ores on the ground"
            )

        if check_timer(start_time, 8000):
            utils.debug("Timeout while moving ore from ground to backpack. Breaking...")
            break
    if ores_on_ground == 0:
        return True
    else:
        return False


def remount():
   if PET:
        if not utils.is_mounted(char):
            while GetDistance(PET) > 2:
                UOSay("all guard me")
                Wait(1000)
            utils.debug("Remounting...")
            UseObject(PET)
            utils.wait_lag(300)


def recall_home():
    utils.debug("Going home.")
    remount()
    if utils.travel_to(HOME_RUNEBOOK_NAME, TRAVEL_SPELL, HOME_RUNE_POSITION):
        return True


def recall_shrine():
    utils.debug("Going to the shrine.")
    remount()
    if utils.travel_to(HOME_RUNEBOOK_NAME, TRAVEL_SPELL, SHRINE_RUNE_POSITION):
        return True


# ##############################################
#
# RUNEBOOK END
#
# ##############################################


def smelt_ores():
    forge = ""
    IgnoreReset()
    # defines if will use PET bettle or home forge to smelt
    forge_name = ""
    if PET:
        utils.debug("Using beetle as forge")
        forge = PET
        if utils.is_mounted(char):
            utils.dismount()
    else:
        # utils.debug("Using home forge")
        forge = FORGE
    if forge and GetDistance(forge) >= 0:
        forge_name = get_item_name(forge)

    if not forge:
        return False

    if FindTypesArrayEx(types.ORES, [ANY_COLOR], [Backpack()], False):
        utils.debug("Starting Smelting...")
        ores_in_backpack = GetFindedList()
        for ore in ores_in_backpack:
            ore_name = get_item_name(ore)
            ore_amount = FindQuantity()
            start_time = datetime.now()
            while IsObjectExists(ore):
                if GetQuantity(ore) <= 1:
                    utils.debug("Ore pile is only 1. Abort smelting, but why?!?")
                    break
                UseObject(ore)
                WaitForTarget(3000)
                WaitTargetObject(forge)
                if TargetPresent():
                    utils.debug(f"Smelting {ore_name} on {forge_name}")
                    TargetToObject(forge)
                Wait(CheckLag(3000))
                if check_timer(start_time, 10000):
                    utils.debug("Timeout smelting...")
                    return False
            # Ignore(ore)
            Wait(CheckLag(3000))


def get_closer_to_forge():
    if 0 < GetDistance(FORGE) <= 2:
        utils.debug("Forge is more than 2 tiles away.")
        if NewMoveXY(GetX(FORGE), GetY(FORGE), True, 1, True):
            utils.debug("Got to the forge")
            Wait(CheckLag(3000))
        else:
            utils.debug("Could not move closer to forge! Abort UNload!")
            return False
    else:
        utils.debug("Char is already close to the forge")


def get_closer_to_ore_storage_container():
    if 0 < GetDistance(ORE_STORAGE_CONTAINER) >= 2:
        utils.debug("Storage Container is more than 2 tiles away.")
        if NewMoveXY(
            GetX(ORE_STORAGE_CONTAINER), GetY(ORE_STORAGE_CONTAINER), True, 1, True
        ):
            utils.debug("Got to storage container")
            Wait(CheckLag(3000))
        else:
            utils.debug("!! Could not move closer to storage container!")
            return False
    else:
        utils.debug("Char is already close to storage container")


def unload():
    find_and_save_ore_container_maybe()
    find_and_save_forge_maybe()

    utils.debug("Unloading ores in home")
    # CheckAFK("miner")

    if Dead():
        utils.debug("Dead on unload")
        return False

    open_storage()

    get_closer_to_forge()

    start_time = datetime.now()
    while confirm_script_loop_conditions() and FindTypesArrayEx(
        GEMS, [ANY_COLOR], [Backpack()], False
    ):
        gem = FindItem()
        gem_name = get_item_name(gem)
        gem_amount = FindQuantity()
        utils.debug("Moving %s to stock" % (gem_name))
        MoveItem(gem, gem_amount, ORE_STORAGE_CONTAINER, 0, 0, 0)
        Wait(CheckLag(3000))
        if check_timer(start_time, 10000):
            utils.debug("10s moving stuff to container. Breaking...")
            break

    smelt_ores()

    # Ingots
    while confirm_script_loop_conditions() and FindType(0x1BF2, Ground()):
        utils.debug("ingots from ground")
        ClientPrintEx(FindItem(), 33, 0, "!!!")
        MoveItem(FindItem(), 65000, ORE_STORAGE_CONTAINER, 0, 0, 0)
        Wait(CheckLag(3000))
    while confirm_script_loop_conditions() and FindType(0x1BF2, Backpack()):
        utils.debug("ingots from backpack")
        MoveItem(FindItem(), 65000, ORE_STORAGE_CONTAINER, 0, 0, 0)
        Wait(CheckLag(3000))


def upload():
    if Dead():
        utils.debug("Dead on upload")
        return
    utils.debug("Getting tinker tools")
    if (
        GetDistance(ORE_STORAGE_CONTAINER) <= 2
        and GetDistance(ORE_STORAGE_CONTAINER) != -1
    ):
        #check_tinker_tools_on_storage(MINIMUM_TINKER_TOOLS_ON_STORAGE)
        getitems(types.TINKER_TOOLS, 1, 1, ORE_STORAGE_CONTAINER)

        make_shovels_maybe()
    else:
        utils.debug("Too far from Container! Abort UPload!")


def combine_ore_piles():
    utils.debug("Combining ore piles...")
    for ore_type in types.ORES:
        FindType(ore_type, Backpack())
        ores = GetFindedList()
        for ore in ores:
            color = GetColor(ore)
            if FindTypeEx(0x19B7, color, Backpack(), True):
                UseObject(ore)
                if WaitForTarget(3000):
                    mainStack = FindTypeEx(ore_type, color, Backpack(), True)
                    TargetToObject(mainStack)
                    utils.wait_lag(1000)


def mine(list):
    global CURRENT_RUNEBOOK
    global CURRENT_RUNE
    if PET:
        if is_mounted(char):
            utils.dismount()
            UOSay("all follow me")
    if not confirm_script_loop_conditions():
        return False
    for tile, x, y, z in list:
        if confirm_script_loop_conditions():
            check_afk_gump()

            if NewMoveXY(x, y, True, 1, True):
                spot_valid = True
                spot_out_of_ore = False

                previous_weight = Weight()
                while (
                    spot_valid
                    and utils.count(SHOVEL)
                    and confirm_script_loop_conditions()
                    and Weight() < WEIGHT_LIMIT
                ):
                    # check_connection()

                    if TargetPresent():
                        CancelTarget()

                    drop_special_resources_on_ground_maybe()
                    while not TargetPresent():
                        # find shovel to mine
                        if not FindType(SHOVEL, Backpack()):
                            utils.debug(">> Out of shovels. Going to make some.")
                            return False
                        else:
                            # utils.debug("preso aqui")
                            UseType2(SHOVEL)
                            # UseObject(FindItem())
                            Wait(10)

                    if TargetPresent():
                        starttime = datetime.now()
                        if tile in range(1339, 1387):
                            TargetToTile(tile, x, y, z)  # cave floor
                            utils.wait_lag(1)
                        else:
                            TargetToTile(
                                0, x, y, z
                            )  # for some reason i can target only mountains.
                            utils.wait_lag(1)

                    smelt_ores()

                    mobs_nearby = get_nearby_mobs(20, [], [3, 4, 6])
                    # mobs_nearby = get_nearby_mobs(10, [], 6)
                    danger = False
                    if len(mobs_nearby) > 0:
                        for mob in mobs_nearby:
                            mob_name = GetName(mob)
                            if (mob_name != 'Jethro'):
                                if utils.is_pk(mob) or GetType(mob) in AGRESSIVE_MOBS:
                                    danger = True

                        if danger:
                            utils.debug(f">>> {mob_name} close to miner {char_name}.")
                            # try:
                            #     msg = f"**MINER IN RISK** **{mob_name}** close to miner **{char_name}** at **{CURRENT_RUNEBOOK} - Rune {CURRENT_RUNE}**. Tried to escape"
                            #     send_discord_message(DISCORD_WEBHOOK_URL, msg)
                            # except:
                            #     pass

                            if WAIT_HOME_IF_ATTACKED:
                                if PLACE_TO_ESCAPE_ATTACKS == "home":
                                    recall_home()
                                else:
                                    recall_bank()

                                utils.debug(
                                    ">>> Waiting 5 minutes to return to mine spot..."
                                )
                                Wait(300000)
                                break
                            elif RECALL_TO_ESCAPE_ATTACKS:
                                return False

                    # if weight changed, it confirms previous mine was succesfull
                    if Weight() > previous_weight:
                        # utils.debug(f"Mining. Weight: {Weight()} / {MaxWeight()}")
                        utils.debug(f"> Mining. (W: {Weight()}/{MaxWeight()})")
                        previous_weight = Weight()

                    utils.wait_lag(1)

                    if is_spot_out_of_ore():
                        utils.debug(
                            # f"runebook {CURRENT_RUNEBOOK} | rune {CURRENT_RUNE} is out of ore. Travelling to next rune."
                            f">> Runebook {CURRENT_RUNEBOOK} | Rune {CURRENT_RUNE} is out of ore. Travelling to next rune."
                        )
                        return False

                    if not is_spot_valid():
                        utils.debug(
                            # f"{CURRENT_RUNE} at {CURRENT_RUNEBOOK} runebook is being marked as invalid mining spot."
                            f">>> {CURRENT_RUNE} at {CURRENT_RUNEBOOK} runebook is being marked as invalid mining spot."
                        )
                        spot_valid = False
                        return False

                    if GetHP(char) < GetMaxHP(char) * 0.8:
                        if SKIP_RUNES_WHERE_CHAR_WAS_ATTACKED:
                            runes_where_char_was_attacked[CURRENT_RUNEBOOK].append(
                                CURRENT_RUNE
                            )
                            try:
                                msg = (
                                    "Miner %s being attacked! Tried to escape"
                                    % (char_name),
                                )
                                send_discord_message(DISCORD_WEBHOOK_URL, msg)
                            except:
                                pass
                            return False

                return True

        else:
            return


def gettiles2(radius):
    temp = []
    temp2 = []
    caves = (
        1339,
        1340,
        1341,
        1342,
        1343,
        1344,
        1345,
        1346,
        1347,
        1348,
        1349,
        1350,
        1351,
        1352,
        1353,
        1354,
        1355,
        1356,
        1357,
        1358,
        1359,
        1361,
        1362,
        1363,
        1386,
    )  # caves
    mountains = (
        220,
        221,
        222,
        223,
        224,
        225,
        226,
        227,
        228,
        229,
        230,
        231,
        236,
        237,
        238,
        239,
        240,
        241,
        242,
        243,
        244,
        245,
        246,
        247,
        252,
        253,
        254,
        255,
        256,
        257,
        258,
        259,
        260,
        261,
        262,
        263,
        268,
        269,
        270,
        271,
        272,
        273,
        274,
        275,
        276,
        277,
        278,
        279,
        286,
        287,
        288,
        289,
        290,
        291,
        292,
        293,
        294,
        296,
        296,
        297,
        321,
        322,
        323,
        324,
        467,
        468,
        469,
        470,
        471,
        472,
        473,
        474,
        476,
        477,
        478,
        479,
        480,
        481,
        482,
        483,
        484,
        485,
        486,
        487,
        492,
        493,
        494,
        495,
        543,
        544,
        545,
        546,
        547,
        548,
        549,
        550,
        551,
        552,
        553,
        554,
        555,
        556,
        557,
        558,
        559,
        560,
        561,
        562,
        563,
        564,
        565,
        566,
        567,
        568,
        569,
        570,
        571,
        572,
        573,
        574,
        575,
        576,
        577,
        578,
        579,
        581,
        582,
        583,
        584,
        585,
        586,
        587,
        588,
        589,
        590,
        591,
        592,
        593,
        594,
        595,
        596,
        597,
        598,
        599,
        600,
        601,
        610,
        611,
        612,
        613,
        1010,
        1741,
        1742,
        1743,
        1744,
        1745,
        1746,
        1747,
        1748,
        1749,
        1750,
        1751,
        1752,
        1753,
        1754,
        1755,
        1756,
        1757,
        1771,
        1772,
        1773,
        1774,
        1775,
        1776,
        1777,
        1778,
        1779,
        1780,
        1781,
        1782,
        1783,
        1784,
        1785,
        1786,
        1787,
        1788,
        1789,
        1790,
        1801,
        1802,
        1803,
        1804,
        1805,
        1806,
        1807,
        1808,
        1809,
        1811,
        1812,
        1813,
        1814,
        1815,
        1816,
        1817,
        1818,
        1819,
        1820,
        1821,
        1822,
        1823,
        1824,
        1831,
        1832,
        1833,
        1834,
        1835,
        1836,
        1837,
        1838,
        1839,
        1840,
        1841,
        1842,
        1843,
        1844,
        1845,
        1846,
        1847,
        1848,
        1849,
        1850,
        1851,
        1852,
        1853,
        1854,
        1861,
        1862,
        1863,
        1864,
        1865,
        1866,
        1867,
        1868,
        1869,
        1870,
        1871,
        1872,
        1873,
        1874,
        1875,
        1876,
        1877,
        1878,
        1879,
        1880,
        1881,
        1882,
        1883,
        1884,
        1981,
        1982,
        1983,
        1984,
        1985,
        1986,
        1987,
        1988,
        1989,
        1990,
        1991,
        1992,
        1993,
        1994,
        1995,
        1996,
        1997,
        1998,
        1999,
        2000,
        2001,
        2002,
        2003,
        2004,
        2028,
        2029,
        2030,
        2031,
        2032,
        2033,
        2100,
        2101,
        2102,
        2103,
        2104,
        2105,
    )  # mountains

    rocks = (
        0x453B,
        0x453C,
        0x453D,
        0x453E,
        0x453F,
        0x4540,
        0x4541,
        0x4542,
        0x4543,
        0x4544,
        0x4545,
        0x4546,
        0x4547,
        0x4548,
        0x4549,
        0x454A,
        0x454B,
        0x454C,
        0x454D,
        0x454E,
        0x454F,
    )  # rocks

    for currenttile in caves, mountains, rocks:

        land = GetLandTilesArray(
            GetX(Self()) - radius,
            GetY(Self()) - radius,
            GetX(Self()) + radius,
            GetY(Self()) + radius,
            WorldNum(),
            currenttile,
        )
        if len(land) > 0:
            temp.append(land)
        static = GetStaticTilesArray(
            GetX(Self()) - radius,
            GetY(Self()) - radius,
            GetX(Self()) + radius,
            GetY(Self()) + radius,
            WorldNum(),
            currenttile,
        )
        if len(static) > 0:
            temp.append(static)

    for tile in temp:
        for subtiles in tile:
            temp2.append(subtiles)

    return temp2


def check_tinker_tools_on_storage(minAmount):
    if (
        GetDistance(ORE_STORAGE_CONTAINER) <= 2
        and GetDistance(ORE_STORAGE_CONTAINER) != -1
    ):
        UseObject(ORE_STORAGE_CONTAINER)
        utils.wait_lag(100)

        amount_of_tinker_tools_in_storage = utils.count(
            types.TINKER_TOOLS, 1, 1, ORE_STORAGE_CONTAINER
        )
        utils.debug(
            "Tinker tools on storage: %s | Required: %d"
            % (amount_of_tinker_tools_in_storage, minAmount)
        )

        if utils.count(types.TINKER_TOOLS) < 1:
            utils.debug("Doesn't have tinkertools on backpack! Check on storage")
            if amount_of_tinker_tools_in_storage < 1:
                make_tinker_tools(MINIMUM_TINKER_TOOLS_ON_STORAGE)
            else:
                getitems(types.TINKER_TOOLS, 1, 1, ORE_STORAGE_CONTAINER)

        if utils.count(types.TINKER_TOOLS, ORE_STORAGE_CONTAINER) < minAmount:
            utils.debug("Low on tinker on storage! Making it")
            Tinkering(
                types.TINKER_TOOLS, minAmount + 2, TINKERMENU_TINKERTOOLS
            )  # +2 = segurança e também é 1 que você pega e bota no próprio backpack depois de craftar
            Tinkering(
                types.TINKER_TOOLS, minAmount + 2, TINKERMENU_TINKERTOOLS
            )  # +2 = segurança e também é 1 que você pega e bota no próprio backpack depois de craftar
            utils.wait_lag(10)

            start_time = datetime.now()
            while confirm_script_loop_conditions() and FindTypeEx(
                types.TINKER_TOOLS, 0x0000, Backpack(), False
            ):
                MoveItem(FindItem(), 65000, ORE_STORAGE_CONTAINER, 0, 0, 0)
                utils.wait_lag(1000)
                if check_timer(start_time, 10000):
                    utils.debug(
                        "10s moving tinker tools to storage container. Breaking..."
                    )
                    break

            getitems(types.TINKER_TOOLS, 1, 1, ORE_STORAGE_CONTAINER)


def getitems(type, minamount, amount, storage):
    if GetQuantity(FindTypeEx(type, 0x0000, Backpack(), False)) < minamount:
        UseObject(Backpack())
        Wait(500)
        CheckLag(3000)
        start_time = datetime.now()
        while LastContainer() != storage:
            UseObject(storage)
            Wait(500)
            CheckLag(3000)
            if check_timer(start_time, 10000):
                utils.debug("10s moving tinker tools to storage container. Breaking...")
                break
        CheckLag(3000)
        if GetQuantity(FindTypeEx(type, 0x0000, storage, False)) >= amount:
            item = FindItem()
            item_name = get_item_name(item)
            utils.debug("Restocking %d %s" % (amount, item_name))
            MoveItem(item, amount, backpack, 0, 0, 0)
            Wait(500)
        elif (
            GetQuantity(FindTypeEx(type, 0x0000, storage, False)) <= amount
            and type == types.INGOT
        ):
            item = FindItem()
            item_name = get_item_name(item)
            utils.debug("Trying to move ingot pile to ground to use new one")
            MoveItem(item, amount, Ground(), GetX(char) + 1, GetY(char) + 1, GetZ(char))
            Wait(1000)
        else:
            utils.debug("Storage out of resources. Warning on discord.")
            try:
                if PLAY_SOUNDS:
                    PlayWav(ALARM_SOUND)
                send_discord_message(
                    DISCORD_WEBHOOK_URL,
                    "**NO RESOURCES** Miner %s has no resources in restock!"
                    % (char_name),
                )
            except:
                pass


def make_shovels_maybe():
    # check shovels
    amount_of_shovels_in_backpack = GetQuantity(
        FindTypeEx(SHOVEL, 0x0000, Backpack(), False)
    )
    if amount_of_shovels_in_backpack < 5:
        amount_of_shovels_to_make = (
            MINIMUM_SHOVELS_IN_BACKPACK - amount_of_shovels_in_backpack
        )
        utils.debug("Making shovels")
        return Tinkering(SHOVEL, amount_of_shovels_to_make, TINKERMENU_SHOVEL)
    else:
        utils.debug("Already have %d shovels in backpack")


def make_tinker_tools(min_amount=MINIMUM_TINKER_TOOLS_ON_STORAGE):
    # check tinker tools
    amount_of_tinker_tools_in_backpack = GetQuantity(
        FindTypeEx(SHOVEL, 0x0000, Backpack(), False)
    )
    if amount_of_tinker_tools_in_backpack < min_amount:
        utils.debug("Making tinker tools")
        return Tinkering(types.TINKER_TOOLS, 1, TINKERMENU_TINKERTOOLS)
    else:
        utils.debug("Already have enought tinker tools")


def Tinkering(itemType, amount, buttonnumber):
    if utils.count(itemType) < amount:
        start_time = datetime.now()
        while utils.count(itemType) < amount:
            if check_timer(start_time, 30000):
                utils.debug("30 sec tinkering. Breaking...")
                break
            getitems(types.INGOT, 10, 100, ORE_STORAGE_CONTAINER)
            if FindType(types.TINKER_TOOLS, Backpack()):
                UseObject(FindItem())
                # UseType2(types.TINKER_TOOLS)
                Wait(CheckLag(3000))
                # if not gumps.in_gump("Shovel"):
                #     utils.debug("Coundlt find shovels gump")
                #     break
                utils.debug(f">> Tinkering: {Count(itemType)}/{amount} created")
                gumps.in_gump("TINKERING MENU", 8)
                Wait(CheckLag(3000))
                gumps.in_gump("TINKERING MENU", buttonnumber)
                Wait(CheckLag(3000))
                gumps.in_gump("TINKERING MENU", 0)
                Wait(CheckLag(3000))
            else:
                utils.debug("Out of tinker tools while tinkering!")
                return False

        utils.debug(f"Tinkering -> {Count(itemType)} / {amount}")


# ======================================================================
# PREPARE TO START
# ======================================================================

connection.connect()
char_name = connection.get_char_name()
if char_name:
    print("Char name: %s" % (char_name))

# if travel spell is not set in char config, try to infer it
# if that fails, then exit
if not TRAVEL_SPELL:
    TRAVEL_SPELL = utils.set_travel_method()
    if not TRAVEL_SPELL:
        print(
            "Char doenst have a way to travel. Train magery or chivalry, get regs or tithe and try again"
        )
        print(f"Char Magery: {GetSkillValue('Magery')}")
        print(f"Char Chivalry: {GetSkillValue('Chivalry')}")
        print(f"Char Tithing Points: {utils.get_current_tithing_points()}")
        # disable exit traceback for a clean log
        sys.tracebacklimit = 0
        exit("Check errors above")


##############################################################################
# main routine.
#
def drop_special_resources_on_ground_maybe():
    if FAST_GEMS_MODE:
        if Weight() >= WEIGHT_LIMIT:
            start_time = datetime.now()
            # combine_ore_piles()
            while FindTypesArrayEx(types.ORES, [0xFFFF], [Backpack()], False):
                ores_in_backpack = GetFindedList()
                for ore in ores_in_backpack:
                    if check_timer(start_time, 8000):
                        utils.debug("Timeout 8s droping ores on ground...")
                        utils.move_char_to_random_direction()
                        return False
                    # resource_name = SPECIAL_MINING_RESOURCES.get("resource")
                    ore_color = GetColor(ore)

                    if ore_color == VALORITE_COLOR and ore_color == VERITE_COLOR:
                        Ignore(ore)
                    if ore_color != VALORITE_COLOR and ore_color != VERITE_COLOR:
                        found = FindItem()
                        resource_name = get_item_name(found)
                        resource_amount = FindQuantity()
                        utils.debug(
                            "FAST ECRU is on. Throwing %s on the ground"
                            % (resource_name)
                        )
                        utils.drop(found, resource_amount)


def handle_death():

    global FIRST_RUN
    # notify on discord
    try:
        if PLAY_SOUNDS:
            PlayWav(ALARM_SOUND)
        if FIRST_RUN:
            debug(
                "**MINER DEAD** | {ProfileName()} ({char_name}) started macro dead! Going to ress..."
                % (char_name),
            )
            # send_discord_message(
            #     DISCORD_WEBHOOK_URL,
            #     "**MINER DEAD** | {ProfileName()} ({char_name}) started macro dead! Going to ress..."
            #     % (char_name),
            # )
        else:
            send_discord_message(
                DISCORD_WEBHOOK_URL,
                f"**MINER DEAD** | {ProfileName()} ({char_name}) dead in {CURRENT_RUNEBOOK} -> Rune {CURRENT_RUNE}",
            )
    except:
        pass

    # set to skip rune so char wont die again on this spot
    if not FIRST_RUN and SKIP_RUNES_WHERE_CHAR_DIED:
        utils.debug(
            "Miner died on rune %d from %s runebook. Will skip this rune on next mining cycle."
            % (CURRENT_RUNE, CURRENT_RUNEBOOK)
        )
        runes_where_char_died[CURRENT_RUNEBOOK].append(CURRENT_RUNE)

    ress.ress()
    RELOG = True
    utils.remove_death_robe()
    if AUTO_REEQUIP_SET:
        if not utils.is_set_equiped():
            utils.dress_char_set()
        utils.save_char_set()


def check_tithe():
    if not Dead() and Connected():
        if TRAVEL_SPELL == "chiva":
            current_tithing_points = utils.get_current_tithing_points()
            if current_tithing_points < 15:
                send_discord_message(
                    DISCORD_WEBHOOK_URL,
                    "**MINER NO TITHE** @everyone %s has %d tithe and CANT TRAVEL! Taking char to Britain bank moongate and exiting Macro..."
                    % (char_name, current_tithing_points),
                )
                try:
                    PlayWav(ALARM_WAV)
                except:
                    pass
                utils.debug(
                    "**NO TITHE** %s only has %d tithe and CANT TRAVEL! Taking char to brit..."
                    % (char_name, current_tithing_points),
                )
                utils.go_to_britain_via_help_request()
                utils.go_to_britain_bank_vendor_mall_moongate()
                exit()

            if current_tithing_points < MINIMUM_TITHING_POINTS:
                if AUTO_REFILL_TITHING_POINTS:
                    utils.debug("*LOW TITHE* Char is low on tithing points.")
                    utils.debug("Going to the bank to get money to tithe gold")

                    # check and solve char weight first
                    if utils.count(types.ORE):
                        utils.debug(
                            "Dropping ores from backpack to withdraw gold to the shrine"
                        )
                        utils.drop_type(types.ORE, utils.count(types.ORE))
                    if utils.count(types.ORE):
                        utils.debug(
                            "Dropping ores from backpack to withdraw gold to the shrine"
                        )
                        utils.drop_type(types.ORE, utils.count(types.ORE))
                    if Weight() >= MaxWeight():
                        utils.debug(
                            "Char is overweight. Reducing weight to go tithe gold"
                        )
                        reduce_weight_to_travel()

                    if Gold() < 10000:
                        recall_home()
                        utils.wait_lag(1000)
                        find_and_save_ore_container_maybe()
                        get_closer_to_ore_storage_container()
                        UseObject(ORE_STORAGE_CONTAINER)
                        utils.wait_lag(1000)
                        # sometimes (most of the times) stealth subcontainers search fails
                        # so we open the bags ourselves to FindType to find it
                        if FindType(types.BAG, ORE_STORAGE_CONTAINER):
                            for item in GetFindedList():
                                UseObject(item)
                                utils.wait_lag(600)
                        if FindTypeEx(GOLD, 0, ORE_STORAGE_CONTAINER, True):
                            gold_coin = FindItem()
                            start_time = datetime.now()
                            while utils.count(GOLD) < 30000:
                                utils.debug(
                                    "Getting gold from storage container to tithe"
                                )
                                Grab(gold_coin, 30000)
                                utils.wait_lag(1000)
                                if check_timer(start_time, 10000):
                                    utils.debug(
                                        "Timeout 10s geting gold to tithe... Breaking..."
                                    )
                                    utils.move_char_to_random_direction()
                                    return False
                        else:

                            send_discord_message(
                                DISCORD_WEBHOOK_URL,
                                f"**MINER NO GOLD** @everyone No gold in home for **{ProfileName()} ({char_name})**",
                            )

                    if Gold() > 0:
                        recall_shrine()
                        utils.tithe_gold_to_shrine()
                        return True
                else:
                    utils.debug(
                        "*LOW TITHE* Char only has %d tithing points left which is bellow the threshold"
                        % (current_tithing_points)
                    )
                    utils.debug("Buy more tithing points and play the script again")
                    utils.debug(
                        "The script also supports auto refilling tithing points when this happens"
                    )
                    utils.debug(
                        "Just mark a rune to a shrine and put it your Home Runebook"
                    )
                    Disconnect()
                    exit()
                    return False


if __name__ == "__main__":
    global FIRST_RUN
    FIRST_RUN = True
    close_gumps()
    global RELOG
    RELOG = False
    connection.connect()

    # set to autoreconnect in case disconnected
    # trying to fix overnight disconect and stuck bug
    SetPauseScriptOnDisconnectStatus(False)
    SetARStatus(True)

    start_cordinates = (GetX(Self()), GetX(Self()))
    initial_balance = 0

    time_char_started_macro = datetime.now()

    if len(MINE_RUNEBOOKS) == 0:
        utils.debug("Char Runebooks are not configured! Exiting...")
        exit()

    if Dead():
        utils.debug("Char started macro dead. Trying to ress")
        ress.ress()
        # NOTE: check if this wont affect config that actually use robes
        remove_death_robe()

        if not is_set_equiped():
            dress_char_set()
            save_char_set()

    check_jail()
    check_tithe()

    if GetHP(Self()) < GetMaxHP(Self()):
        utils.heal_self_until_max_hp()
    # get char initial bank balance
    # initial_balance = 0
    # if confirm_script_loop_conditions():
    #     initial_balance = common.get_current_bank_balance()
    #     utils.debug("Initial bank balance: %d" % (initial_balance))
    # else:
    #     initial_balance = 0

    while True:

        utils.debug("while true")
        if Dead():  
            if RELOG == False:
                Disconnect()
                Connect() 
                RELOG = True
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
            RELOG = False
            CURRENT_BALANCE = initial_balance
            amount_of_checks_in_bank = 0
            remove_death_robe()
            
            check_tithe()
            if not utils.is_mounted(char): 
                find_pet_on_ground(PET)
            insurance.is_set_insured()
            check_jail()
            check_tithe()

            if not utils.is_set_equiped():
                utils.dress_char_set()
                utils.save_char_set()

            if not utils.count(SHOVEL):
                utils.debug("** NO SHOVELS ** Going to make Shovels.")
                # if ORE_STORAGE_CONTAINER:
                #     if GetDistance(ORE_STORAGE_CONTAINER) == -1:
                #         utils.debug("Cant find resource container close.")
                recall_home()
                # else:
                # utils.debug(
                #     "Already close to restock container. Distance: %d"
                #     % (GetDistance(ORE_STORAGE_CONTAINER))
                # )
                find_and_save_ore_container_maybe()
                find_and_save_forge_maybe()
                open_storage()
                utils.wait_lag(100)
                #check_tinker_tools_on_storage(MINIMUM_TINKER_TOOLS_ON_STORAGE)
                getitems(types.TINKER_TOOLS, 1, 1, ORE_STORAGE_CONTAINER)
                make_shovels_maybe()

            for runebook in MINE_RUNEBOOKS:
                if not confirm_script_loop_conditions():
                    break
                CURRENT_RUNEBOOK = runebook
                utils.debug("TESTE RUNEBOOK %s" % (runebook))
                utils.debug("Starting another mining cycle on %s runebook" % (runebook))
                for runenumber in range(1, 17):
                    remount()
                    utils.debug("Entrou for da runa do runebook")

                    CURRENT_RUNE = runenumber
                    if not confirm_script_loop_conditions():
                        utils.debug("Saindo do loop for da runa do runebook")
                        break

                    # if char is connected for more than 1 hour, start printing uptime
                    if ConnectedTime() > time_char_started_macro + timedelta(
                        minutes=15
                    ):
                        connection.print_uptime()
                    CURRENT_RUNEBOOK = runebook

                    if GetHP(Self()) < GetMaxHP(Self()):
                        utils.heal_self_until_max_hp()

                    # ---------------------------------------------------
                    # main mine. will only loop while char is not overweighted with ores and has shovels
                    while (
                        confirm_script_loop_conditions()
                        and utils.count(SHOVEL)
                        and Weight() < WEIGHT_LIMIT
                    ):
                        utils.debug("entrou main loop das runas")

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
                                "%s died on last visit to rune %d on %s runebook. Skillping it."
                                % (char_name, runenumber, runebook)
                            )
                            break
                        else:
                            if utils.travel_to(
                                runebook, TRAVEL_SPELL, runenumber, 4000
                            ):
                                utils.wait_lag(1)
                                if not FAST_GEMS_MODE:
                                    get_ores_from_ground_maybe()
                                if TargetPresent():
                                    CancelTarget()

                                utils.debug(
                                    "Starting to mine. Weight: %s / %s"
                                    % (Weight(), MaxWeight())
                                )
                                if mine(gettiles2(1)):
                                    continue
                                else:
                                    break
                            else:
                                utils.debug(
                                    f"Failed traveling to {runenumber}. Skipping to next rune."
                                )
                                break

                    start_time = datetime.now()
                    while (
                        confirm_script_loop_conditions()
                        and utils.count(types.ORE)
                        and Weight() >= MaxWeight()
                    ):
                        utils.debug(
                            "Char is overweight with ores. Dropping some to travel."
                        )
                        amount_to_drop = Weight() - WEIGHT_LIMIT
                        utils.drop_type(types.ORE, amount_to_drop)
                        if check_timer(start_time, 30000):
                            utils.debug("30s droping ores. Fuck it, breaking.")
                            break

                    # this part is only the repetition of the bellow while, but for ecrus in FAST ECRUS mode
                    ecrus_in_backpack = utils.count(ECRU_CITRINE)
                    while FAST_GEMS_MODE and ecrus_in_backpack >= MAX_ECRUS_IN_BACKPACK:
                        utils.debug(
                            "Char has %d Ecrus in backpack. Going to unload it."
                            % (ecrus_in_backpack)
                        )
                        # if FORGE and GetDistance(FORGE) == -1:
                        #     utils.debug("Cant find resource container close.")
                        recall_home()
                        # else:
                        unload()
                        upload()
                        unload()
                        smelt_ores()
                        return_to_previous_mine_spot()
                        if not FAST_GEMS_MODE:
                            get_ores_from_ground_maybe()
                        if not mine(gettiles2(1)):
                            utils.debug("Mining failed.")
                            break

                    # ---------------------------------------------------
                    # char is overweighted but doenst have any more logs in bag, go sell
                    # add final maxweight condition to avoid travlling overweighted
                    while (
                        confirm_script_loop_conditions()
                        and utils.count(types.ORE)
                        and Weight() >= WEIGHT_LIMIT
                        and Weight() <= MaxWeight()
                    ):
                        utils.debug(
                            "Char is over the weight limit. Going home to unload"
                        )

                        # if droping stuff allows lowers weight bellow the limitf, we can mine again, so break
                        drop_special_resources_on_ground_maybe()
                        # if Weight() <= WEIGHT_LIMIT:
                        #     utils.debug(
                        #         "Char is underweight again. Aborting going home and continue mining."
                        #     )
                        #     break

                        check_tithe()
                        # if (
                        #     ORE_STORAGE_CONTAINER
                        #     and GetDistance(ORE_STORAGE_CONTAINER) == -1
                        # ):
                        #     utils.debug("Cant find resource container close.")
                        recall_home()
                        # else:
                        # utils.debug("Already close to restock container.")
                        unload()
                        upload()
                        unload()
                        combine_ore_piles()
                        return_to_previous_mine_spot()
                        if not FAST_GEMS_MODE:
                            get_ores_from_ground_maybe()
                        if not mine(gettiles2(1)):
                            utils.debug("Mining failed.")
                            break

                    # ---------------------------------------------------
                    # char is overweighted with other stuff thats not mining materials
                    # ex: logs from the mine macro, gold, etc..
                    while (
                        confirm_script_loop_conditions()
                        and not utils.count(types.ORE)
                        and Weight() >= WEIGHT_LIMIT
                    ):
                        utils.debug("Char is overweight without ores. Maybe ingots?")
                        recall_home()
                        unload()
                        upload()
                        unload()

            utils.debug("finished another runebook")
            utils.wait_lag(10)