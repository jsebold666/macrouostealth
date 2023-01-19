#############################################################################
# NPC UTILS
#############################################################################

from modules.types import HUMANOIDS
from modules.common_utils import debug, count
import modules.common_utils as utils
from modules.gumps import close_gumps
import modules.gumps as gumps
from datetime import datetime


def is_npc(mob):
    mob_name = GetAltName(mob)
    mob_noto = GetNotoriety(mob)
    NPC_NAMES = [
        "priest of mondain",
        "priest of mondain",
        "the fighter",
        "gipsy",
        "the mage",
        "the guard",
        "the holy mage",
        "the fisherman",
        "the ticket seller",
        "the alchemist",
        "the herbalist",
        "the hairstylist",
        "the keeper of chivalry",
        "the real state broker",
        "the town crier",
        "the artist",
        "the bride",
        "the healer",
        "the fisher",
        "the architect",
        "the bowyer",
        "the carpenter",
        "the tinker",
        "the blacksmith",
        "the noble",
    ]
    for name in NPC_NAMES:
        if mob_name.lower().find(name) > 0:
            return True

    return False


# search for an array of possible npcs
def find_npc_types(npc_types_array, range_to_search=20):
    npc = ""
    for npc_type in npc_types_array:
        npc = find_npc_type(npc_type, range_to_search)
        if npc:
            return npc

    return False


def buy_item_from_npc(npc_id, item_type, ammount_to_buy=1):
    AutoBuy(item_type, 0, ammount_to_buy)
    wait_lag(1000)
    SetContextMenuHook(npc_id, 2)
    wait_lag(1000)
    RequestContextMenu(npc_id)
    wait_lag(1000)
    # reset context and autobuy
    SetContextMenuHook(0, 0)
    AutoBuy(0, 0, 0)


def find_vendor(vendor_profession, range_to_search=20):
    return find_npc_type(vendor_profession, range_to_search)


def find_npc(npc_profession, range_to_search=20):
    return find_npc_type(npc_profession, range_to_search=20)


def find_npc_type(npc_profession, range_to_search=20):
    SetFindDistance(range_to_search)
    SetFindVertical(5)

    npcs_found = []
    if FindTypesArrayEx(HUMANOIDS, [0xFFFF], [Ground()], False):
        # if FindNotoriety(-1, 1):
        npcs_found += GetFindedList()

    if len(npcs_found) > 0:
        start_time = datetime.now()
        for npc in npcs_found:
            vendor_name = GetAltName(npc).lower()
            # utils.debug("name %s" % (vendor_name))
            # utils.debug("profession %s" % (npc_profession))
            if vendor_name.lower().find(npc_profession.lower()) > 0:
                utils.debug("NPC %s found: %s" % (npc_profession, vendor_name))
                return npc
            # else:
            #     Ignore(found)

        if checkTimeThreshold(start_time, 6000):
            start_time = datetime.now()
            print(
                "Timeout 8s waiting to find vendor %s. Breaking..." % (npc_profession)
            )
            return False
    # else:
    #     print("Couldnt find any NPCs around...")

    return False


def is_char_at_vendor(vendor_type):
    SetFindDistance(25)

    if FindTypesArrayEx(HUMANOIDS, [0xFFFF], [Ground()], False):
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


def sell_item_to_npc(item_type, npc_id, qtd=999, sell_btn_position=2):
    start_time = datetime.now()
    AutoSell(item_type, 0, qtd)
    SetContextMenuHook(npc_id, sell_btn_position)

    # only sells common items with color 0
    while utils.count(item_type):
        RequestContextMenu(npc_id)
        utils.wait_lag(600)
        if utils.check_timer(start_time, 10000):
            print("Timeout trying to sell to NPC. Breaking...")
            break

    # reset context
    SetContextMenuHook(0, 0)
    # reset autosell
    AutoSell(0, 0, 0)
    gumps.close_gumps()
