SetFindDistance(14)
SetFindVertical(14) 
while True:

     if FindTypeEx(0x22C5, 2130, Ground(), False):
        founds = GetFindedList()
        for found in founds:
            print('Foundsss', founds) 
            print('Id Found',found)
            ClickOnObject(1152260579)
            Wait(250)   
            if ( found == 1152260579):
                print('[Property] Error: Invalid', GetName(found))
                UseObject(found)
                
