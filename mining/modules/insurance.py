# =======================================================================
# INSURANCE UTILS
# =======================================================================

from datetime import datetime
from modules.common_utils import check_timer, wait_lag, CHAR_WEARABLE_LAYERS
import modules.common_utils as utils


def is_insured(item):
    tooltip = GetTooltip(item)
    if tooltip == "":
        # VAZIO. CLICAR NO ITEM UMA VEZ E AGUARDAR UM TEMPINHO
        ClickOnObject(item)
        wait_lag(100)
        tooltip = GetTooltip(item)
    tooltip_str = str(tooltip)
    if tooltip_str.find("Insured") > 0:
        return True
    else:
        return False


def is_blessed(item):
    tooltip = GetTooltip(item)
    if tooltip == "":
        # VAZIO. CLICAR NO ITEM UMA VEZ E AGUARDAR UM TEMPINHO
        ClickOnObject(item)
        wait_lag(100)
        tooltip = GetTooltip(item)
    tooltip_str = str(tooltip)
    if tooltip_str.find("Blessed") > 0:
        return True
    else:
        return False


def insure_items(item_list):
    for item in item_list:
        insure_item(item)


def insure_item(item):
    if is_insured(item) or is_blessed(item):
        print("Item already Insured or blessed")
        return False
    RequestContextMenu(char)
    SetContextMenuHook(char, 3)
    WaitForTarget(2000)
    if TargetPresent():
        WaitTargetObject(item)
        Wait(500)
        reset_context_menu()
        if TargetPresent():
            CancelTarget()
        return item


def get_total_cost_of_insurance():
    total_cost_of_insurance = 0
    SetContextMenuHook(char, 2)
    WaitGump(1000)
    RequestContextMenu(char)
    wait_lag(50)
    wait_gump_without_using_object(3465474465)

    for gump in range(GetGumpsCount()):
        idd = GetGumpID(gump)
        if idd == 3465474465:

            # gump do insurance menu
            infogump = GetGumpInfo(gump)
            total_cost_of_insurance = int(infogump["Text"][1][0])
        else:
            break
    # reset the context! important!
    SetContextMenuHook(0, 0)
    close_gumps()
    wait_lag(1)
    close_gumps()
    return total_cost_of_insurance


def is_set_insured():
    start_time = datetime.now()
    equipped_layers = []
    # its very important that suit is already equipped when char gets here
    for layer in CHAR_WEARABLE_LAYERS:
        obj = ObjAtLayer(CHAR_WEARABLE_LAYERS.get(layer))
        if obj > 0:
            item_details = GetTooltip(obj)
            while (
                not item_details
            ):  # sometimes due to lag, item info is not returned by stealth.
                ClickOnObject(obj)
                utils.wait_lag(50)
                item_details = GetTooltip(obj)
                if utils.check_timer(start_time, 10000):
                    print(
                        "Timeout trying to get item detail to check for insurance. Aborting"
                    )
                    return False
            item_details_stringified = str(GetTooltip(obj))
            item_name = GetAltName(obj)
            # print("item details")
            # print(item_details)
            # print(item_details[0])
            # print(item_details[1])
            if (
                item_details_stringified.find("Insured") < 0
                and item_details_stringified.find("Blessed") < 0
            ):
                print("Non Insured and non blessed wearable found! ")
                print("Item details: %s" % (item_details))
                print("Item name: %s" % (item_name))
                print("Blesses: %s" % (str(item_details_stringified.find("Blessed"))))
                print("Insured: %s" % (str(item_details_stringified.find("Insured"))))
                return False
    return True


BLESSED_ARTIFACTS = [
    "Enourmous Venus Flytrap",
    "Undertaker's Staff",
]

REPLICAS = [
    0x1413,  # Gladiator's CollaR
    0x1540,  # Crown of Tal'Keesh
    0x1F03,  # ROBE (pode ser de cold, de fire, de physical)
    0x2684,  # Hooded (MKP, ARI, OAK LEAF)
    0x170B,  # Bota de INT
    0x1F0B,  # Orc Helm
    0x1541,  # Sash
    0x171B,  # Captain johns hat
    0x13FF,  # Brave Knight Of the Britannia
]


def get_replicas_in_backpack():
    FindTypesArrayEx(REPLICAS, [0xFFFF], [Backpack()], False)
    items_found = GetFindedList()
    replicas = []
    if len(items_found) > 0:
        for item in items_found:
            item_name = get_item_name(item)
            if item_name.lower().find("Replica".lower()) > 0:
                debug("Found %s replica" % (item_name))
                replicas.append(item)
    if len(replicas) > 0:
        return replicas

    return None


LTOTS = [
    0x2D32,  # blade dance
    0x1F04,  # robe of the equinoxx
    0x2FB8,  # brightsight lenses
    0x27A2,  # the destroyer
    0xEFF,  # pigments of tokuno
    0x2853,  # Honorable Swords of Akira
    0x27A5,  # hanzos bow
    0x2805,  # Flute of Renewal
    0x2708,  # Ancient Farmer's Kasa
    0x2D33,  # Soulseeker
    0x2D35,  # Righteous Anger
    0x493C,  # grifous statue
    0x2D21,  # flesh ripper
    0x277A,  # leorocians mempo´s of fortunes
    0x2FB7,  # quiver of elements
    # 0x09B5, # bright coloured eggs
    0x2792,  # gloves of the sun
    0x2788,  # legs of stability
    0x27A3,  # pilfered dancer fans
    0x1F03,  # robes of eclipse and equinox
    0x2D1E,  # wildfire bow
    0x2B6E,  # aegis of grace
    0x4C22,  # horse painting
    0x13F8,  # undertaker´s staff (this is blessed!)
    0x2785,  # daymos helm
    0x2D34,  # talon bite
    0x42BA,  # dying plant
    0x2D23,  # raed´s glory
]


def get_ltots_in_backpack():
    FindTypesArrayEx(LTOTS, [0xFFFF], [Backpack()], False)
    ltots = GetFindedList()
    if len(ltots) > 0:
        return ltots
    else:
        return []


def insure_ltots_maybe():
    ltots_in_backpack = get_ltots_in_backpack()
    if len(ltots_in_backpack) > 0:
        for found in ltots_in_backpack:
            ltot_type = GetType(found)
            ltot_color = GetColor(found)
            if ltot_type == "":
                # VAZIO. CLICAR NO ITEM UMA VEZ E AGUARDAR UM TEMPINHO
                ClickOnObject(found)
                wait_lag(100)
                ltot_type = GetType(found)
                ltot_color = GetColor(found)
            if ltot_type == ROBE_TYPE and ltot_color == DEATH_ROBE_COLOR:
                break
            if ltot_type in LTOTS:
                if not is_insured(found):
                    ltot_name = get_item_name(found)
                    if ltot_name in BLESSED_ARTIFACTS:
                        return
                    if not is_blessed(found):
                        print(
                            "### LTOT! ##### Non Insured and non blessed wearable found: %s"
                            % (ltot_name)
                        )
                        if insure_item(found):
                            print("INSURED ITEM %s!" % (ltot_name))
                            return found
