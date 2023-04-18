# =======================================================================
# AFK GUMP SETTINGS
# =======================================================================
from datetime import datetime
import json

# requests
try:
    import requests
except ModuleNotFoundError:
    print("No 'requests' module found.\n Install it using 'pip install requests' ")
    exit()

from modules.common_utils import debug
from modules.gumps import in_gump, waitgumpid_textentry, wait_gump_and_press_btn
import modules.gumps as gumps


DEMISE_AFK_GUMP_IDS = [
    0xC37345F3,
    0xB3601A01,
    0xC8485931,
]

GUMP_DEBUG_LOG = "/Scripts/gump-debug.txt"
RESPOND_AFK_GUMP = True

# AFK_ANSWER_API_URL = "http://150.136.251.245:5000/resolveAFKGump"
AFK_ANSWER_API_URL = "https://uo-api.herokuapp.com/resolve-afk-gump"


def is_afk_gump():
    if IsGump():
        id = GetGumpID(GetGumpsCount() - 1)
        if id in DEMISE_AFK_GUMP_IDS:
            return True
        # elif OUTLANDS_AFK_GUMP_IDS:
        #     if id in OUTLANDS_AFK_GUMP_IDS:
        #         return True
        elif gumps.in_gump("Enter verification code"):
            return True
        # uo outlands says captcha on the gump
        elif gumps.in_gump("Captcha"):
            debug("Detectou AFK por 'Captcha' escrito no gump")
            return True
        elif gumps.in_gump("Type the Value"):
            debug("Detectou AFK por 'Type the Value' escrito no gump")
            return True
        else:
            return False

    return False


def get_last_gump_id():
    return GetGumpInfo(GetGumpsCount() - 1)


def solve_afk_gump():
    # debug("Gumps Count:" + str(GetGumpsCount()))
    # debug("Gump Id:" + str(id))
    gump_info = get_last_gump_id()
    gump_debug_log = open(StealthPath() + GUMP_DEBUG_LOG, "a+")
    gump_debug_log.writelines(
        f"\n\n\n------GUMP FOUND 1! Char: {CharName()}\n ----------"
    )
    gump_debug_log.writelines("\n-------" + str(datetime.now()) + "-------\n")
    json.dump(gump_info, gump_debug_log)

    gumpFullLines = GetGumpFullLines(GetGumpsCount() - 1)
    gump_debug_log.writelines("\n-------FULL LINES-------\n")
    json.dump(gumpFullLines, gump_debug_log)
    for gump in range(GetGumpsCount() - 1):
        idd = GetGumpID(gump)

        gump_debug_log.writelines("\n-------ID - for-------\n")
        gump_info = GetGumpInfo(gump)
        json.dump(gump_info, gump_debug_log)

        gumpFullLines = GetGumpFullLines(gump)
        gump_debug_log.writelines("\n-------FULL LINES - for-------\n")
        json.dump(gumpFullLines, gump_debug_log)

    gump_debug_log.close()

    # TRYING TO PRESS CHECKBOX
    debug("PRESSING CHECKBOX")
    Wait(2000)  # waiting 2 seconds just to pretend
    button = gump_info["GumpButtons"][0]["ReturnValue"]
    gumps.wait_gump_and_press_btn(id, int(button), True, 5)
    # Wait (600000) # Wait for 10 Minutes

    Wait(4000)
    gump_info = GetGumpInfo(GetGumpsCount() - 1)
    Wait(1000)
    print("Got new Gump Info")
    # print(gump_info)
    gump_debug_log = open(StealthPath() + GUMP_DEBUG_LOG, "a+")
    # print(gump_info)
    gump_debug_log.writelines(
        f"\n\n\n------GUMP FOUND 2! Char: {CharName()}\n ----------"
    )
    gump_debug_log.writelines("\n-------" + str(datetime.now()) + "-------\n")
    json.dump(gump_info, gump_debug_log)
    gump_debug_log.close()

    # print("Getting CAPTCHA!")
    retry = 0
    captcha_response = ""
    while not captcha_response.isdigit():
        print("Trying to solve CAPTCHA for the %d TIME!!" % (retry))
        try:
            captcha_response = requests.post(
                url=AFK_ANSWER_API_URL, data=json.dumps(gump_info)
            )
            captcha_response = captcha_response.text
        except:
            captcha_response = "FALHOU! :(. Vai tentar de novo"
        retry += 1
        print(f"RESPONSE FROM API: {captcha_response}")
        if retry > 5:
            print("****TOO MANY RETRIES TRYING TO SOLVE GUMP! BREAKING!***")
            break
        if not IsGump():
            print("Não achou gump enquanto pegava resposta da API. Sair da função.")
            return

        Wait(1234)
    if retry <= 5:
        gumps.waitgumpid_textentry(id, 1, captcha_response, 5)
        print("AFTER ENTRYING TEXT!!")
        Wait(4300)
        gumps.wait_gump_and_press_btn(id, 1, True, 5)
        print("AFTER PRESSING OKAY BUTTON!!")
    else:
        gumps.waitgumpid_textentry(id, 1, "00", 5)
        print("Answered '00' on purpose to try to change the gump")
        Wait(4300)
        gumps.wait_gump_and_press_btn(id, 1, True, 5)


# def checkGMGump(charFunction=""):
#     global GMGumpFound
#     global GMGumpAnswered
#     if IsGump():
#         captcha_response = ""
#         print("IsGump")
#         print(GetGumpID(GetGumpsCount() - 1))
#         # print(GetGumpInfo(GetGumpsCount() - 1))
#         if GetGumpsCount() > 0:
#             id = GetGumpID(GetGumpsCount() - 1)
#             # if id in DEMISE_AFK_GUMP_IDS or id in OUTLANDS_AFK_GUMP_IDS:
#             if id in DEMISE_AFK_GUMP_IDS:
#                 if PLAY_SOUNDS:
#                     try:
#                         PlayWav(ALARM_SOUND)
#                     except:
#                         pass
#                 if GMGumpFound is not True:
#                     debug("#### FOUND AFK GUMP ######")
#                     if SEND_DISCORD_AFK_WARNINGS:
#                         send_discord_message(
#                             DISCORD_WEBHOOK_AFK_URL, DISCORD_WEBHOOK_AFK_MSG
#                         )

#                 debug("Gumps Count:" + str(GetGumpsCount()))
#                 # id = GetGumpID(GetGumpsCount()-1)
#                 debug("Gump Id:" + str(id))
#                 # gumpFullInfo = GetGumpFullInfo(GetGumpsCount()-1)
#                 gump_info = GetGumpInfo(GetGumpsCount() - 1)
#                 # with open('gump-debug.txt','w') as file:
#                 gump_debug_log = open(StealthPath() + GUMP_DEBUG_LOG, "a+")
#                 # print(gump_info)
#                 gump_debug_log.writelines(
#                     "\n\n\n---------------GUMP FOUND! Char:"
#                     + str(CharName())
#                     + "----------------"
#                 )
#                 gump_debug_log.writelines(
#                     "\n-------" + str(datetime.now()) + "-------\n"
#                 )
#                 json.dump(gump_info, gump_debug_log)

#                 gumpFullLines = GetGumpFullLines(GetGumpsCount() - 1)
#                 # print(gumpFullLines)
#                 gump_debug_log.writelines("\n-------FULL LINES-------\n")
#                 json.dump(gumpFullLines, gump_debug_log)
#                 for gump in range(GetGumpsCount() - 1):
#                     idd = GetGumpID(gump)

#                     gump_debug_log.writelines("\n-------ID - for-------\n")
#                     gump_info = GetGumpInfo(gump)
#                     json.dump(gump_info, gump_debug_log)

#                     gumpFullLines = GetGumpFullLines(gump)
#                     gump_debug_log.writelines("\n-------FULL LINES - for-------\n")
#                     json.dump(gumpFullLines, gump_debug_log)

#                 gump_debug_log.close()

#                 if RESPOND_AFK_GUMP:
#                     # TRYING TO PRESS CHECKBOX
#                     Wait(1000)  # waiting 2 seconds just to pretend
#                     debug("PRESSING CHECKBOX")
#                     button = gump_info["GumpButtons"][0]["ReturnValue"]
#                     wait_gump_and_press_btn(id, int(button), True, 5)
#                     # Wait (600000) # Wait for 10 Minutes

#                     Wait(4000)
#                     gump_info = GetGumpInfo(GetGumpsCount() - 1)
#                     Wait(1000)
#                     print("Got new Gump Info")
#                     print(gump_info)
#                     gump_debug_log = open(StealthPath() + GUMP_DEBUG_LOG, "a+")
#                     # print(gump_info)
#                     gump_debug_log.writelines(
#                         "\n\n\n---------------GUMP FOUND 2! Char:"
#                         + str(CharName())
#                         + "----------------"
#                     )
#                     gump_debug_log.writelines(
#                         "\n-------" + str(datetime.now()) + "-------\n"
#                     )
#                     json.dump(gump_info, gump_debug_log)
#                     gump_debug_log.close()

#                     debug("Getting CAPTCHA!")
#                     retry = 0
#                     while not captcha_response.isdigit():
#                         debug("Trying to solve CAPTCHA for the %d TIME!!" % (retry))
#                         try:
#                             captcha_response = requests.post(
#                                 url=AFK_ANSWER_API_URL, data=json.dumps(gump_info)
#                             )
#                             captcha_response = captcha_response.text
#                         except:
#                             captcha_response = "FALHOU! :(. Vai tentar de novo"
#                         retry += 1
#                         debug("RESPONSE FROM API:" + captcha_response)
#                         if retry > 5:
#                             debug(
#                                 "****TOO MANY RETRIES TRYING TO SOLVE GUMP! BREAKING!***"
#                             )
#                             break
#                         if not IsGump():
#                             debug(
#                                 "Não achou gump enquanto pegava resposta da API. Sair da função."
#                             )
#                             return

#                         Wait(1234)
#                     if retry <= 5:
#                         waitgumpid_textentry(id, 1, captcha_response, 5)
#                         debug("AFTER ENTRYING TEXT!!")
#                         Wait(4300)
#                         wait_gump_and_press_btn(id, 1, True, 5)
#                         debug("AFTER PRESSING OKAY BUTTON!!")
#                     else:
#                         waitgumpid_textentry(id, 1, "00", 5)
#                         debug("Answered '00' on purpose to try to change the gump")
#                         Wait(4300)
#                         wait_gump_and_press_btn(id, 1, True, 5)
#             else:
#                 debug("Gump detected was NOT an AFK Gump")
#                 debug("Leaving as is...")
#                 GMGumpFound = False
#                 return False
#                 # close_gumps()
