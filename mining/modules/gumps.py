# checks if char is in jail, prints a msg in log and warns in discord
GATE_GUMP_ID = 0xE0E675B8
GATE_CONFIRM_BTN = 1


# =========================================================================
# REFILL TITHING POINS SETTINGS
# =========================================================================

TITHE_GOLD_GUMP_ID = 3746635695
TITHE_GOLD_POSITION = 2
TITHE_ALL_GOLD_BTN = 4
TITHE_ALL_GOLD_OK_BTN = 5


# ===================================================================
# GUMP Utils
# ===================================================================
#
def step_until_gump(direction, gumpID, times):
    return walkStepCheckingGump(direction, gumpID, times)


def walkStepCheckingGump(direction, gumpID, times):
    SetMoveThroughNPC(True)
    for i in range(times):
        Step(direction, False)
        if gump_exists(gumpID):
            return
        Wait(18)


def close_gumps():
    while IsGump():
        if not Connected():
            return False
        if not IsGumpCanBeClosed(GetGumpsCount() - 1):
            return False
        # WaitGump('0')
        else:
            CloseSimpleGump(GetGumpsCount() - 1)
    return True


def use_object_and_wait_gump(object, gump_id, timeout=15):
    return waitgumpid(gump_id, object, timeout=15)


def waitgumpid(gumpid, object, timeout=15):
    maxcounter = 0
    UseObject(object)
    while maxcounter < timeout * 10:
        if IsGump():
            for currentgumpnumb in range(0, (GetGumpsCount())):
                currentgump = GetGumpInfo(currentgumpnumb)
                if (
                    "GumpID" in currentgump
                ):  # got to check if key exists or we might get an error
                    if currentgump["GumpID"] == gumpid:
                        return True
                if IsGumpCanBeClosed(currentgumpnumb):
                    CloseSimpleGump(currentgumpnumb)
        maxcounter += 1
        CheckLag(5000)
    return False


def wait_gump_without_using_object(gumpid, timeout=15):
    maxcounter = 0
    while maxcounter < timeout * 10:
        if IsGump():
            for currentgumpnumb in range(0, (GetGumpsCount())):
                currentgump = GetGumpInfo(currentgumpnumb)
                if (
                    "GumpID" in currentgump
                ):  # got to check if key exists or we might get an error
                    if currentgump["GumpID"] == gumpid:
                        return True
                if IsGumpCanBeClosed(currentgumpnumb):
                    CloseSimpleGump(currentgumpnumb)
        maxcounter += 1
        CheckLag(100000)
    return False


def wait_gump_and_press_btn(gumpid, number=0, pressbutton=True, timeout=15):
    maxcounter = 0
    while maxcounter < timeout * 10:
        if IsGump():
            for currentgumpnumb in range(0, (GetGumpsCount())):
                currentgump = GetGumpInfo(currentgumpnumb)
                if (
                    "GumpID" in currentgump
                ):  # got to check if key exists or we might get an error
                    if currentgump["GumpID"] == gumpid:
                        if pressbutton:
                            NumGumpButton(currentgumpnumb, number)
                        else:
                            return currentgump
                        return True
                if IsGumpCanBeClosed(currentgumpnumb):
                    CloseSimpleGump(currentgumpnumb)
        maxcounter += 1
        CheckLag(100000)
    return False


def waitgumpid_checkbox(gumpid, number=0, pressbutton=True, value=0, timeout=15):
    maxcounter = 0
    while maxcounter < timeout * 10:
        if IsGump():
            for currentgumpnumb in range(0, (GetGumpsCount())):
                currentgump = GetGumpInfo(currentgumpnumb)
                if (
                    "GumpID" in currentgump
                ):  # got to check if key exists or we might get an error
                    if currentgump["GumpID"] == gumpid:
                        if pressbutton:
                            NumGumpCheckBox(currentgumpnumb, number, value)
                        else:
                            return currentgump
                        return True
                if IsGumpCanBeClosed(currentgumpnumb):
                    CloseSimpleGump(currentgumpnumb)
        maxcounter += 1
        CheckLag(100000)
    return False


def waitgumpid_textentry(gumpid, textEntryId=0, value="", timeout=15):
    maxcounter = 0
    while maxcounter < timeout * 10:
        if IsGump():
            for currentgumpnumb in range(0, (GetGumpsCount())):
                currentgump = GetGumpInfo(currentgumpnumb)
                if (
                    "GumpID" in currentgump
                ):  # got to check if key exists or we might get an error
                    if currentgump["GumpID"] == gumpid:
                        NumGumpTextEntry(currentgumpnumb, textEntryId, value)
                        return True
                if IsGumpCanBeClosed(currentgumpnumb):
                    CloseSimpleGump(currentgumpnumb)
        maxcounter += 1
        CheckLag(100000)
    return False


def gump_exists(gumpid):
    for i in range(GetGumpsCount()):
        if gumpid and gumpid == GetGumpID(i):
            return True
    return False


def get_in_gump_field_value(gump_text):
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
                # print("HTML")
                found = next(
                    (
                        GetClilocByID(x["ClilocID"]).upper()
                        for x in infogump["XmfHtmlGump"]
                        if gump_text.upper() in GetClilocByID(x["ClilocID"]).upper()
                    ),
                    None,
                )
                break
            if not found and len(infogump["XmfHTMLGumpColor"]) > 0:
                # print("HTML color")
                found = next(
                    (
                        GetClilocByID(x["ClilocID"]).upper()
                        for x in infogump["XmfHTMLGumpColor"]
                        if gump_text.upper() in GetClilocByID(x["ClilocID"]).upper()
                    ),
                    None,
                )
                break
            elif not found and len(infogump["Text"]) > 0:
                # print("text")
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
        # if value != 999:
        #     NumGumpButton(GetGumpsCount() - 1, value)
    return found


def find_text_in_open_gump_and_pŕess_btn(text, btn_number=999):
    if value != 999:
        return in_gump(text, btn_number)

    return in_gump(text, btn_number)


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
                # print("HTML")
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
                # print("HTML color")
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
                # print("text")
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


def InGumpRegexIN_UPPERCASE(regex):
    t = 1
    while True:
        # print ("while")
        for i in range(GetGumpsCount()):
            print("loop")
            infogump = GetGumpInfo(i)
            # print ("for")
            index = i

            if len(infogump["XmfHtmlGump"]) > 0:
                print("HTMLGump")
                for gump_line in infogump["XmfHtmlGump"]:
                    print(str(GetClilocByID(gump_line["ClilocID"])))
                    regexSearch = re.search(
                        regex, GetClilocByID(gump_line["ClilocID"]).upper()
                    )
                    if regexSearch is not None:
                        return regexSearch

            if len(infogump["XmfHTMLGumpColor"]) > 0:
                print("XmfHTMLGumpColor")
                for x in infogump["XmfHTMLGumpColor"]:
                    print(str(GetClilocByID(x["ClilocID"])))
                    regexSearch = re.search(regex, GetClilocByID(x["ClilocID"]).upper())
                    if regexSearch is not None:
                        return regexSearch

            elif len(infogump["Text"]) > 0:
                print("Text")
                for x in infogump["Text"]:
                    print(x[0])
                    regexSearch = re.search(regex, x[0].upper())
                    if regexSearch is not None:
                        return regexSearch
        Wait(100)
        t += 1
        if t > 5:
            return False
        CheckLag()
