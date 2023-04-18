from stealth import *

def stack(ObjType, Color):
    PackItem = 0
    GroundItem = 0
    FindType(ObjType, Backpack())
    if FindFullQuantity() > 0: PackItem = FindItem()
    FindType(ObjType, Ground())
    if FindFullQuantity() > 0: IgnoreReset()
    while True:
        FindTypeEx(ObjType, Color, Ground(), False)
        if FindCount() > 0:
            if FindQuantity() > 55000: Ignore(FindItem())
            else: GroundItem = FindItem()
        FindTypeEx(ObjType, Color, Ground(), False)
        if FindCount() == 0 or GroundItem != 0:
            break
    if (PackItem != 0) and (GroundItem != 0): MoveItems(Backpack(), ObjType, Color, GroundItem, 0, 0, 0, 1000)
    else: DropHere(PackItem)