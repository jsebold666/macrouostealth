from stealth import *

BOD_TYPE_BS = [0x2258]
COLOR_BS = [1102]
BACKPACK = [Backpack()]
BOD_BOOK_TYPE = 0x2259
ANY_COLOR = 0xffff

def move_bods_to_book():
    if FindTypeEx(BOD_BOOK_TYPE, ANY_COLOR, Backpack()):
        book = FindItem()
        print(book)
    while FindTypesArrayEx(BOD_TYPE_BS, COLOR_BS, BACKPACK, False):
        findedbods = GetFindedList()
        for findedbod in findedbods: 
            if (findedbod):
                AddToSystemJournal('movendo bods ')
                MoveItem(findedbod, ANY_COLOR, book, 0, 0, 0)
                Wait(2000) 
            else:
                AddToSystemJournal('acabou as bof ')
                Wait(2000) 
    return

while 42:
    move_bods_to_book()
    exit()