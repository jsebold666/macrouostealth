import threading
from discord_webhook import DiscordWebhook
from datetime import *
from py_stealth import *

from common_utils import *
import common_utils

# =====================================================================================================
# CONFIG: Webhook and alarm as you wish
#
#
common_utils.RESPOND_AFK_GUMP = False
DISCORD_WEBHOOK_HTOWN = "https://discord.com/api/webhooks/900757304553644052/UJE7XDTyibVeKjRNzRpgBpLHIYBvHTY3WLsHpYfHXYldntTkgf2-rzFywScoESZ8lF6P"
common_utils.DISCORD_WEBHOOK_AFK_URL = DISCORD_WEBHOOK_HTOWN
#
common_utils.DISCORD_WEBHOOK = DISCORD_WEBHOOK_HTOWN
common_utils.WAV_AFK = "\\Scripts\\Sounds\\AFKCHECK.wav"
#
ALARM = "\\Scripts\\Sounds\\ALARM.wav"
#
#
# =====================================================================================================
# VARIABLES
# =====================================================================================================
WARNING_MSG_COOLDOWN = 60
timer_warning_check = datetime.now() - timedelta(seconds=WARNING_MSG_COOLDOWN)
#
# SETAR TRUE PARA MATAR APENAS BOSS PASSARO
PASSARO_ONLY = False
#
# END OF CONFIG! DO NOT EDIT!
# =====================================================================================================
OTHER_BOSS = [[6006, 633],[6059, 626], [6075, 579], [6075, 579],[6065, 580], [6064, 580], [6479, 2107], 
[6439, 2106], [6436, 2100], [6437, 2091], [6437, 2087], [6427, 2087], [6424, 2089], [6424, 2090], [5223, 2084],
[5223, 2083], [5198, 2083], [5189, 2083], [5190, 2091], [5190, 2098], [5193, 2098], [5193, 2085], [5190, 2085],
[5190, 2093], [5202, 2089], [5193, 2083],[5165, 2082],[5162, 2090], [5162, 2104], [5180, 2104], [5180, 2096],
[5175, 2096], [5172, 2095], [5172, 2104], [5218, 2103], [5219, 2089], [5200, 2089], [5200, 2078],
[5168, 2078], [5168, 2090], [5155, 2090], [5155, 2102], [5186, 2102], [5186, 2117],[5174, 2117],
[5176, 2110]]
PASSARO_PATH = [[6006, 633],[6059, 626],[6087, 621],[6087, 615],[6087, 612],[6083, 612],[6083, 601],[6090, 601]]
#PASSARO_PATH_DEPOIS_NINHO = [[7078,518],[7069,518],[7067,523],[7066,523],[7036,531]]
PATH_DEPOIS_DO_RAIO = [[7050,527],[7036,531]]

DEPOIS_DO_NINHO_MIN_Y = 514
DEPOIS_DO_NINHO_MAX_Y = 523
DEPOIS_DO_NINHO_MIN_X = 7065
DEPOIS_DO_NINHO_MAX_X = 7082

list_boss_alive = []

def follow_path(path_array):
    ClearBadLocationList()
    #SetGoodLocation(startX,startY)
    SetMoveThroughCorner(True)
    SetMoveOpenDoor(True)
    SetMoveThroughNPC(0)
    SetMoveCheckStamina(0)
    for path in path_array:
        NewMoveXY(path[0], path[1], True, 0, True)

def goto_passaro():
    if not PASSARO_ONLY:
        #moongate event info
        mg_gump = 0x11775c2e
        mg_id = 0x43b84350
        
        
        
        #reaching moongate event
        while (GetX(Self()) != GetX(mg_id) and GetY(Self()) != GetY(mg_id)):
            NewMoveXY(GetX(mg_id), GetY(mg_id), True, 0, True)
        
        #entering moongate event
        UseObject(mg_id)
        Wait(1000)
        wait_gump_and_press_btn(mg_gump, 1)
        Wait(1000)
        if GumpExists(mg_gump):
            wait_gump_and_press_btn(mg_gump, 1,15)
        print("Entrando no gate")

        print("Indo Até o Boss no gate")
        follow_path(OTHER_BOSS)
    else:
        #moongate event info
        mg_gump = 0x11775c2e
        mg_id = 0x43b84350
        
        
        
        #reaching moongate event
        while (GetX(Self()) != GetX(mg_id) and GetY(Self()) != GetY(mg_id)):
            NewMoveXY(GetX(mg_id), GetY(mg_id), True, 0, True)
        
        #entering moongate event
        UseObject(mg_id)
        Wait(1000)
        wait_gump_and_press_btn(mg_gump, 1)
        Wait(1000)
        if GumpExists(mg_gump):
            wait_gump_and_press_btn(mg_gump, 1,15)
        print("Entrando no gate")
        
        follow_path(PASSARO_PATH)
        
        SetFindDistance(4)
        SetFindVertical(20)
        FindType(0x1AD4,Ground())
        if FindItem():
            print("VAI CLICAR NO NINHO")
            UseObject(FindItem())
            Wait(1000)
            NewMoveXY(7079, 518, True, 0, True)
            SetFindDistance(15)
            SetFindVertical(20)
            while not FindType(0x3818,Ground()):
                Wait(50)
            
            energyX = GetX(FindItem())
            energyY = GetY(FindItem())
            i = 0
            while GetX(Self()) > DEPOIS_DO_NINHO_MIN_X and GetX(Self()) < DEPOIS_DO_NINHO_MAX_X and GetY(Self()) > DEPOIS_DO_NINHO_MIN_Y and GetY(Self()) < DEPOIS_DO_NINHO_MAX_Y:
                i = i + 1
                if i > 9:
                    print("****FUDEU**** NÂO CONSEGUI PASSAR PELO RAIO!!!!")
                    break
                ClearBadLocationList()
                y_to_go = energyY - i
                if y_to_go >= DEPOIS_DO_NINHO_MIN_Y: 
                    NewMoveXY(7079, y_to_go, True, 0, True)
                    NewMoveXY(energyX, energyY, True, 0, True)
                if not (GetX(Self()) >= DEPOIS_DO_NINHO_MIN_X and GetX(Self()) <= DEPOIS_DO_NINHO_MAX_X and GetY(Self()) >= DEPOIS_DO_NINHO_MIN_Y and GetY(Self()) <= DEPOIS_DO_NINHO_MAX_Y):
                    print("CHEGUEI NO BOSS!!! PORRA GRIFO!")
                    break
                else:
                    if y_to_go <= DEPOIS_DO_NINHO_MAX_Y:
                        y_to_go = energyY + i
                        NewMoveXY(7079, y_to_go, True, 0, True)
                        NewMoveXY(energyX, energyY, True, 0, True)

            #NewMoveXY(GetX(FindItem()), 518, True, 0, True)
            #NewMoveXY(GetX(FindItem()), GetY(FindItem()), True, 0, True)

            follow_path(PATH_DEPOIS_DO_RAIO)

def msg_disco(msg):
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_HTOWN, content=str(msg))
    webhook.execute()
    return

# =======================================================================
# EVENT AREA UTILS
# =======================================================================
EVENTAREA_X_TOP_LEFT = 5993
EVENTAREA_Y_TOP_LEFT = 899
EVENTAREA_X_BOTTOM_RIGHT = 6044
EVENTAREA_Y_BOTTOM_RIGHT = 945

def check_event_area():
    global timer_warning_check
    currentX = GetX(char)
    currentY = GetY(char)
    if (currentX >= EVENTAREA_X_TOP_LEFT) and (currentX <= EVENTAREA_X_BOTTOM_RIGHT):
        if (currentY >= EVENTAREA_Y_TOP_LEFT) and (currentY <= EVENTAREA_Y_BOTTOM_RIGHT):
            ########### WARNING TIMER CHECK #############
            if datetime.now() >= timer_warning_check + timedelta(seconds=WARNING_MSG_COOLDOWN):
                timer_warning_check = datetime.now()
                PlayWav(ALARM)
                send_discord_message(DISCORD_WEBHOOK_HTOWN,'**HALLOWEEN** | **[BOT:** ' + CharName() + '**] ->** movido para gate de entrada ! ' + GetName(FindItem()))
            return True
    else:
        return False

#################################################################
# JAIL UTILS
#################################################################
JAIL_X_TOP_LEFT = 5270
JAIL_Y_TOP_LEFT = 1160
JAIL_X_BOTTOM_RIGHT = 5310
JAIL_Y_BOTTOM_RIGHT = 1190

def check_in_jail():
    currentX = GetX(char)
    currentY = GetY(char)
    if (currentX >= JAIL_X_TOP_LEFT) and (currentX <= JAIL_X_BOTTOM_RIGHT):
        if (currentY >= JAIL_Y_TOP_LEFT) and (currentY <= JAIL_Y_BOTTOM_RIGHT):
            PlayWav(ALARM)
            send_discord_message(DISCORD_WEBHOOK_HTOWN,'**HALLOWEEN** | **[BOT:** ' + CharName() + '**] ->** movido para Jail ! ' + GetName(FindItem()))
            exit()
            return True
    else:
        return False



def find_boss(range=18):
    global list_boss_alive

    names_mobs = ['Gravedigger','Jack The Ripper','The Gravedigger','Headless Horseman','A Costumed Orc Champion','Freddy Krueger','Helda','Araneam','Britomartis','A Steaming Heap','Peinsluth','A Pumpkin Lord','Mr. Hyde','Wraith High Priest','The Guardian of The Asylum','Clawser Jr','Clawser','A Noxious Gas Cloud','Gomez', 'Terror', 'Suspicion', 'Panic', 'Paranoia', 'Despair', 'Revulsion']
    types_mobs = [0x190, 0x191, 0x2df, 0x29b, 0x2d5, 0xf, 0x53, 0x10b, 0x33e, 0x13e, 0x1e, 0x49, 0x111, 0x0109, 0x0315, 0x00A8, 0x0309, 0x02E6, 0x02C0]

    SetFindDistance(range)

    for type in types_mobs:
        if FindType(type, Ground()) > 0:
            for name in names_mobs:
                if GetName(FindItem()).lower().find(name.lower()) >= 0:
                    if FindItem() not in list_boss_alive:
                        list_boss_alive.append(FindItem())
                        send_discord_message(DISCORD_WEBHOOK_HTOWN,'**HALLOWEEN** |' + CharName() + ' **>>** ' + '**Boss is UP:** ' + GetName(FindItem()) + " " + str(FindItem()) )
                        UOSay('\\'+str(CharName() + ' >> ' + 'Boss is UP: ' + GetName(FindItem())))
                        PlayWav(ALARM)
                        return True
    return False


def check_arty():
    arties = [0x1f03,0x2f58,0x1087]
    for i in arties:
        if FindType(i, Backpack()):
            if 'Conjurer' in GetTooltip(FindItem()) and 'Insured' not in GetTooltip(FindItem()) and 'Blessed' not in GetTooltip(FindItem()):
                #checar se realmente começa com 0
                CancelTarget()
                RequestContextMenu(Self())
                Wait(500)
                SetContextMenuHook(Self(), 3)
                Wait(1000)
                if TargetPresent():
                    TargetToObject(FindItem())
                    Wait(2000)
                    CancelTarget()
                    msg = '**HALLOWEEN** | + @here ' + CharName() + ' received an arty'
                    msg_disco(msg)  
            else:
                Ignore(FindItem())
    return

def check_buff(buff):
    if '\'Attribute_ID\': {}'.format(buff) in str(GetBuffBarInfo()):
        return True
    return False

def survive():
    while True:
        if GetHP(Self()) < GetMaxHP(Self())*0.9 or IsPoisoned(Self()):
            if not check_buff('1069'):
                WaitTargetObject(Self())
                UseType(0xe21, 0x0000)   
                if TargetPresent:
                    TargetToObject(Self()) 
                Wait(2000)

        if GetStam(Self()) < GetMaxStam(Self())*0.7:
            Cast('Divine Fury')
            Wait(2000)        
        Wait(100)
    return

def attack_boss():
    global list_boss_alive
    #setando o primeiro boss como target
    bossID = list_boss_alive[0]
    
    #se tiver mais de um boss próximo, pega o mais próximo e ataca
    if len(list_boss_alive) > 1:
        for boss in list_boss_alive:
            if GetDistance(bossID) == -1 or (GetDistance(boss) < GetDistance(bossID) and GetDistance(boss) != -1):
                bossID = boss 
        
    #verificando se não há boss para atacar
    if GetDistance(bossID) == -1:
        print("There's no boss to attack!")
        list_boss_alive = []
        return
    
    print("Ataccking Boss: " , GetTooltip(bossID), str(bossID) + " distance: " + str(GetDistance(bossID)) + " HP: " + str(GetHP(bossID)))
    UsePrimaryAbility()
    Attack(bossID)
    Wait(50)
    
    if bossID != None and IsDead(bossID) == False and GetDistance(bossID) > 10:
        if GetSkillValue('Archery') >= 100:
            newMoveXY(GetX(bossID), GetY(bossID), True, 9, True)
        elif GetSkillValue('Mace Fighting') >= 100 or GetSkillValue('Swordsmanship') >= 100 or GetSkillValue('Fencing') >= 100:     
            newMoveXY(GetX(bossID), GetY(bossID), True, 1, True)
            
    if bossID != None and IsDead(bossID) == False and GetDistance(bossID) <= 2:
        keepDistance(bossID,6)
    if not check_buff('1082'):
        Cast('Consecrate Weapon')
        Wait(600)

    if not check_buff('1010'):
        Cast('Divine Fury')
        Wait(600)

    if not check_buff('1011'):   
        Cast('Enemy Of One')
        Wait(600)
    return


def keepDistance(ObjID,minDistance = 5):
    global charX 
    global charY 
    global charZ
    ClearBadLocationList()
    SetMoveBetweenTwoCorners(0)
    SetMoveCheckStamina(0)
    SetMoveThroughCorner(0)
    SetMoveThroughNPC(0)
    ClickOnObject(ObjID)
    foundDestination = False
    distance = GetDistance(ObjID)
    while distance < minDistance:
        foundDestination=False
        ClearBadLocationList()
        ClearBadObjectList()
        #checking for traps and setting it as bad locations
        #SettingTrapsAsBadLocations()

        objX = GetX(ObjID)
        objY = GetY(ObjID)
        if objX <=0 and objY <=0:
            #ClientPrintEx(Self(), 66, 1, "object not found. returning")
            return
        charX = GetX(Self())
        charY = GetY(Self())
        charZ = GetZ(Self())
        #objDirection = CalcDir(currX, currY, objX, objY)
        #opositeDirection = objDirection + 4
        #if (objDirection >= 4):
        #    opositeDirection = objDirection - 4
        #toX,toY = calculateCoordsBasedOnDirection(objX,objY,opositeDirection,minDistance)
        #Debug
        #ClientPrintEx(Self(), 66, 1, "SelfX:"+str(charX)+". SelfY:"+str(charY))
        #ClientPrintEx(Self(), 66, 1, "Distance:"+str(distance))
        #ClientPrintEx(Self(), 66, 1, "minDistance:"+str(minDistance))
        #ClientPrintEx(Self(), 66, 1, "Distance:"+str(distance))
        #print("Direction:"+str(objDirection))
        #print("Oposite:"+str(opositeDirection))
        
        while not foundDestination:
            if minDistance < 1:
                print("ABORT! Could not keep a minimal distance!")
                return
            circunferenceCoords = sortByDistance(generateCircunferenceCoordsArray(objX,objY,minDistance))
            destX, destY = findDestination(circunferenceCoords)
            if destX > -1:
                foundDestination = True
            else:
                print("Can't keep min distance of "+str(minDistance)+". Trying distance "+str(minDistance-1))
                minDistance = minDistance - 1
        
        #ClientPrintEx(Self(), 66, 1, "toX:"+str(destX)+". toY:"+str(destY))
        #ClientPrintEx(Self(), 66, 1, "HP:"+str(GetHP(Self())))
        if foundDestination:
            NewMoveXY(destX, destY, True, 0, True)
            #ClientPrintEx(Self(), 66, 1, "currDistance:"+str(GetDistance(ObjID)))
        #ClientPrintEx(Self(), 66, 1, "--------------------")
        distance = GetDistance(ObjID)

import math
def normal_round_based_on_coords(centerX,centerY,nX,nY):
    #round number for a "outer coord" using center coord as reference.
    if nX < centerX and nY < centerY:
        return math.floor(nX),math.floor(nY)
    if nX < centerX and nY > centerY:
        return math.floor(nX),math.ceil(nY)
    if nX > centerX and nY > centerY:
        return math.ceil(nX),math.ceil(nY)
    if nX > centerX and nY < centerY:
        return math.ceil(nX),math.floor(nY)
    #print("nao retornou. cx:"+str(centerX)+". cy:"+str(centerY)+". nx:"+str(nX)+". ny:"+str(nY))
    return round(nX),round(nY)


def generateCircunferenceCoordsArray(centerX,centerY,radius):
    #BUG:
    #Alguns pontos são mais longes (principalmente nos cantos) deveriam são considerados como distância maior, mais aqui estão como se estivessem como a distância certa. Isso fica evidente para raio 3 ou 4.
    #Se eu removo os da ponta, funciona para raio 3, mas não funciona para raio 4 pra cima.
    #Para corrigir, talvez tenha que ser levado em consideração a diferença entre coords X e Y usando a função abs. Similar ao que tem no stealth na função Dist
    arrayOfPoints = []
    topLeft     = 0
    topRight    = 0
    bottomLeft  = 0
    bottomRight = 0
    arraysOfRoundedPoints = []
    arraysOfInvalidDistance = []

    numberOfPoints = radius * 8
    for i in range(0,numberOfPoints+1):

        #xt= radius * math.cos(angle) + Xinicial
        #yt= radius * math.sin(angle) + Yinicial

        xt= radius * math.cos(2*math.pi/numberOfPoints*i) + centerX
        yt= radius * math.sin(2*math.pi/numberOfPoints*i) + centerY
        #For debug purpose
        #print ("X:"+str(xt)+". Y:"+str(yt) + ". roundX:"+str(math.ceil(xt))+" roundY:"+str(math.ceil(yt)))
        tempArray = [xt, yt]
        arrayOfPoints.append(tempArray)
        #For debug purpose
  
        roundedX, roundedY = normal_round_based_on_coords(centerX,centerY,xt,yt)
        tempRoundedArray = [roundedX, roundedY]
        if tempRoundedArray not in arraysOfRoundedPoints:
            if Dist(roundedX,roundedY,centerX,centerY) == radius:
                arraysOfRoundedPoints.append(tempRoundedArray)
            #For debug Purpose
            else:
                arraysOfInvalidDistance.append(tempRoundedArray)

    return arraysOfRoundedPoints

#For Python 3
def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
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

def sortByStealthDistance(x,y):
    firstDistance = Dist(charX,charY,x[0],x[1])
    secondDistance = Dist(charX,charY,y[0],y[1])
    #print("SORT. first:"+str(firstDistance)+". second:"+str(secondDistance))
    return firstDistance - secondDistance

def findDestination(coordsToCheck):
    #print(coordsToCheck)
    #print(charX)
    for coord in coordsToCheck:
        if IsWorldCellPassable (charX, charY, charZ, coord[0], coord[1], WorldNum())[0]:
            #Checking if there's a trap on the destination coord.
            objOnCoord = FindAtCoord(coord[0], coord[1])
            #if not GetType(objOnCoord) in TRAPS_TYPES:
            return coord[0], coord[1]
    return -1, -1

def sortByDistance(arrayOfPoints):
    #arrayOfPoints.sort(key = lambda p: sqrt((p.centerX - centerX)**2 + (p.centerY - centerY)**2))
    #Python 2:
    #return sorted(arrayOfPoints, cmp=sortByStealthDistance)
    #Ptyhon 3:
    from functools import cmp_to_key
    return sorted(arrayOfPoints, key=cmp_to_key(sortByStealthDistance))

def check_boss_and_attack():
    while True:
        while Connected():         
            checkGMGump("EventBOT")
            check_arty()      
            check_in_jail()   
            if check_event_area():
                goto_passaro()
            boss = find_boss()    
            if len(list_boss_alive) > 0: 
                attack_boss()  
                if Dead():
                    msg = '**HALLOWEEN** | + @here ' + CharName() + ' is dead'
                    msg_disco(msg)
                    exit()
            elif not check_buff('1012'): 
                UseSkill('Hiding')  
                SetWarMode(True)
                Wait(1000)       
            Wait(200) 

        while not Connected():
            AddToSystemJournal('Reconnect')
            Connect()
            Wait(10000)

if __name__ == '__main__':
    AddToSystemJournal('Start')
    SetFindDistance(25)
    SetFindVertical(10)  
    SetMoveThroughNPC(0)
    SetMoveCheckStamina(0) 
    SetMoveOpenDoor(True)
    
    survive_thread = threading.Thread(target=survive)
    survive_thread.start()
    check_boss_and_attack()      
    
