# =======================================================================
# Check Connection
# =======================================================================

from modules.common_utils import wait_lag
import modules.common_utils as common


def connect():
    if not Connected():
        while not Connected():
            print("Character is not connected. Connecting...")
            Connect()
            Wait(15000)
    if Connected():
        # adding pause after connecting to try to fix bug where char connects too fast and doenst start macroing
        common.wait_lag(1500)


def reconnect():
    print("Reconnecting char...")
    Disconnect()
    Wait(8000)
    connect()


def check_connection():
    if not Connected():
        AddToSystemJournal("No connection.")
        while not Connected():
            AddToSystemJournal(">>> Trying to connect...")
            connect()
            Wait(5000)
        AddToSystemJournal("*** Server connection restored.")
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
        # print("Char name: %s" % (char_name))
        return char_name
