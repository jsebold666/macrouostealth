# =======================================================================
# JAIL UTILS
# =======================================================================

from modules.common_utils import debug
import modules.common_utils as utils

from modules.types import GATE
import modules.types as types
from modules.gumps import use_object_and_wait_gump, GATE_GUMP_ID
import modules.gumps as gumps


char = Self()

JAIL_X_TOP_LEFT = 5270
JAIL_Y_TOP_LEFT = 1160
JAIL_X_BOTTOM_RIGHT = 5310
JAIL_Y_BOTTOM_RIGHT = 1190

JAIL_ESCAPE_GATE_6H_X = 5301
JAIL_ESCAPE_GATE_6H_Y = 1180

JAIL_6H_X_TOP_LEFT = 5302
JAIL_6H_Y_TOP_LEFT = 1180
JAIL_6H_X_BOTTOM_RIGHT = 5310
JAIL_6H_Y_BOTTOM_RIGHT = 1190

#################################################################
# JAIL UTILS
#  jo
#################################################################


# checks if char is in jail, prints a msg in log and warns in discord
def is_char_in_jail(charFunction=""):
    currentX = GetX(char)
    currentY = GetY(char)

    if (currentX >= JAIL_X_TOP_LEFT) and (currentX <= JAIL_X_BOTTOM_RIGHT):
        if (currentY >= JAIL_Y_TOP_LEFT) and (currentY <= JAIL_Y_BOTTOM_RIGHT):
            return True
    else:
        return False


# checks if char is in jail, prints a msg in log and warns in discord
def is_char_in_6_hours_jail(charFunction=""):
    currentX = GetX(char)
    currentY = GetY(char)

    if (currentX >= JAIL_6H_X_TOP_LEFT) and (currentX <= JAIL_6H_X_BOTTOM_RIGHT):
        if (currentY >= JAIL_6H_Y_TOP_LEFT) and (currentY <= JAIL_6H_Y_BOTTOM_RIGHT):
            return True
    else:
        return False


def escape_jail(charFunction=""):
    currentX = GetX(char)
    currentY = GetY(char)

    if is_char_in_jail():
        UOSay("I have been warned")
        Wait(7000)
        SetFindDistance(2)
        if FindType(types.GATE, Ground()):
            escape_gate = FindItem()
            utils.debug("Escaping jail")
            gumps.use_object_and_wait_gump(escape_gate, GATE_GUMP_ID)
            NumGumpCheckBox(0, 8, 1)
            wait_gump_and_press_btn(GATE_GUMP_ID, GATE_CONFIRM_BTN)
    else:
        return False
