from modules.common_utils import *
from modules.regions import *
from modules import *
from modules.spell_utils import cast_self
from datetime import datetime, timedelta
from random import randrange
from py_stealth import (
    CastToObj,
    Wait,
    IsDead,
    UseType,
    WaitForTarget,
    TargetToObject,
    GetMana,
    Self,
    GetMaxHP,
    GetHP,
    IsPoisoned,
    FindTypesArrayEx,
    GetDistance,
    IsObjectExists,
    IsHidden,
    GetFindedList,
    SetFindDistance,
    SetFindVertical,
    IsTrade,
    GetTradeContainer,
    TradeCount,
    GetTradeOpponent,
    GetTradeOpponentName,
    FindType,
    UOSay,
    CancelTrade,
    ConfirmTrade,
    GetType,
    Backpack,
    FindItem,
    UseObject,
    MoveItem,
    GetTooltip,
    StealthPath,
    GetClilocByID,
)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/951998293464981564/IAWIizZlJ1Kc6GTJswM3i6UjVaOThwhdZ82jBvvprYT1Ixmm5WnemHVfw5CXf_uqaAuG"
PRIVATE_MODE = False
PLAYERS = [
    0x0009AF6A, 0x21441, 0xa8465, 0x9af6a, 0x5fe72, 0x11fe28, 0x80285, 0xb6ea9, 0xa8465, 0x3df2a, 0xa72bb, 0x3b10b, 0x3e336, 0x17ad, 0xfc6a9, 0x54a53, 0x7173c, 0x120587, 0x21441, 0xbe78e, 0x66144, 0x31b92, 0xc1132, 0xad741, 0x1b40f9, 0x1b40f9, 0x10b10c, 0x8ba9e, 0x82a, 0xd9d5c, 0xabce3, 0x140513, 0x94715, 0x1282d5, 0x458c4, 0x133a62, 0x5c9d0, 0x7173c, 0x82d14, 0x9a19c, 0x000D0AE4, 0xbe78e, 0x00036827, 0x1810e0, 0x1adc1c, 0x4670d, 0x1adc1c
]
PETS = [
  0x1b18d8, 0x000BC6AB, 0x154f51, 0xfe661, 0x00065E68, 0xb58ba, 0x14f1e3, 0x8ee, 0x127847, 0x609ee, 0xcc , 0x31f, 0x36827, 0x7cb8, 0x1105d5, 0x54c9a, 0x00036827, 0xd987b, 0x1c4a90, 0xe822e, 0x8e994, 0x187e43, 0x47f05
]

COMMANDS = [
    "BandageCount",  # bandage count
    "SawCount",  # saw count
    "SewingKitCount",  # se
    "RepairCount",  # sdsff
    "Uptime",  # sdsff
    "JailCount",
    "WhoAreYou",
]


def get_who_am_i_msgs():
    WHO_AM_I_MSGS = [
        "Im Helper Bot. Nice to meet you, player",
        "A guy trying to help you get back to PvP.",
        "I am (Bot error: 'Cant reveal Master's name')",
        "Who wants to know?",
        "I am EOS",
        "I am Selene",
        "I am the alpha and the omega",
        "I am your friendly neighbour resser bot",
        "I am the guy you dont wanna mess with if you want your pet ressed to get back to PvP fast.",
        "Really? I mean, really??",
        "I am you.",
    ]
    return WHO_AM_I_MSGS


COMMANDS_TO_SEARCH = ""
for commandd in COMMANDS:
    if COMMANDS_TO_SEARCH == "":
        COMMANDS_TO_SEARCH = commandd
    else:
        COMMANDS_TO_SEARCH = COMMANDS_TO_SEARCH + "|" + commandd
COMMANDS_TO_SEARCH = "bot help|" + COMMANDS_TO_SEARCH


# timers
global PET_RESS_MSG_TIMER
PET_RESS_MSG_TIMER = datetime.now()
global HELP_MSG_TIMER
HELP_MSG_TIMER = datetime.now() - timedelta(minutes=2)

carp_type = [0x0E89, 0x0DF0]
skit_type = 0x0F9D
saw_type = 0x1034
tink_type = 0x1EB8
wait_time = 500  # Default Wait Time
wait_lag_time = 10000  # Default Wait Lag Time
action_wait = 500


def wait_lag(wait_time=wait_time, lag_time=wait_lag_time):
    Wait(wait_time)
    CheckLag(lag_time)
    return


def in_gump(text, value=999):
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
                # debug("HTML")
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
                # debug("HTML color")
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
                # debug("text")
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


def listen_to_trade():
    pendingTrade = True
    item_type = 0
    if IsTrade():
        tradeContainer = GetTradeContainer(TradeCount() - 1, 2)
        player_trading = GetTradeOpponent(TradeCount() - 1)
        player_trading_name = GetTradeOpponentName(TradeCount() - 1)
        FindType(0xFFFF, tradeContainer)
        items_in_trade = GetFindedList()
        if len(items_in_trade) > 1:
            UOSay("Ill fix your (carpentry item), wait a while...")
            CancelTrade(TradeCount() - 1)
            return False, False, False, False
        foundType = GetType(items_in_trade[0])
        if foundType in carp_type:
            FindType(saw_type, Backpack())
            if not FindItem():
                UOSay("Sorry but i don have any saws atm to fix that")
                CancelTrade(TradeCount() - 1)
                return False, False, False, False
            UOSay("vou arrumar esse taco")
        else:
            FindType(skit_type, Backpack())
            if not FindItem():
                UOSay("sem seweing kits, desculpe")
                CancelTrade(TradeCount() - 1)
                return False, False, False, False
            UOSay("Ill fix your Tailoring item, wait a while...")
        ConfirmTrade(TradeCount() - 1)

        while pendingTrade is True:
            foundTradeWithPlayer = False
            #debug("Waiting for you to confirm trade...")
            for i in range(TradeCount()):
                #debug(GetTradeOpponentName(i))
                if GetTradeOpponent(i) == player_trading:
                    foundTradeWithPlayer = True
            if foundTradeWithPlayer is False:
                pendingTrade = False
            Wait(100)

        UOSay(
            "Wait ... " + str(player_trading_name) + " while i fix your item for you..."
        )
        return player_trading, player_trading_name, items_in_trade[0], foundType
    return False, False, False, False


def fix_item(item_id, fix_type):
    fixed = False
    starttime = datetime.now()
    while fixed is False:
        if fix_type == "tailor":
            FindType(skit_type, Backpack())
            UseObject(FindItem())
            wait_gump_and_press_btn(0x38920ABD, 42, 5)
            wait_lag(500)
            WaitTargetObject(item_id)
            wait_lag(500)
        if fix_type == "carpenter":
            FindType(saw_type, Backpack())
            UseObject(FindItem())
            wait_gump_and_press_btn(0x38920ABD, 42, 5)
            wait_lag(500)
            WaitTargetObject(item_id)
            wait_lag(500)

        # debug(InGump("You repair the item"))
        # debug(InGump("item is in full repair"))
        # debug(InGump("item cannot be repaired"))
        # debug(InGump("has been repaired many times"))
        if in_gump("You repair") is not None:
            wait_gump_and_press_btn(0x38920ABD, 0, 1)
            fixed = True
            break
        if in_gump("item cannot be repaired") is not None:
            wait_gump_and_press_btn(0x38920ABD, 0, 1)
            return False
        if in_gump("item is in full repair") is not None:
            wait_gump_and_press_btn(0x38920ABD, 0, 1)
            return False
        if in_gump("has been repaired many times") is not None:
            UOSay("poderá quebrar, coloque pownder primeiro")
            wait_gump_and_press_btn(0x38920ABD, 0, 1)
            return False
        if in_gump("You fail to repair the item") is not None:
            wait_gump_and_press_btn(0x38920ABD, 0, 1)
            return False

        wait_gump_and_press_btn(0x38920ABD, 0, 1)
        #debug("Tentando consertar")
        Wait(1000)
        if datetime.now() >= starttime + timedelta(seconds=60):
            #debug("SECURITY BREAK FIXING!!")
            return True
    return True


def return_item(item_id, player_trading, player_trading_name):
    item_type = GetType(item_id)
    listOfPlayers = find_players()
    foundPlayer = False
    foundItem = False

    for player in listOfPlayers:
        if player == player_trading:
            foundPlayer = True
            break
    if not foundPlayer:
        UOSay(
            "O Player desapareceu ("
            + str(player_trading_name)
            + ') não consigo devolver o item! Você sabe como me achar, fique tranquilo seu item está seguro"'
        )
        return False

    MoveItem(item_id, 65000, player_trading, 0, 0, 0)
    UOSay("obrigado, muchas gracias, ty" + str(player_trading_name))
    wait_lag(200)
    while TradeCount() > 0:
        #debug("esperando player aceitar o trade")
        for i in range(TradeCount()):
            if GetTradeOpponent(i) == player_trading:
                tradeContainerToMe = GetTradeContainer(i, 2)
                FindType(0xFFFF, tradeContainerToMe)
                items_in_trade = GetFindedList()
                if len(items_in_trade) == 0:
                    tradeContainerFromMe = GetTradeContainer(i, 1)
                    FindType(item_type, tradeContainerFromMe)
                    foundss = GetFindedList()
                    for itemFound in foundss:
                        if itemFound == item_id:
                            ConfirmTrade(i)
                            foundItem = True
                            break
                    if foundItem is False:
                        UOSay(
                            "Algo deu errado! ("
                            + str(player_trading_name)
                            + ") fique tranquilo, seu item está seguro"
                        )
                        CancelTrade(i)
                        return False
                else:
                    UOSay(
                        "Algo deu errado! ("
                        + str(player_trading_name)
                        + ") fique tranquilo, seu item está seguro"
                    )
                    CancelTrade(i)
                    return False
        Wait(100)
    return True


def handle_trade():
    player_trading, player_trading_name, item_id, item_type = listen_to_trade()
    if player_trading is not False:
        if item_type in carp_type:
            fix_type = "carpenter"
        else:
            fix_type = "tailor"
        fix_item(item_id, fix_type)

        tooltip = GetTooltip(item_id)
        repairLog = open(
            StealthPath() + "/Scripts/repairLog.txt".format(datetime.today()), "a+"
        )
        repairLog.writelines(
            "{0} | {1} | {2} | ID:{3} | TOOLTIP: {4} \n".format(
                player_trading_name, fix_type, str(datetime.now()), item_id, tooltip
            )
        )
        repairLog.close()

        return_item(item_id, player_trading, player_trading_name)


def send_char_position():
    request_position_msg = "resser pos"
    if InJournal(request_position_msg) > 0:
        UOSay("\ POSITION -> | %d | %d" % (GetX(char), GetY(char)))
        ClearJournal()


def get_bandages_from_ground():
    bandage_initial_count = count(BANDAGE_TYPE)
    if FindType(BANDAGE_TYPE, Ground()):
        bandages = FindItem()
        Grab(bandages, 999)
        wait(1000)
        if bandage_initial_count == 0:
            UOSay("Thank you for the bandages! I can start ressing pets again now...")
        else:
            UOSay("Thank you for the bandages!")


def check_status(mob):
    global PET_RESS_MSG_TIMER
    mob_name = GetName(mob)
    if IsDead(mob):
        # while mob is far, warn and ask to get closer
        if GetDistance(mob) > 1:
            if check_timer(PET_RESS_MSG_TIMER, 5000):
                PET_RESS_MSG_TIMER = datetime.now()
                msg = ""

                # set the msg depending if its player or pet, if its in luna or not
                if is_player_ghost(mob):
                    if in_region("luna_moongate"):
                        msg = f"Hey {mob_name}, come closer and ill ress you"
                    else:
                        msg = f"\ Get closer to me, {mob_name}, ill ress you"
                else:
                    if count(BANDAGE_TYPE) == 0:
                        msg = f"Psst! I could ress {mob_name} if you give me some bandages or drop some on the ground for me to get..."
                        get_bandages_from_ground()

                    if in_region("luna_moongate"):
                        msg = f"Hey! Want a pet ress? Bring {mob_name} closer to me."
                    else:
                        msg = f"\ {mob_name} is not close enough to ress. Get closer..."

                UOSay(msg)

        # if mob is within ressing range, try to ress it
        start_time = datetime.now()
        while not Dead() and Connected() and IsDead(mob) and GetDistance(mob) <= 1:
            msg = ""
      

            # ress with spell of bandage depending if its player or pet
            if is_player_ghost(mob):
                UOSay(f"\ Trying to ress {mob_name} ")
                CastToObj("Resurrection", mob)
                Wait(4000)
            else:
                bandage_count = count(BANDAGE_TYPE)
                if bandage_count == 0:
                    msg = f"I could ress {mob_name} if drop some bandages on the ground for me to get..."
                    get_bandages_from_ground()
                    break

                if in_region("luna_moongate"):
                    msg = f"Trying to ress pet {mob_name} ({bandage_count} bandages left)..."
                else:
                    msg = f"\ Trying to ress pet {mob_name} ({bandage_count} bandages left)..."

                UOSay(msg)
                if GetHP(mob) == 0:
                    UseType2(BANDAGE_TYPE)
                    WaitTargetObject(mob)
                    Wait(3000)

    else:
        if IsPoisoned(mob) and GetMana(Self()) >= 8:
            #debug("Curing %s" % (mob_name))
            last_action = datetime.now()
            CastToObj("Arch Cure", mob)
            Wait(2850)
        elif GetHP(mob) < GetMaxHP(mob) * 0.8:
            UOSay(
                "\ Healing %s | HP: %d / %d" % (mob_name, GetHP(char), GetMaxHP(char))
            )
            CastToObj("Greater Heal", mob)
            Wait(2850)
        # elif not IsHidden(player):
        #     debug("Hiding %s" % (player_name))
        #     CastToObj("Invisibility", player)
        #     Wait(2850)


def listen_to_commands():
    global HELP_MSG_TIMER
    starttime = datetime.now() - timedelta(seconds=1)
    if check_timer(HELP_MSG_TIMER, 800000):
        HELP_MSG_TIMER = datetime.now()
        #UOSay("Hello! I'm a official announcer O guild.")
        #AddToSystemJournal("Hello! I'm a official announcer O guild.")
        #UOSay("I am EOS")
        #AddToSystemJournal("I am EOS")
        # UOSay("***I'm taking a break***")
    # if (InJournal(COMMANDS_TO_SEARCH) > -1):
    # if InJournalBetweenTimes(COMMANDS_TO_SEARCH, starttime, datetime.now()) > -1:
    if InJournal(COMMANDS_TO_SEARCH) > -1:
        ClearJournal()
        msgText = Journal(LineIndex())
        print(msgText)
        regexSearch = re.search("(.*):.*(" + COMMANDS_TO_SEARCH + ").*", msgText)
        # print(regexSearch)
        # print(regexSearch.group(1))
        # print(regexSearch.group(2))
        if regexSearch is not None and regexSearch.group(1) != CharName():
            print(regexSearch.group(0))
            answer_command(regexSearch.group(2))

    # Wait(2000)
    # starttime = datetime.now() - timedelta(seconds=2)


def answer_command(command):
    cmds = ""
    if command == "BotHelp" or command == "bot help":
        UOSay(
            "I can: Heal, Cure, Ress, Ress your pet and Repair (Carp/Taylor) items for you (just trade then with me)"
        )
        Wait(2000)
        UOSay("I have the following commands:")
        for i in COMMANDS:
            if not cmds:
                cmds = i
            else:
                cmds = cmds + ", " + i
        UOSay(cmds)
        UOSay(
            'If you have any problems or suggestions, contact me on Discord "UOHelperBot#6983"'
        )
        return
    if command == "WhoAreYou":
        msgs = get_who_am_i_msgs()
        UOSay(msgs[randrange(len(msgs))])
        starttime = datetime.now() - timedelta(seconds=1)
        Wait(2000)

    try:
        if command == "RepairCount":
            UOSay(f"I have have been online since {ConnectedTime()}")

        if command == "RepairCount":
            num_lines = 0
            try:
                num_lines = sum(
                    1 for line in open(StealthPath() + "/Scripts/repairLog.txt")
                )
            except:
                pass
            UOSay(f"I have repaired a total of {num_lines} items since 08/14/2020.")

        if command == "RessCount":
            num_lines = 0
            try:
                num_lines = sum(
                    1 for line in open(StealthPath() + "/Scripts/ressLog.txt")
                )
            except:
                pass
            UOSay(f"I have ressed a total of {num_lines} players since 08/14/2020.")

        if command == "PetRessCount":
            num_lines = 0
            try:
                num_lines = sum(
                    1 for line in open(StealthPath() + "/Scripts/petRessLog.txt")
                )
            except:
                pass
            UOSay(f"I have ressed a total of {num_lines} pets.")

        if command == "JailCount":
            num_lines = 0
            try:
                num_lines = sum(
                    1 for line in open(StealthPath() + "/Scripts/jailhelperbot.txt")
                )
            except:
                pass
            if num_lines == 0:
                UOSay("HEY!! I haven't be in jail yet! Thanks GMs!")
            else:
                UOSay(f"I have been in jail {num_lines} times since 08/14/2020.")

        if command == "BandageCount":
            qtd = count(BANDAGE)
            UOSay(f"I have {qtd} Bandages.")

        if command == "SawCount":
            qtd = count(SAW_TYPE)
            founds = GetFindedList()
            tool_uses_remaining = 0
            for itemFound in founds:
                tooltip = GetTooltip(itemFound)
                print(tooltip)
                regexSearch = re.search("uses\s+remaining:\s+(\d+).*", tooltip)
                if regexSearch is not None:
                    tool_uses_remaining = tool_uses_remaining + int(
                        regexSearch.group(1)
                    )
            UOSay(f"I have {qtd} Saws, and can do {tool_uses_remaning} repairs.")

        if command == "SewingKitCount":
            qtd = count(SEWINGKIT_TYPE)
            founds = GetFindedList()
            remainingCount = 0
            for itemFound in founds:
                tooltip = GetTooltip(itemFound)
                regexSearch = re.search("uses\s+remaining:\s+(\d+).*", tooltip)
                if regexSearch is not None:
                    remainingCount = remainingCount + int(regexSearch.group(1))
            UOSay(f"I have {qtd} Sewing kits, and can do {remainingCount} repairs.")
    except:
        pass

def start():
    print("Bot will answer to the following commands:")
    print(COMMANDS_TO_SEARCH)
    while True:
        if Dead():
            send_discord_message(
                DISCORD_WEBHOOK_URL, f"**RESSER DEAD** Resser bot {char_name} is dead!"
            )
            while Dead():
                wait_and_accept_ress()

        while not Dead() and Connected():
            listen_to_commands()
            if not IsRunning(char) and Poisoned() or GetHP(char) < GetMaxHP(char) * 0.9:
                mage_mini_heal()
            if not IsRunning(char) and Poisoned() or GetHP(char) < GetMaxHP(char) * 0.5:
                mage_big_heal()

            if in_region("luna_moongate"):
                distance = 20
            else:
                distance = 2

            mobs_nearby = get_nearby_mobs(distance, [], [1, 2, 3, 4, 5, 6], False)
            if len(mobs_nearby) > 0:
                for mob in mobs_nearby:
                    # if not has_mobs_nearby(4):
                    check_status(mob)
                    # else:
                    #     debug("Esperando mobs proximos se afastarem")
            if (
                not in_region("luna_moongate")
                and not in_region("doom_safe_room")
                and not in_region("vendor_mall")
            ):
            
                while not Hidden():
                    UseSkill("hiding")
                    Wait(1000)
                send_char_position()
            handle_trade()

            get_bandages_from_ground()


if __name__ == "__main__":
    ClearSystemJournal()
    #debug("RESSER BOT")
    #debug("by gugutz")
    start()