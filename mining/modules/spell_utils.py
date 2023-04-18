from datetime import datetime, timedelta
from py_stealth import *
import json
from pprint import pprint
import requests
import os
import statistics
import math

try:
    from modules.common_utils import *
    import modules.common_utils
except Exception as err:
    print("Error importing common_utils: %s" % (err))
    exit()


# import six; reload(six)
# from discord_webhook import DiscordWebhook

char = Self()
charLMC = 22
charFCR = 3
# BE CONSERVATIVE!
rtt_latency = 160
security_margin = 20  # scurity margin in miliseconds

DEFAULT_SPELL_WAIT_TIME = 2000
CURSE_WEAPON_SCROLL = 0x2263
PIG_IRON = 0x0F8A

SPELL_WAIT_TIMES = {
    "magery": {
        "1": 900,
        "2": 1000,
        "3": 1000,
        "4": 1800,
        "5": 2200,
        "6": 2600,
        "7": 3000,
        "8": 3400,
    }
}

SPELLS = {
    # 1st circle
    "magic arrow": {
        "generates_target": True,
        "wait_time": SPELL_WAIT_TIMES["magery"].get("1"),
    },
    "heal": {
        "generates_target": True,
        "wait_time": SPELL_WAIT_TIMES["magery"].get("1"),
    },
    "weaken": {
        "generates_target": True,
        "wait_time": SPELL_WAIT_TIMES["magery"].get("1"),
    },
    # 2nd circle
    "cure": {
        "generates_target": True,
        "wait_time": SPELL_WAIT_TIMES["magery"].get("2"),
    },
    "arch cure": {
        "generates_target": True,
        "wait_time": SPELL_WAIT_TIMES["magery"].get("2"),
    },
    # 3rd circle
    "fireball": {
        "generates_target": True,
        "wait_time": SPELL_WAIT_TIMES["magery"].get("3"),
    },
    # 4th circle
    "lightning": {
        "generates_target": True,
        "wait_time": SPELL_WAIT_TIMES["magery"].get("4"),
    },
    "greater heal": {
        "generates_target": True,
        "wait_time": SPELL_WAIT_TIMES["magery"].get("4"),
    },
    "recall": {
        "generates_target": True,
        "wait_time": SPELL_WAIT_TIMES["magery"].get("4"),
    },
    # 5th circle
    # 6th circle
    "invisibility": {
        "generates_target": True,
        "wait_time": SPELL_WAIT_TIMES["magery"].get("6"),
    },
    "explosion": {
        "generates_target": True,
        "wait_time": SPELL_WAIT_TIMES["magery"].get("6"),
    },
    "energy bolt": {
        "generates_target": True,
        "wait_time": SPELL_WAIT_TIMES["magery"].get("6"),
    },
    # 7th circle
    "flame strike": {
        "generates_target": True,
        "wait_time": SPELL_WAIT_TIMES["magery"].get("7"),
    },
    "meteor swarm": {
        "generates_target": True,
        "wait_time": SPELL_WAIT_TIMES["magery"].get("7"),
    },
    # 8th circle
    "ressurection": {
        "generates_target": True,
        "wait_time": SPELL_WAIT_TIMES["magery"].get("8"),
    },
}


BUFF_ICONS = {
    "Dismount Prevention": 1001,
    "NoRearm": 1002,
    "Night Sight": 1005,
    "Death Strike": 1006,
    "Evil Omen": 1007,
    "Honored": 1008,
    "Achieve Perfection": 1009,
    "Divine Fury": 1010,
    "Enemy Of One": 1011,
    "HidingAndOrStealth": 1012,
    "Active Meditation": 1013,
    "Blood Oath Caster": 1014,
    "Blood Oath Curse": 1015,
    "Blood Oath": 1015,
    "Corpse Skin": 1016,
    "Mindrot": 1017,
    "PainS pike": 1018,
    "Strangle": 1019,
    "Gift Of Renewal": 1020,
    "Attune Weapon": 1021,
    "Thunderstorm": 1022,
    "Essence Of Wind": 1023,
    "Ethereal Voyage": 1024,
    "Gift Of Life": 1025,
    "Arcane Empowerment": 1026,
    "Mortal Strike": 1027,
    "Reactive Armor": 1028,
    "Protection": 1029,
    "Arch Protection": 1030,
    "Magic Reflection": 1031,
    "Incognito": 1032,
    "Disguised": 1033,
    "Animal Form": 1034,
    "Polymorph": 1035,
    "Invisibility": 1036,
    "Paralyze": 1037,
    "Poison": 1038,
    "Bleed": 1039,
    "Clumsy": 1040,
    "Feeblemind": 1041,
    "Weaken": 1042,
    "Curse": 1043,
    "Mass Curse": 1044,
    "Agility": 1045,
    "Cunning": 1046,
    "Strength": 1047,
    "Bless": 1048,
    "Sleep": 1049,
    "Stone Form": 1050,
    "Spell Plague": 1051,
    "Gargoyle Berserk": 1052,
    "Fly": 1054,
    "Inspire": 1055,
    "Invigorate": 1056,
    "Resilience": 1057,
    "Perseverance": 1058,
    "Tribulation": 1059,
    "Despair": 1060,
    "Arcane Empowerment2": 1061,
    "Magic Fish Buff": 1062,
    "Hit Lower Attack": 1063,
    "Hit Lower Defense": 1064,
    "Hit Dual Wield": 1065,
    "Block": 1066,
    "Defense Mastery": 1067,
    "Despair Bard": 1068,
    "Healing Skill": 1069,
    "Healing": 1069,
    "Spell Focusing": 1070,
    "Spell Focusing Debuff": 1071,
    "Rage Focusing Debuff": 1072,
    "Rage Focusing": 1073,
    "Warding": 1074,
    "Tribulation Bard": 1075,
    "Force Arrow": 1076,
    "Disarm": 1077,
    "Surge": 1078,
    "Feint": 1079,
    "Talon Strike": 1080,
    "Psychic Attack": 1081,
    "Consecrate Weapon": 1082,
    "Grapes Of Wrath": 1083,
    "Enemy Of One Debuff": 1084,
    "Horrific Beast": 1085,
    "Lich Form": 1086,
    "Vampiric Embrace": 1087,
    "Curse Weapon": 1088,
    "Reaper Form": 1089,
    "Immolating Weapon": 1090,
    "Enchant": 1091,
    "Honorable Execution": 1092,
    "Confidence": 1093,
    "Evasion": 1094,
    "Counter Attack": 1095,
    "Lightning Strike": 1096,
    "Momentum Strike": 1097,
    "Orange Petals": 1098,
    "Rose Of Trinsic Petals": 1099,
    "Poison Resistance": 1100,
    "Veterinary": 1101,
    "Perfection": 1102,
    "Honored2": 1103,
    "Mana Phase": 1104,
    "Fandancer Fan Fire": 1105,
    "Rage": 1106,
    "Webbing": 1107,
    "Medusa Stone": 1108,
    "Dragon Slasher Fear": 1109,
    "Aura Of Nausea": 1110,
    "Howl Of Cacophony": 1111,
    "Gaze Despair": 1112,
    "Hiryu Physical Resistance": 1113,
    "Rune Beetle Corruption": 1114,
    "Bloodworm Anemia": 1115,
    "Rotworm Blood Disease": 1116,
    "Skill Use Delay": 1117,
    "Faction Stat Loss": 1118,
    "Heat Of Battle": 1119,
    "Criminal": 1120,
    "Armor Pierce": 1121,
    "Splintering": 1122,
    "Swing Speed Debuff": 1123,
    "Wraith Form": 1124,
    "Honorable Execution2": 1125,
    "City Trade Deal": 1126,
}


# Basic mana cost,How to see if spell was cast ('buff, or 'journal', 'timer')
spellsDetails = {
    # TYPE 1: Regular FCR calc (on demise is bushido and some chiv spells)
    # TYPE 2: Necro and some chiv spells, a little faster. FCR 6 does not count latency - wait is 0! and FCR 5 is latency / 3
    # TYPE 3: Magery. A LOT faster. FCR 6 does not count latency. FCR 5 has almost no wait. FCR 4 is latency / 6.
    # templates (FCR 0, 1, 2, 3, 4, 5, 6) without rtt:
    # Type 1: 1500,1250,1000,750,500,250,0
    # Type 2: 1212,980,692,445,242,"0",0 #for sake, will use type 1 until FCR 1 (eg.: FCR 0 = 1250)
    # Type 3: 945,710,470,210,"0","0",0	#for sake, will use type 1 until FCR 2 (eg.: FCR 0 = 1000)
    "Greater Heal": {
        "manaCost": 11,
        "buffsToCheck": [],
        "journalToCheck": "",
        "timer": 1,
        "negateCheck": False,
        "afterCastWait": 1,
        "type": 3,
    },
    "Arch Cure": {
        "manaCost": 11,
        "buffsToCheck": [],
        "journalToCheck": "",
        "timer": 1,
        "negateCheck": False,
        "afterCastWait": 1,
        "type": 3,
    },
    "Bless": {
        "manaCost": 9,
        "buffsToCheck": [],
        "journalToCheck": "",
        "timer": 1,
        "negateCheck": False,
        "afterCastWait": 1,
        "type": 3,
    },
    "Ressurection": {
        "manaCost": 50,
        "buffsToCheck": [],
        "journalToCheck": "",
        "timer": 1,
        "negateCheck": False,
        "afterCastWait": 1,
        "type": 3,
    },
    # CHIV/BUSHIDO/2 necros
    # CHIV/BUSHIDO/2 necros
    # CHIV/BUSHIDO/2 necros
    "Lightning Strike": {
        "manaCost": 5,
        "buffsToCheck": ["Lightning Strike"],
        "journalToCheck": "",
        "timer": 1,
        "negateCheck": False,
        "afterCastWait": 1,
        "type": 2,
        # journal: "prepare to strike quickly" ou buff "lightning strike"
    },
    "Counter Attack": {
        "manaCost": 5,
        "buffsToCheck": ["Counter Attack"],
        "journalToCheck": "",
        "timer": 1500,
        "negateCheck": False,
        "afterCastWait": 12,
        "type": 1,
        # journal next blocked blow ou buff counter attack
    },
    "Confidence": {
        "manaCost": 10,
        "buffsToCheck": ["Confidence"],
        "journalToCheck": "",
        "timer": 1500,
        "negateCheck": False,
        "afterCastWait": 12,
        "type": 1,
        # journal exude confidence ou buff confidence
    },
    "Dispel Evil": {
        "manaCost": 10,
        "buffsToCheck": [],
        "journalToCheck": "",
        "timer": 1500,
        "negateCheck": False,
        "afterCastWait": 12,
        "type": 1,
        # mana
    },
    "Evasion": {
        "manaCost": 10,
        "buffsToCheck": ["Evasion"],
        "journalToCheck": "",
        "timer": 1500,
        "negateCheck": False,
        "afterCastWait": 12,
        "type": 1,
        # journal able to deflect any attack ou buff evasion
    },
    "Holy Light": {
        "manaCost": 10,
        "buffsToCheck": [],
        "journalToCheck": "",
        "timer": 1500,
        "negateCheck": False,
        "afterCastWait": 12,
        "type": 1,
        # TIME
    },
    ###########COMO FAZER ESSE????? MANA?##############
    ###########COMO FAZER ESSE????? MANA?##############
    ###########COMO FAZER ESSE????? MANA?##############
    "Cleanse by Fire": {
        "manaCost": 10,
        "buffsToCheck": [],
        "journalToCheck": "",
        "timer": 1500,
        "negateCheck": True,
        "afterCastWait": 0,
        "type": 2,
        # Não tem mais buff de poison
    },
    "Consecrate Weapon": {
        "manaCost": 10,
        "buffsToCheck": ["Consecrate Weapon"],
        "journalToCheck": "",
        "timer": 1500,
        "negateCheck": False,
        "afterCastWait": 12,
        "type": 1,
        # buff Consecrate Weapon
    },
    "Close Wounds": {
        "manaCost": 10,
        "buffsToCheck": [],
        "journalToCheck": "",
        "timer": 1500,
        "negateCheck": False,
        "afterCastWait": 0,
        "type": 2,
        # heal. checar life?
    },
    "Divine Fury": {
        "manaCost": 15,
        "buffsToCheck": ["Divine Fury"],
        "journalToCheck": "",
        "timer": 1500,
        "negateCheck": False,
        "afterCastWait": 12,
        "type": 2,
        # Buff Divine Fury
    },
    "Remove Curse": {
        "manaCost": 20,
        "buffsToCheck": ["Blood Oath", "Corpse Skin", "Curse", "Weaken", "Mindrot"],
        #'buffsToCheck': [],
        "journalToCheck": "",
        "timer": 1500,
        "negateCheck": True,
        "afterCastWait": 0,
        "type": 2,
        # não tem mais buffs de curse
    },
    "Enemy of One": {
        "manaCost": 20,
        "buffsToCheck": ["Enemy of One"],
        "journalToCheck": "",
        "timer": 1500,
        "negateCheck": False,
        "afterCastWait": 12,
        "type": 1,
        # buff enemy of one
    },
    "Vampiric Embrace": {
        "manaCost": 25,
        "buffsToCheck": [],
        "journalToCheck": "lost a lot of karma",
        "timer": 1250,
        "negateCheck": False,
        "afterCastWait": 0,
        "type": 2,
        # journal lost a lot of karma
    },
}


def IsActivatedBufficon(spell, timer_start=datetime.now()):
    bufficon = BUFF_ICONS.get(spell)
    info = GetBuffBarInfo()
    for icon in info:
        if icon.get("Attribute_ID") == bufficon:
            if bufficon == 1011:
                enemy_of_one_start = icon.get("TimeStart")
                if enemy_of_one_start < timer_start:
                    return False
                else:
                    return True
            else:
                return True
    return False


def is_buff_active(spell, timer_start=datetime.now()):
    bufficon = BUFF_ICONS.get(spell)
    info = GetBuffBarInfo()
    for icon in info:
        if icon.get("Attribute_ID") == bufficon:
            if bufficon == 1011:
                enemy_of_one_start = icon.get("TimeStart")
                if enemy_of_one_start < timer_start:
                    return False
                else:
                    return True
            else:
                return True
    return False


def setFCRAndManaCost():
    global spellsDetails
    extended_info = GetExtInfo()
    # print(extended_info)
    # charLMC = extended_info['Lower_Mana_Cost']
    # charLMC = 22

    # charFCR = extended_info['Faster_Cast_Recovery']
    # charFCR = 3
    # charFCRCalc=((6 - charFCR) / 4 * 1000) + rtt_latency/2 + security_margin

    for key, value in spellsDetails.items():
        newManaCost = round(
            spellsDetails[key]["manaCost"]
            - (spellsDetails[key]["manaCost"] * charLMC / 100)
        )
        spellsDetails[key]["manaCost"] = newManaCost

        if spellsDetails[key]["type"] == 1:
            charFCRCalc = ((6 - charFCR) / 4 * 1000) + rtt_latency / 2 + security_margin
            newFCR = round(spellsDetails[key]["afterCastWait"] + charFCRCalc)
            spellsDetails[key]["afterCastWait"] = newFCR
        elif spellsDetails[key]["type"] == 2:
            charFCRCalc = (
                ((6 - 1 - charFCR) / 4 * 1000) + rtt_latency / 2 + security_margin
            )
            if charFCRCalc < 0:
                charFCRCalc = 0
            newFCR = round(spellsDetails[key]["afterCastWait"] + charFCRCalc)
            spellsDetails[key]["afterCastWait"] = newFCR
        elif spellsDetails[key]["type"] == 3:
            charFCRCalc = (
                ((6 - 2 - charFCR) / 4 * 1000) + rtt_latency / 2 + security_margin
            )
            if charFCRCalc < 0:
                charFCRCalc = 0
            newFCR = round(spellsDetails[key]["afterCastWait"] + charFCRCalc)
            spellsDetails[key]["afterCastWait"] = newFCR
    # BASE
    # var afterCastWait = Math.round((6 - FCR) / 4)
    # O cálculo do FCR acima + latência / 1,5

    # Remove Curse
    # FCR 0 - 1575-1600
    # FCR 3 - 800-825
    # FCR 6 - 90-100

    # Consecrate Weapon
    # FCR 0  - 275-300
    print(spellsDetails)


def castSpell(spellName, target=False, waittime=False, checkBuff=True):
    # print(spellName)
    starttime = datetime.now()
    currMana = GetMana(Self())
    currMaxMana = GetMaxMana(Self())
    isCasting = GetGlobal("char", "isCasting")

    if isCasting == "True":
        common_utils.common_utils.debug("already casting a spell")
        return False

    common_utils.common_utils.debug("Trying to cast spell " + str(spellName))

    if spellName in spellsDetails and spellsDetails[spellName]["manaCost"] > currMana:
        common_utils.common_utils.debug("No Mana")
        return False

    SetGlobal(
        "char", "isCasting", "True"
    )  # Set a global var to inform that we are casting. get only works as string, that's why its not boolean...
    Cast(spellName)
    Wait(10)

    if target is not False:
        WaitTargetObject(target)
        if TargetPresent():
            TargetToObject(target)

    # print(InJournalBetweenTimes('not yet recovered|already casting|reagents', starttime, datetime.now()))
    # print("checkcast")
    if (
        InJournalBetweenTimes(
            "not yet recovered|already casting|reagents|frizzles|must wait before trying again|concentration is disturbed",
            starttime,
            datetime.now(),
        )
        > -1
    ):
        common_utils.common_utils.debug("##couldn't cast! Trying again!")
        Wait(50)
        Cast(spellName)
        if target is not False:
            WaitTargetObject(target)
            if TargetPresent():
                TargetToObject(target)

    if waittime is False and spellName in spellsDetails:
        superCommon_Utils.Common_Utils.Debug("spell in list")
        if checkBuff is True and spellsDetails[spellName]["buffsToCheck"]:
            superCommon_Utils.Common_Utils.Debug("check for buffs")
            print(spellsDetails[spellName]["buffsToCheck"])
            # Spellchecktype is buff!!!
            if spellsDetails[spellName]["negateCheck"] is True:
                while True:
                    Wait(2)
                    foundActiveBuff = True
                    for buff in spellsDetails[spellName]["buffsToCheck"]:
                        if IsActivatedBufficon(buff, starttime) is False:
                            foundActiveBuff = False
                            break
                    if foundActiveBuff is False:
                        # CASTED OK!!!
                        break
                    if datetime.now() >= starttime + timedelta(
                        milliseconds=DEFAULT_SPELL_WAIT_TIME
                    ):
                        print(
                            "SECURITY BREAK CHECKING SPELL CAST (BUFFS)! Spell:"
                            + str(spellName)
                        )  # could be a failed cast
                        SetGlobal("char", "isCasting", "False")
                        return False

                    if (
                        InJournalBetweenTimes(
                            "not yet recovered|already casting|reagents|frizzles|must wait before trying again|concentration is disturbed",
                            starttime,
                            datetime.now(),
                        )
                        > -1
                    ):
                        Wait(spellsDetails[spellName]["afterCastWait"])
                        common_utils.common_utils.debug(
                            "#couldn't cast inside checking buff (negate)! return false!"
                        )
                        SetGlobal("char", "isCasting", "False")
                        return False

                # We must check if the buffs are NOT actives
            else:
                while True:
                    Wait(2)
                    foundActiveBuff = False
                    for buff in spellsDetails[spellName]["buffsToCheck"]:
                        if IsActivatedBufficon(buff, starttime) is True:
                            foundActiveBuff = True
                            break
                    if foundActiveBuff is True:
                        superCommon_Utils.Common_Utils.Debug("found buff")
                        # CASTED OK!!!
                        break
                    if datetime.now() >= starttime + timedelta(
                        milliseconds=DEFAULT_SPELL_WAIT_TIME
                    ):
                        print(
                            "SECURITY BREAK CHECKING SPELL CAST (BUFFS)!"
                        )  # could be a failed cast
                        SetGlobal("char", "isCasting", "False")
                        return False

                    if (
                        InJournalBetweenTimes(
                            "not yet recovered|already casting|reagents|frizzles|must wait before trying again|concentration is disturbed",
                            starttime,
                            datetime.now(),
                        )
                        > -1
                    ):
                        common_utils.common_utils.debug(
                            "#couldn't cast inside checking buff! return false!"
                        )
                        Wait(spellsDetails[spellName]["afterCastWait"])
                        SetGlobal("char", "isCasting", "False")
                        return False

        elif spellsDetails[spellName]["journalToCheck"]:
            # Spellchecktype is journal
            while True:
                Wait(2)
                if (
                    InJournalBetweenTimes(
                        spellsDetails[spellName]["journalToCheck"],
                        starttime,
                        datetime.now(),
                    )
                    > -1
                ):
                    # CASTED OK!!!
                    break
                if datetime.now() >= starttime + timedelta(
                    milliseconds=DEFAULT_SPELL_WAIT_TIME
                ):
                    print(
                        "SECURITY BREAK CHECKING SPELL CAST (BUFFS)!"
                    )  # could be a failed cast
                    SetGlobal("char", "isCasting", "False")
                    return False

                if (
                    InJournalBetweenTimes(
                        "not yet recovered|already casting|reagents|frizzles|must wait before trying again|concentration is disturbed",
                        starttime,
                        datetime.now(),
                    )
                    > -1
                ):
                    common_utils.common_utils.debug(
                        "#couldn't cast inside checking journal! return false!"
                    )
                    Wait(spellsDetails[spellName]["afterCastWait"])
                    SetGlobal("char", "isCasting", "False")
                    return False

        else:
            superCommon_Utils.Common_Utils.Debug("mana check")
            # CHECK MANA!
            startTimeManaCheck = datetime.now()
            # while GetMana(Self()) >= currMana - spellsDetails[spellName]['manaCost']/2:
            while GetMana(Self()) >= currMana:
                if GetMaxMana(Self()) < currMaxMana:
                    print("#MAX MANA DROPED! (curse?) abort")
                    Wait(spellsDetails[spellName]["afterCastWait"])
                    SetGlobal("char", "isCasting", "False")
                    return False
                if datetime.now() >= startTimeManaCheck + timedelta(seconds=5):
                    print("#SECURITY BREAK MANA DIDN'T DROP!")
                    Wait(spellsDetails[spellName]["afterCastWait"])
                    manaBreak = True
                    SetGlobal("char", "isCasting", "False")
                    return False
                Wait(2)
                if (
                    InJournalBetweenTimes(
                        "not yet recovered|already casting|reagents|frizzles|must wait before trying again|concentration is disturbed",
                        starttime,
                        datetime.now(),
                    )
                    > -1
                ):
                    common_utils.common_utils.debug(
                        "#couldn't cast inside checking mana! return false!"
                    )
                    Wait(spellsDetails[spellName]["afterCastWait"])
                    SetGlobal("char", "isCasting", "False")
                    return False
            # Wait(spellsDetails[spellName]['timer'])

    else:
        superCommon_Utils.Common_Utils.Debug("mana check else")
        # CHECK MANA!
        startTimeManaCheck = datetime.now()
        while GetMana(Self()) >= currMana:
            if GetMaxMana(Self()) < currMaxMana:
                print("#MAX MANA DROPED! (curse?) abort")
                break
                # Wait(spellsDetails[spellName]['afterCastWait'])
                # return False
            if datetime.now() >= startTimeManaCheck + timedelta(seconds=5):
                print("#SECURITY BREAK MANA DIDN'T DROP!")
                break
                # Wait(spellsDetails[spellName]['afterCastWait'])
                # manaBreak = True
                # return False
            Wait(2)
            if (
                InJournalBetweenTimes(
                    "not yet recovered|already casting|reagents|frizzles|must wait before trying again|concentration is disturbed",
                    starttime,
                    datetime.now(),
                )
                > -1
            ):
                common_utils.common_utils.debug(
                    "#couldn't cast inside checking mana! return false!"
                )
                break
                # Wait(spellsDetails[spellName]['afterCastWait'])
                # return False
        if waittime is not False:
            Wait(waittime)
        else:
            Wait(DEFAULT_SPELL_WAIT_TIME)

        SetGlobal("char", "isCasting", "False")
        return

    # HERE YOU INSERT THE AFTER CAST WAIT TIME (FCR?)
    common_utils.common_utils.debug(
        "Waiting FCR/After cast. cur:" + str(spellsDetails[spellName]["afterCastWait"])
    )
    Wait(spellsDetails[spellName]["afterCastWait"])
    SetGlobal("char", "isCasting", "False")


def checkSpellWaitTime(
    spell1,
    spell2,
    spell1HasTarget=True,
    spell2HasTarget=True,
    manaCheckSpell1=True,
    startcast=3000,
    initialWaitTime=0,
    tolerance=5,
    waitTimeInMS=30000,
    descendRatio=2,
):
    ClearJournal()
    ClearSystemJournal()
    foundValue = False
    if initialWaitTime < 0:
        initialWaitTime = 0
    print(
        "----CHECKING SPELL:"
        + str(spell1)
        + ". maximumTime: "
        + str(startcast)
        + ". minTime: "
        + str(initialWaitTime)
        + ".----"
    )

    currCast = startcast
    beforeTime = 0

    descendingTime = startcast - initialWaitTime
    secondsToCheckMana = 5

    castSucess = False

    bestCastTime = 5000

    goodTimes = []
    goodTimesCurrTime = []

    while not foundValue:
        manaBreak = False
        timeToCast = 0
        currMana = GetMana(Self())

        # differenceBetweenTimes = highLimit - lowLimit
        # halfDifferenceBetweenTimes = differenceBetweenTimes / 2
        # ClientPrintEx(Self(), 66, 1, "begin."+str(currMana))
        startTimeCast = datetime.now()
        Cast(spell1)
        if spell1HasTarget is True:
            WaitTargetObject(Self())
            if TargetPresent():
                TargetToObject(Self())
        castingTime = datetime.now() - startTimeCast

        # ClientPrintEx(Self(), 66, 1, "manachecking."+str(currMana))
        startTimeManaCheck = datetime.now()
        if manaCheckSpell1 is True:
            while GetMana(Self()) >= currMana:
                # print("Waiting mana. starttime:"+str(startTimeManaCheck+timedelta(seconds=secondsToCheckMana))+". now:"+str(datetime.now()))
                if datetime.now() >= startTimeManaCheck + timedelta(
                    seconds=secondsToCheckMana
                ):
                    # print("MANA DIDN'T DROP! Trying loop all again!")
                    manaBreak = True
                    break
                Wait(10)
            if manaBreak is True:
                continue
        timeToCast = datetime.now() - startTimeManaCheck
        # ClientPrintEx(Self(), 66, 1, "manachecked"+str(timeToCast)+". mana:"+str(GetMana(Self())))

        Wait(currCast)

        Cast(spell2)
        if spell2HasTarget is True:
            WaitTargetObject(Self())
            if TargetPresent():
                TargetToObject(Self())

        Wait(5000)

        if InJournal("wait before trying again") > -1:
            Wait(1000)
            ClearJournal()
            ClearSystemJournal()
            continue

        # print("curr time:"+str(currCast)+". low limit: "+str(lowLimit)+". high limit: "+str(highLimit)+". half cast: "+str(halfDifferenceBetweenTimes)+".")
        if InJournal("recovered|already casting") > -1:
            if currCast == startcast:
                print("PROBLEM!!!!")
                return False
            # currCast = currCast + halfDifferenceBetweenTimes
            descendingTime = descendingTime / descendRatio
            beforeTime = currCast
            currCast = round(currCast + descendingTime)
            # lowLimit = currCast
            castSucess = False
        else:
            goodTimes.append(timeToCast.total_seconds() * 1000 + currCast)
            goodTimesCurrTime.append(currCast)
            if currCast < bestCastTime:
                # record bestCastTime
                bestCastTime = currCast

            # currCast = currCast - halfDifferenceBetweenTimes
            descendingTime = descendingTime / descendRatio
            beforeTime = currCast
            currCast = round(currCast - descendingTime)
            # highLimit = currCast
            castSucess = True

        print(
            "curr time:"
            + str(beforeTime)
            + ". descendingTime: "
            + str(descendingTime)
            + ". casting time: "
            + str(castingTime)
            + ". timeAfterCast: "
            + str(timeToCast)
            + ". Total (wait+timetocast): "
            + str(timeToCast.total_seconds() * 1000 + beforeTime)
            + ".Sucess? "
            + str(castSucess)
            + ". Injournal?"
            + str(InJournal("recovered|already casting|wait before trying again"))
        )

        if descendingTime < tolerance:
            median = statistics.median(goodTimes)
            medium = sum(goodTimes) / len(goodTimes)
            medianCurTime = statistics.median(goodTimesCurrTime)
            mediumCurTime = sum(goodTimesCurrTime) / len(goodTimesCurrTime)
            print(
                "##########WAIT CAST TIME:"
                + str(currCast)
                + ". descendingTime: "
                + str(descendingTime)
                + ". BEST: "
                + str(bestCastTime)
                + ". Medium (total): "
                + str(medium)
                + ". Median (total): "
                + str(median)
                + ". Medium (curr time): "
                + str(mediumCurTime)
                + ". Median (curr time): "
                + str(medianCurTime)
                + ".###########"
            )
            print("Array of times (total):")
            print(goodTimes)
            print("Array of times (currtime):")
            print(goodTimesCurrTime)
            print("#######################################################")
            return bestCastTime

        Wait(waitTimeInMS)
        while GetMana(Self()) < 44:
            Wait(1000)
        ClearJournal()
        ClearSystemJournal()


# ###################################################################
# GENERIC CAST FUNCTION
# ###################################################################
#
def cast(spell_name, serial=0):
    spell_generates_target = SPELLS.get(spell_name).get("generates_target")
    spell_wait_time = SPELLS[spell_name].get("wait_time")
    if TargetPresent():
        CancelTarget()
    if spell_generates_target:
        CastToObj(spell_name, serial)
        Wait(spell_wait_time)
    else:
        Cast(spell_name)
        Wait(spell_wait_time)
    return


def cast_self(spell_name):
    cast(spell_name, char)
    return


# ###################################################################
# MAGERY CAST HELPERS
# ###################################################################


# simulate Razor and UOSteam mage big and mini heals
def mage_mini_heal():
    if Poisoned() and GetMana(char) > 10:
        cast_self("cure")
    if GetMana(char) > 10:
        cast_self("heal")


def mage_big_heal():
    if TargetPresent():
        CancelTarget()
    if Poisoned() and GetMana(char) > 10:
        cast_self("arch cure")
    if GetMana(char) > 10:
        cast_self("greater heal")


# ###################################################################
# CHIVALRY CAST HELPERS
# ###################################################################


def chivalry_heal():
    if TargetPresent():
        CancelTarget()
    if Poisoned() and GetMana(char) > 10:
        CastToObj("Cleanse by Fire", char)
        Wait(3000)
    elif GetHP(char) < GetMaxHP(char) and GetMana(char) > 10:
        CastToObj("Close Wounds", char)
        Wait(4000)


def chivheal():
    return chivalry_heal()


# ENEMY OF ONE
def cast_enemy_of_one():
    if GetSkillValue("Chivalry") >= 60:
        if not is_buff_active("Enemy of One") and GetMana(char) >= 14:
            Cast("Enemy of One")
            Wait(300)


def cast_consecrate_weapon():
    if GetSkillValue("Chivalry") >= 60:
        if (not is_buff_active("Consecrate Weapon")) and (GetMana(char) >= 8):
            Cast("Consecrate Weapon")
            Wait(200)


def chivalry_remove_curse():
    # REMOVE CURSE
    if (
        is_buff_active("Blood Oath")
        or is_buff_active("Curse")
        or is_buff_active("Clumsy")
        or is_buff_active("Weaken")
    ):
        common_utils.debug("Removing Curse")
        Cast("Remove Curse")
        WaitForTarget(2000)
        if TargetPresent():
            WaitTargetObject(char)
        Wait(1000)


def cast_divine_fury():
    if GetSkillValue("Chivalry") >= 60:
        common_utils.debug("Casting Divine Fury")
        # if stam is under 70%, fill it
        if GetStam(char) < GetMaxStam(char) * 0.7 and GetMana(char) >= 12:
            common_utils.debug("Under 70% stamina. Re-Filling...")
            Cast("Divine Fury")
            common_utils.wait_lag(1500)
            return True
        elif common_utils.count_set_hci() < 40:
            common_utils.debug(
                "Char HCI is under %d. Casting Divine Fury..."
                % (common_utils.count_set_hci())
            )
            Cast("Divine Fury")
            common_utils.wait_lag(1500)
            return True


def cast_confidence():
    if GetSkillValue("Bushido") >= 80:
        if (
            not is_buff_active("Confidence")
            and GetHP(char) < GetMaxHP(char)
            and not is_buff_active("Evasion")
        ):
            common_utils.debug("Casting Confidence")
            cast("Confidence")
            Wait(200)
            return True


def cast_evasion():
    if not is_buff_active("Evasion") and GetHP(char) > GetMaxHP(char) * 0.8:
        common_utils.debug("Casting Evasion")
        Cast("Evasion")
        Wait(200)
        return True


def cast_counter_attack():
    if GetSkillValue("Bushido") >= 80:
        if (
            not is_buff_active("Counter Attack")
            and GetMana(char) >= 5
            # and not is_buff_active("Evasion")
            # and not is_buff_active("Confidence")
        ):
            # common_utils.common_utils.debug("* COUNTER ATTACK *", 10)
            Cast("Counter Attack")
            Wait(500)


# def cast_counter_attack():
#     if (
#         not is_buff_active("Evasion")
#         and not is_buff_active("Confidence")
#         and not is_buff_active("Counter Attack")
#     ):
#         # if not is_buff_active("Evasion") and not is_buff_active("Counter Attack"):
#         print("Casting Counter Attack")
#         Cast("Counter Attack")
#         Wait(500)
#         return True


def cast_confidence():
    if (
        GetSkillValue("Bushido") >= 80
        and not is_buff_active("Confidence")
        # and GetHP(char) < GetMaxHP(char) * 0.7
    ):
        # ClientPrintEx(char, 40, -2, "CONFIDENCE!")
        Cast("Confidence")
        Wait(500)
        return True


def cast_lightning_strike():
    if GetSkillValue("Bushido") >= 80:
        if not is_buff_active("Lightning Strike") and GetMana(char) >= 10:
            # common_utils.common_utils.debug("* LIGHTNING STRIKE *", 10)
            Cast("Lightning Strike")
            Wait(500)


def cast_arcane_empowerment():
    if FindType(0x3155, Backpack()) and GetSkillValue("spellweaving") >= 80:
        if not self.is_buff_active("Arcane Empowerment"):
            Cast("Arcane Empowerment")
            Wait(1500)


def dispel_renavant():
    # Dispeling renavant
    if FindType(0x190, Ground()) > 0:
        founds = GetFindedList()
        for found in founds:
            if GetName(found).find("a revenant") >= 0:
                Cast("Dispel Evil")
                Wait(1000)


def cast_remove_curse():
    if GetSkillValue("Chivalry") >= 60:
        if is_buff_active("Blood Oath"):
            SetWarMode(True)
            SetWarMode(False)
            common_utils.debug("Removing Blood Oath")
            Cast("Remove Curse")
            WaitForTarget(3000)
            if TargetPresent():
                WaitTargetObject(char)
            Wait(1000)


# ###################################################################
# NECRO CAST HELPERS
# ###################################################################


def cast_curse_weapon():
    # curse-weapon
    if (
        GetHP(char) < GetMaxHP(char) * 0.8  # no need to cast if life is full
        and not is_buff_active("Curse Weapon")
        and GetMana(char) > 5
    ):
        if FindType(CURSE_WEAPON_SCROLL, Backpack()):
            UseType2(CURSE_WEAPON_SCROLL)
            scroll_count = common_utils.count(CURSE_WEAPON_SCROLL)
            common_utils.debug("*Curse Weapon Scroll (%d left)* " % (scroll_count))
        # elif count_set_lrc() > 80:
        #     Cast("Curse Weapon")
        elif FindType(PIG_IRON, Backpack()):
            Cast("Curse Weapon")


def cast_wraith_form():
    if GetType(char) != 0x2EB and GetType(char) != 0x2EC:
        common_utils.debug("Char is not in Wraith form! Turning...")
        # if not is_set_equiped():
        #     dress_char_set()

        start_time = datetime.now()
        while GetType(char) != 0x2EB and GetType(char) != 0x2EC:
            if GetMana(char) < 16:
                common_utils.common_utils.debug("Waiting for mana to cast Wraith Form")
                starttime = datetime.now()
                while GetMana(char) < 16:
                    if common_utils.check_timer(starttime, 4000):
                        common_utils.common_utils.debug(
                            "Waiting for mana to cast Wraith Form"
                        )
                        starttime = datetime.now()
                    Wait(100)
            else:
                Cast("wraith form")
                Wait(1000)
                if (
                    InJournalBetweenTimes("spell fizzles", start_time, datetime.now())
                    < 0
                    and InJournalBetweenTimes(
                        "More reagents are needed", start_time, datetime.now()
                    )
                    < 0
                ):
                    Cast("Wraith Form")
                    Wait(1000)


def cast_vampiric_embrace():
    if GetColor(char) != 33918:
        common_utils.debug("Turning into Vampire...")
        if (
            not common_utils.count(common_utils.VAMPIRIC_EMBRACE_SCROLL)
            and common_utils.count_set_lrc() < 21
        ):
            common_utils.debug(
                "Char doenst have enough LRC. Gonna try to equip some LRC..."
            )
            start_time = datetime.now()
            common_utils.find_lrc_items_in_backpack_and_dress()
            common_utils.wait_lag(500)

        starttime = datetime.now()
        while GetColor(char) != 33918:
            if common_utils.has_item_in_backpack(common_utils.VAMPIRIC_EMBRACE_SCROLL):
                UseType2(common_utils.VAMPIRIC_EMBRACE_SCROLL)
            elif GetMana(char) < 23:
                common_utils.common_utils.debug(
                    "Waiting for mana to cast Vampiric Embrace"
                )
                while GetMana(char) < 23:
                    if common_utils.check_timer(starttime, 10000):
                        common_utils.common_utils.debug(
                            "Waiting for mana to cast Vampiric Embrace"
                        )
                        starttime = datetime.now()
                    Wait(100)
            else:
                Cast("Vampiric Embrace")
                common_utils.wait_lag(common_utils.VAMPIRIC_EMBRACE_CAST_TIME)
                if (
                    InJournalBetweenTimes("spell fizzles", starttime, datetime.now())
                    < 0
                    and InJournalBetweenTimes(
                        "More reagents are needed", starttime, datetime.now()
                    )
                    < 0
                ):
                    Cast("Vampiric Embrace")
                    common_utils.wait_lag(common_utils.VAMPIRIC_EMBRACE_CAST_TIME)

        if GetColor(char) == 33918:
            common_utils.debug("Turned into Vampire.")

            if not common_utils.is_set_equiped():
                common_utils.undress_char_set()
                common_utils.dress_char_set()
            return True
        else:
            return False
    else:
        common_utils.debug("Already in Vampire Form.")
        return False
