from datetime import datetime, timedelta
from py_stealth import *
from random import SystemRandom

random = SystemRandom()
from itertools import *

# Made by Quaker
# Have runes on backpack
BAG = 0xE76
MARK_TYPE = "miner"  #'lumber' or 'miner'
USE_ONLY_UNMARKED_RUNES = False
SORT_BY_DISTANCE = True
NUMBER_OF_RUNES = -1  # -1 = marcar todas.


def debug(message, message_color=66):
    AddToSystemJournal(message)
    ClientPrintEx(Self(), message_color, 1, message)


def set_container_for_marked_runes():
    global BAG_TO_PLACE_MARKED_RUNES
    if FindType(BAG, Backpack()):
        debug("Setting bag to put marked runes")
        BAG_TO_PLACE_MARKED_RUNES = FindItem()
    else:
        debug("Couldnt find a bag to put marked runes. Will leave them in backpack.")
        BAG_TO_PLACE_MARKED_RUNES = 0


TREE_TYPES = [
    3274,
    3275,
    3277,
    3280,
    3281,
    3282,
    3283,
    3286,
    3288,
    3290,
    3293,
    3296,
    3299,
    3302,
    3303,
    3320,
    3323,
    3326,
    3329,
    3393,
    3394,
    3395,
    3396,
    3415,
    3416,
    3418,
    3419,
    3438,
    3439,
    3440,
    3441,
    3442,
    3460,
    3461,
    3462,
    3476,
    3478,
    3480,
    3482,
    3484,
    3492,
    3496,
    4802,
    4801,
    4803,
]

caves = [
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
]
mountains = [
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
]

rocks = [
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
]  # rocks
MINING_TYPE = caves + mountains + rocks

DISTANCE_TO_FIND_TILE = 10


if MARK_TYPE == "lumber":
    DISTANCE_BETWEEN_MARKS = 4
else:
    DISTANCE_BETWEEN_MARKS = 2


if MARK_TYPE == "lumber":
    TILE_TYPES = TREE_TYPES
else:
    TILE_TYPES = MINING_TYPE

# Relative position to mark
RELATIVE_POSITION_X = 0
RELATIVE_POSITION_Y = +1

RUNE_TYPE = 0x1F14
RUNEBOOK_TYPE = 0x22C5

runes_in_runebook_count = 0
rune_per_runebooks = 16

actionDelay = 500

array_of_marked_positions = []


def markrune(rune):
    while Mana() < 20:
        UseSkill("Meditation")
        Wait(5000)
    Cast("Mark")
    Wait(actionDelay)
    WaitTargetObject(rune)
    Wait(actionDelay * 2)


def markrune_and_bond_to_runebook(runebook):
    while Mana() < 20:
        UseSkill("Meditation")
        Wait(5000)
    if FindTypesArrayEx([RUNE_TYPE], [0xFFFF], [Backpack()], False) > 0:
        rune = FindItem()
        Cast("Mark")
        Wait(actionDelay)
        WaitTargetObject(rune)
        Wait(actionDelay * 4)
        MyMoveItem(rune, 1, runebook, 0, 0, 0)
        Wait(actionDelay)


def MyMoveItem(ItemID, Count, MoveIntoID, X, Y, Z):
    Wait(100)
    drag = DragItem(ItemID, Count)
    debug("Draging? " + str(drag))
    if not drag:
        return False
    Wait(500)
    return DropItem(MoveIntoID, X, Y, Z)


import operator


def find_tiles_position(TILE_TYPES):
    global array_of_marked_positions
    global charX
    global charY
    charX = GetX(Self())
    charY = GetY(Self())
    positions = find_tiles(
        GetX(Self()), GetY(Self()), DISTANCE_TO_FIND_TILE, TILE_TYPES
    )
    # print("POS")
    # print(positions)
    # print("CHAIUN")
    # for tile, x, y, z in find_tiles_chain(GetX(Self()), GetY(Self()), DISTANCE_TO_FIND_TILE, TILE_TYPES):
    #    print(tile, x, y, z)

    # print("SORTED")

    if SORT_BY_DISTANCE:
        positions = sortByDistance(positions)
        # print(sortByDistance(positions))
        # print("after sort")
    # exit()

    for x, y in positions:
        too_close = False
        if IsWorldCellPassable(
            GetX(Self()),
            GetY(Self()),
            GetZ(Self()),
            x + RELATIVE_POSITION_X,
            y + RELATIVE_POSITION_Y,
            WorldNum(),
        )[0]:
            for past_coord in array_of_marked_positions:
                if Dist(past_coord[0], past_coord[1], x, y) <= DISTANCE_BETWEEN_MARKS:
                    too_close = True
                    break
            if too_close:
                print("TOO CLOSE")
                continue
            NewMoveXY(x + RELATIVE_POSITION_X, y + RELATIVE_POSITION_Y, 1, 0, True)
            # print(x)
            # print(y)
            # print(RELATIVE_POSITION_X,RELATIVE_POSITION_Y)
            # print("MOVEU")
            # exit()
            if identify_tile(
                GetX(Self()),
                GetY(Self()),
                -RELATIVE_POSITION_X,
                -RELATIVE_POSITION_Y,
                TILE_TYPES,
            ):
                print()
                array_of_marked_positions.append([x, y])
                debug("ACHOU LUGAR")
                # LUGAR CORRETO! MARCAR RUNA E ADICIONAR AO RUNEBOOK
                return True

    return False


def find_tiles(x, y, distance, tile_types):
    coords_array = []
    for t in tile_types:
        static = GetStaticTilesArray(
            x - distance, y - distance, x + distance, y + distance, WorldNum(), t
        )
        if static:
            for st in static:
                # print("ST")
                # print(st)
                if [st[1], st[2]] not in coords_array:
                    coords_array.append([st[1], st[2]])
        # print("static")
        # print(static)
    return coords_array


def identify_tile(x, y, relativeX, relativeY, tileType=[]):
    absRelativeX = abs(relativeX)
    absRelativeY = abs(relativeY)

    processedAbsRelativeX = absRelativeX + 2
    processedAbsRelativeY = absRelativeY + 2

    wantedPositionX = x + relativeX
    wantedPositionY = y + relativeY

    for xx in range(x - processedAbsRelativeX, x + processedAbsRelativeX):
        for yy in range(y - processedAbsRelativeY, y + processedAbsRelativeY):
            r = ReadStaticsXY(xx, yy, WorldNum())
            for result in r:
                # print(r)
                if result:
                    if (result["X"] == wantedPositionX) and (
                        result["Y"] == wantedPositionY
                    ):
                        # If array of tiletype is set, we need to check for a specific tile type!
                        if tileType:
                            if result["Tile"] in tileType:
                                return result
                        # if not, return the first tile
                        else:
                            return result
    return False


"""for t, x, y, z in find_trees(50):
    MoveXYZ(x, y, z, 1, 5, True)
    WaitTargetTile(t, x, y, z)
    use_axe()
"""


# For Python 3
def cmp_to_key(mycmp):
    "Convert a cmp= function into a key= function"

    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0

    return K


charX = 0
charY = 0


def sortByStealthDistance(x, y):
    # print(x,y)
    firstDistance = Dist(charX, charY, x[0], x[1])
    secondDistance = Dist(charX, charY, y[0], y[1])
    # print("after")
    # print("SORT. first:"+str(firstDistance)+". second:"+str(secondDistance))
    return firstDistance - secondDistance


def sortByDistance(arrayOfPoints):
    # arrayOfPoints.sort(key = lambda p: sqrt((p.centerX - centerX)**2 + (p.centerY - centerY)**2))
    # Python 2:
    # return sorted(arrayOfPoints, cmp=sortByStealthDistance)
    # Ptyhon 3:
    from functools import cmp_to_key

    return sorted(arrayOfPoints, key=cmp_to_key(sortByStealthDistance))


def main():

    set_container_for_marked_runes()
    runes = FindTypesArrayEx([RUNE_TYPE], [0xFFFF], [Backpack()], False)
    runes_found = GetFindedList()
    unmarked_runes_list = []
    if USE_ONLY_UNMARKED_RUNES:
        for i in runes_found:
            number_of_attributes = GetTooltip(i).count("|") + 1
            if number_of_attributes == 2:
                unmarked_runes_list.append(i)
    else:
        unmarked_runes_list = runes_found

    random.shuffle(unmarked_runes_list)
    rune_count = 0
    debug(f"Found a total of {len(runes_found)} to mark.")
    for rune in unmarked_runes_list:

        while Mana() < 20:
            ClientPrintEx(Self(), 66, 1, "Mana tool Low... Mediting")
            UseSkill("Meditation")
            Wait(5000)

        if find_tiles_position(TILE_TYPES):
            rune_count = rune_count + 1
            debug(f"Marking rune {rune_count} of {len(runes_found)}")
            markrune(rune)
            Wait(actionDelay * 4)
            MyMoveItem(rune, 1, BAG_TO_PLACE_MARKED_RUNES, 0, 0, 0)
            Wait(actionDelay)

        else:
            debug("Problem finding positions!!! Walking randomly")
            random.seed(10)
            random_number_x = random.randint(DISTANCE_BETWEEN_MARKS, 10)
            random_number_y = random.randint(DISTANCE_BETWEEN_MARKS, 10)
            random.seed(10)
            random_bool = random.randint(0, 3)
            debug(
                f"Moving to: \nX: {GetX(Self()) + random_number_x} | Y: {GetY(Self()) + random_number_y}"
            )
            if random_bool == 0:
                x = GetX(Self()) + random_number_x
                y = GetY(Self()) + random_number_y
            elif random_bool == 1:
                x = GetX(Self()) - random_number_x
                y = GetY(Self()) - random_number_y
            elif random_bool == 2:
                x = GetX(Self()) + random_number_x
                y = GetY(Self()) - random_number_y
            else:
                x = GetX(Self()) - random_number_x
                y = GetY(Self()) + random_number_y

            if NewMoveXY(
                x,
                y,
                True,
                2,
                True,
            ):
                debug("MOVED")
        if NUMBER_OF_RUNES > -1:
            if rune_count > NUMBER_OF_RUNES:
                ClientPrintEx(Self(), 66, 1, "Número de Runas Definidas Marcadas!")


if __name__ == "__main__":
    main()
