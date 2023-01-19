#####################################################
# RESS UTILS
#####################################################

from datetime import datetime, timedelta

char = Self()
try:
    from py_stealth import *
    import py_stealth as stealth
    from modules.common_utils import (
        check_timer,
        debug,
        open_help_request,
        HELP_REQUEST_GUMP_ID,
        HELP_REQUEST_CHARACTER_STUCK_BTN,
        HELP_REQUEST_CHOOSE_TOWN_GUMP_ID,
    )
    import modules.common_utils as utils

    from modules.regions import in_region
    import modules.regions as regions

    from modules.gumps import (
        in_gump,
        gump_exists,
        wait_gump_without_using_object,
        wait_gump_and_press_btn,
        close_gumps,
        step_until_gump,
    )
    import modules.gumps as gumps

    print("Ress Utils: Imported Py Stealth")
except Exception as err:
    print("Ress Utils: Error importing py_stealth: %s" % (err))
    exit()

RESS_GUMP_ID = 0xB04C9A31
PET_RESS_GUMP_ID = 0x4DA72C0
CHAR_MURDERED_GUMP = 523845830


def confirm_muder_gump():
    if gumps.gump_exists(CHAR_MURDERED_GUMP):
        utils.debug("%s was murdered by another player" % (CharName()))
        gumps.wait_gump_and_press_btn(CHAR_MURDERED_GUMP, 1, 5)


def open_town_selection_help_gump():
    while not gumps.in_gump("Delucia") and not gumps.in_gump("Cove"):

        utils.open_help_request()
        gumps.wait_gump_without_using_object(HELP_REQUEST_GUMP_ID, 5)
        utils.wait_lag(10)
        gumps.wait_gump_and_press_btn(
            HELP_REQUEST_GUMP_ID, HELP_REQUEST_CHARACTER_STUCK_BTN, 5, 15
        )
        utils.wait_lag(200)
        gumps.wait_gump_without_using_object(HELP_REQUEST_CHOOSE_TOWN_GUMP_ID, 5)
        if gumps.gump_exists(HELP_REQUEST_CHOOSE_TOWN_GUMP_ID):
            return True
    return False


def ress():
    if Dead():

        utils.debug("%s is dead! Trying to ress." % (CharName()))

        # If char was murdered, there is a gump present we need to close first
        confirm_muder_gump()

        currentX = GetX(char)
        currentY = GetY(char)

        wait_to_be_teleported = False
        # first pick a town to be teleported
        if not regions.in_region("cove") and not regions.in_region("delucia"):
            wait_to_be_teleported = True
            open_town_selection_help_gump()

            if gumps.in_gump("Cove"):
                utils.debug("Going to the healer in cove to ress")
                # FEL OR TRAM - COVE RESS
                gumps.wait_gump_and_press_btn(HELP_REQUEST_CHOOSE_TOWN_GUMP_ID, 6, 5)
                Wait(1000)
                gumps.close_gumps()

            elif gumps.in_gump("Delucia"):
                AddToSystemJournal("T2A Ress")
                # T2A - DELUCIA RESS
                gumps.wait_gump_and_press_btn(HELP_REQUEST_CHOOSE_TOWN_GUMP_ID, 2, 5)
                Wait(1000)
                gumps.close_gumps()

        # after choosing a town, wait to be teleported
        if wait_to_be_teleported:
            while currentX == GetX(char) and currentY == GetY(char):
                utils.debug("Char paralyzed. Waiting to be teleported")
                Wait(5000)

        healer_direction = 0
        healer_oposite_direction = 0
        # move to the town respective healer
        if regions.in_region("cove"):
            utils.debug("Moving to Cove Healer.")
            # NewMoveXY(2249,1229,True,0,True)
            NewMoveXY(
                2247, 1229, True, 0, True
            )  # fix by ivan, move correctly to coves healer
            utils.debug("%s next to the Healer." % (CharName()))
            healer_direction = 6
            healer_oposite_direction = 2

        # move to the town respective healer
        if regions.in_region("delucia"):
            utils.debug("Moving to Delucia Healer")
            NewMoveXY(5208, 3993, True, 0, True)
            NewMoveXY(5201, 3997, True, 0, True)
            healer_direction = 7
            healer_oposite_direction = 3

        # when char is at healer room, try to ress
        starttime = datetime.now()
        count = 0
        while not gumps.gump_exists(RESS_GUMP_ID):
            count = count + 1
            utils.debug("Trying to ress again. try:" + str(count))
            # Gump nao existe.... sair e entrar no healer de novo
            gumps.step_until_gump(healer_direction, RESS_GUMP_ID, 6)
            Wait(2000)
            gumps.step_until_gump(healer_oposite_direction, RESS_GUMP_ID, 6)

            if datetime.now() >= starttime + timedelta(minutes=10):
                utils.debug(
                    f">>> WARNING! COULD NOT RESS AFTER {count} TRIES! QUITING!"
                )
                SetARStatus(False)

                Disconnect()
                exit()

        wait_gump_without_using_object(RESS_GUMP_ID, 5)

        wait_gump_and_press_btn(RESS_GUMP_ID, 1, 5)
        utils.wait_lag(100)
        return True


HTOWN_RESS_GUMP_ID = 0x896028A5


def accept_ress_gump():
    if gumps.gump_exists(RESS_GUMP_ID):
        utils.debug("Ressurecting...")
        wait_gump_and_press_btn(RESS_GUMP_ID, 1)

    if gumps.gump_exists(HTOWN_RESS_GUMP_ID):
        utils.debug("Ressurecting in event...")
        wait_gump_and_press_btn(HTOWN_RESS_GUMP_ID, 1, 5)
        return True


def wait_and_accept_ress(timeout=30000):
    start_time = datetime.now()
    while (
        Dead()
        and not gumps.gump_exists(RESS_GUMP_ID)
        and not gumps.gump_exists(HTOWN_RESS_GUMP_ID)
    ):
        if common_utils.check_timer(start_time, 4000):
            utils.debug("Waiting ress gump...")
        if common_utils.check_timer(start_time, timeout):
            utils.debug("Timeout %d ms waiting for ress..." % (timeout))
            return False
        Wait(100)

    accept_ress_gump()
    if Dead():
        return False

    return True


def find_npc_healer_and_ress():
    healer = find_npc("healer")
    if healer:
        start_time = datetime.now()
        while (
            not gumps.gump_exists(RESS_GUMP_ID)
            and not gumps.gump_exists(HTOWN_RESS_GUMP_ID)
            and GetDistance(healer) > 2
        ):
            gumps.step_until_gump(
                CalcDir(GetX(char), GetY(char), GetX(healer), GetY(healer)),
                RESS_GUMP_ID,
                1,
            )
            if check_timer(start_time, 20000):
                utils.debug("20s trying to reach npc healer. Breaking...")
                break

        accept_ress_gump()

        if not gumps.gump_exists(HTOWN_RESS_GUMP_ID) and GetDistance(healer) <= 2:
            utils.debug(
                "Healer está muito próximo do char. Se afastando para poder gerar gump..."
            )
            gumps.step_until_gump(0, HTOWN_RESS_GUMP_ID, 1)


def go_to_healer_and_ress(healer):
    print("Indo em direção a %s para ressar..." % (GetName(healer)))
    while Dead():
        accept_ress_gump()
        while not gumps.gump_exists(RESS_GUMP_ID):
            accept_ress_gump()
            if GetDistance(healer) > 2:
                gumps.step_until_gump(
                    CalcDir(GetX(char), GetY(char), GetX(healer), GetY(healer)),
                    RESS_GUMP_ID,
                    1,
                )
