try:
    import requests
except ModuleNotFoundError:
    print("No 'requests' module found. Install it using 'pip install requests' ")
    exit()
try:
    from discord_webhook import DiscordWebhook, DiscordEmbed
except ModuleNotFoundError:
    print("No 'discord_webhook' module found. Install it using 'pip install discord_webhook' ")
    exit()

try:
    import PySimpleGUI as sg
except ModuleNotFoundError:
    print("No 'PySimpleGUI' module found. Install it using 'pip install PySimpleGUI' to access the GUI interface.")
    sg = None


from datetime import datetime, timedelta
from time import sleep
from py_stealth import *
from champ_config import *
import threading
import champ_rails


ONRAILS = True
USERESSHELPER = True
USEBAGSENDING =  False

CURSEWEAPON = True
FOLLOW = True
FOLLOWAUT = False
ENEMYOFONE = True
WAV_AFK  =  StealthPath() + 'Scripts\afk.wav'
WAIT_TIME = 500                         #Default Wait Time
WAIT_LAG_TIME = 10000                   #Default Wait Lag Time
TITHING_POINTS_WARNLEVEL = 1000         #Default amount of low TITHING points to warn
TITHING_POINTS_ABORTLEVEL = 150         #Default amount of low TITHING points to abort
TITHING_COOLDOWN_IN_MINUTES = 1         #Default Cooldown time for check TITHING points 
DURABILITY_COOLDOWN_IN_MINUTES = 1      #Default Cooldown time for check durability  

BOSS_TYPES = [0x190, 0x191, 0x00AD, 0x00AC, 0x00AE, 0xAF]
NPC_TYPES = [0x0190, 0x0191]

timer_evasion = datetime.now()- timedelta(seconds=20)
timer_start_boss = datetime.now() 


def IsActivatedBufficon(spell,timer_start=datetime.now()):    
    bufficon = BuffIcons.get(spell)
    info = GetBuffBarInfo() 
    for icon in info: 
        if(icon.get("Attribute_ID") == bufficon):  
            if(bufficon == 1082):   
                consecrate_start = icon.get("TimeStart")   
                if (timer_start > consecrate_start + timedelta(seconds=8) ):
                    return False
                else:
                    return True
            if(bufficon == 1011):
                enemy_of_one_start = icon.get("TimeStart")  
                if (enemy_of_one_start < timer_start):
                    return False
                else:
                    return True
            else:
                return True
    return False  

def CastConfidence(hp = 0.8, force = False):
    if GetSkillValue('Bushido') >= 65 and GetHP(Self()) < GetMaxHP(Self())*hp and (not IsActivatedBufficon('Confidence')  or force):  
        Cast('Confidence')
        Wait(500)

def CastCounterAttack():
    if GetSkillValue('Bushido') >= 80 and not IsActivatedBufficon('Counter Attack') and not IsActivatedBufficon('Evasion') and not IsActivatedBufficon('Blood Oath'):
        Cast('Counter Attack')
        Wait(500)    

def CastCurseWeapon(_lb = 0.3, _ub = 0.85, _mana = 5):
    if not IsActivatedBufficon('Curse Weapon'):
        if GetHP(Self()) > GetMaxHP(Self())*_lb and GetHP(Self()) < GetMaxHP(Self())*_ub and GetMana(Self()) > _mana:
            if FindType(0x2263,Backpack()):
                UseType(0x2263,0x0000)
            elif FindType(0x0F8A,Backpack()): 

                Cast('Curse Weapon')

def findDestination(coordsToCheck):
    #print(coordsToCheck)
    #print(charX)
    for coord in coordsToCheck:
        if IsWorldCellPassable (charX, charY, charZ, coord[0], coord[1], WorldNum())[0]:
            #Checking if there's a trap on the destination coord.
            objOnCoord = FindAtCoord(coord[0], coord[1])
            return coord[0], coord[1]
    return -1, -1

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

def sortByStealthDistance(x,y):
    p = [charX,charY]
    q = [x[0],x[1]]
    firstDistance = math.dist(p, q)
    p = [charX,charY]
    q = [y[0],y[1]]
    secondDistance = math.dist(p, q)
    #print("SORT. first:"+str(firstDistance)+". second:"+str(secondDistance))
    return firstDistance - secondDistance


def sortByDistance(arrayOfPoints):
    #arrayOfPoints.sort(key = lambda p: sqrt((p.centerX - centerX)**2 + (p.centerY - centerY)**2))
    #Python 2:
    #return sorted(arrayOfPoints, cmp=sortByStealthDistance)
    #Ptyhon 3:
    from functools import cmp_to_key
    return sorted(arrayOfPoints, key=cmp_to_key(sortByStealthDistance))  
                
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
    while distance < minDistance and GetHP(Self()) <= GetMaxHP(Self())*0.4: 
        if IsActivatedBufficon('Blood Oath'):
            SetWarMode(False)
        else:
            mob_nearby = get_mobs_nearby()
            Attack(mob_nearby)
        foundDestination=False
        ClearBadLocationList()
        ClearBadObjectList()
        #checking for traps and setting it as bad locations
        SettingTrapsAsBadLocations()

        objX = GetX(ObjID)
        objY = GetY(ObjID)
        if objX <=0 and objY <=0:
            #ClientPrintEx(Self(), 66, 1, "object not found. returning")
            return
        charX = GetX(Self())
        charY = GetY(Self())
        charZ = GetZ(Self())
        
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
        CastCurseWeapon(0.2,0.95,5)

def get_nearby_mobs(
    distance=20,
    mob_types_to_ignore=[],
    notoriety_list=[3, 4, 5, 6],
    lure_distant_enemies=False,
):
    if not Dead():
        SetFindDistance(distance)
        SetFindVertical(30)
        Ignore(char)

        mobs = []
        for notoriety in notoriety_list:
            if FindNotoriety(-1, notoriety):
                mobs += GetFindedList()
                # for mob in mobs:
                #     mob_name = GetAltName(mob)
                #     debug("%s" % (mob_name))

        # se achou algo a gente filtra pra devolver o mais proximo
        if len(mobs) > 0:
            return mobs
        else:
            if FindTypesArrayEx(NPC_TYPES, [0xFFFF], [Ground()], False):
                # debug("PEGOU POR NPC_TYPES")
                Wait(1000)
                mobs += GetFindedList()
                if len(mobs) > 0:
                    return mobs
    return []

def cast_vampiric_embrace():
    VAMPIRIC_EMBRACE_SCROLL = 0x226C
    starttime = datetime.now()
    if GetColor(Self()) != 33918 and GetSkillValue("Necromancy") >= 99:
        while GetMana(Self()) < 21:
            if datetime.now() >= starttime+timedelta(minutes=10000):
                print("Waiting for mana to cast Vampiric Embrace")
                starttime = datetime.now()
            Wait(500)
        while GetColor(Self()) != 33918:
            print("Char is not in Vampire form! Turning...")
            if FindType(VAMPIRIC_EMBRACE_SCROLL, Backpack()):
                UseType(VAMPIRIC_EMBRACE_SCROLL)
                Wait(3000)
            else:
                Cast("Vampiric Embrace")
                Wait(3000)
    if GetColor(Self()) == 33918:
        print("Turned into Vampire.")

def wait_lag(wait_time=WAIT_TIME, lag_time=WAIT_LAG_TIME):
    Wait(wait_time)
    CheckLag(lag_time)
    return

def MyDress():
    for j in range(len(Armor_Item_Layers)):
        while (ObjAtLayer(Armor_Item_Layers[j]) != Armor_Item_List[j]):
            if UnEquip(Armor_Item_Layers[j]):
                wait_lag(1000)
            if Armor_Item_Layers[j] == LhandLayer() or Armor_Item_Layers[j] == RhandLayer():
                UnEquip(LhandLayer())
                wait_lag(1000)
                UnEquip(RhandLayer())
                wait_lag(1000)
            print("EQUIPING. Item: " + str(j) + " layer:" + str(Armor_Item_Layers[j]) + " item:" + str(Armor_Item_List[j]))
            if not Equip(Armor_Item_Layers[j], Armor_Item_List[j]):
                try:
                    raise Exception('')
                except:
                    print("ERROR! Could not find object to equip. Check your set.")    
                    exit()
                            
            wait_lag(1000) 

def save_set():
    global Armor_Item_List
    hat = neck = sleeves = chest = legs = gloves = lhand = ring = brace = robe = shoes = talisman = cloak = ear = rhand = waist = torsoH = shirt = eggs = 0
    Armor_Item_List = [hat,neck,sleeves,chest,legs,gloves,lhand,ring,brace,robe,shoes,talisman,cloak,ear,rhand,waist,torsoH,shirt,eggs]
     
    for layer_i in range(len(Armor_Item_Layers)):
        if ObjAtLayer(Armor_Item_Layers[layer_i]) > 0:
            Armor_Item_List[layer_i] = ObjAtLayer(Armor_Item_Layers[layer_i]) 
    return 

def DressLRCSet():
    for key, val in LRC_SET.items():
        if val != 0:
            while (ObjAtLayer(key()) != val):
                if (ObjAtLayer(key()) != val):
                    if UnEquip(key()):
                        wait_lag(1000)
                if key() == LhandLayer() or key() == RhandLayer():
                    UnEquip(LhandLayer())
                    wait_lag(1000)
                    UnEquip(RhandLayer())
                    wait_lag(1000)
                     
                print("EQUIPING. Item: " + str(val) + " layer:" + str(key()))
                if not Equip(key(),val):                                                             
                    try:
                        raise Exception('')
                    except:
                        print("ERROR! Could not find LRC object to equip. Check your LRC set.")    
                        exit()
                wait_lag(1000)

def initial_check():
    if GetColor(Self()) != 33918 and not Dead(): 
        DressLRCSet()
        Wait(1000)
        #Casting Vampiric Embrace 
        cast_vampiric_embrace()    
        MyDress()

def checktithingPoints():
    tp = GetExtInfo()['Tithing_points']
    global last_tithingpoints_check
    if datetime.now() >= last_tithingpoints_check + timedelta(minutes=TITHING_COOLDOWN_IN_MINUTES):
        last_tithingpoints_check = datetime.now()
        if tp < TITHING_POINTS_ABORTLEVEL:
            ClientPrintEx(Self(), 66, 1, "### ABORTING!!! TITHING POINTS TOO LOW! ABORTING!!! Current: "+str(tp)+" ###")
        if tp < TITHING_POINTS_WARNLEVEL:
            ClientPrintEx(Self(), 66, 1, "WARNING!!! LOW ON TITHING POINTS!!! Current: "+str(tp))
    if tp < TITHING_POINTS_ABORTLEVEL:
        return False
    if tp < TITHING_POINTS_WARNLEVEL:
        return True

    return True 

class SampireWindow(threading.Thread):
    def __init__(self):
        global sg
        super(SampireWindow, self).__init__(daemon=True)
        self._running = False
        self._window = None  
        if sg is None: 
            self.terminate() 

         
    def finded(self):
        return self._finded
    
    def active(self):
        return self._running 
                 
    def modify_flags(self,event):
        if self._window is None:
            return
        global ONRAILS   
        global USERESSHELPER 
        global USEBAGSENDING
        global GOTOSAFEANDLOGOUT
        if event == '1':
            if ONRAILS:
                self._window.FindElement('1').Update(button_color=('black', 'red'))
                self._window.FindElement('1').Update('OFF')  
                ONRAILS = False
            else:
                self._window.FindElement('1').Update(button_color=('black', 'green'))
                self._window.FindElement('1').Update('ON') 
                ONRAILS = True     
        elif event == '2':
            if USERESSHELPER:
                self._window.FindElement('2').Update(button_color=('black', 'red'))
                self._window.FindElement('2').Update('OFF')  
                USERESSHELPER = False
            else:
                self._window.FindElement('2').Update(button_color=('black', 'green'))
                self._window.FindElement('2').Update('ON') 
                USERESSHELPER = True
        elif event == '2':
            if USEBAGSENDING:
                self._window.FindElement('2').Update(button_color=('black', 'red'))
                self._window.FindElement('2').Update('OFF')  
                USEBAGSENDING = False
            else:
                self._window.FindElement('2').Update(button_color=('black', 'green'))
                self._window.FindElement('2').Update('ON') 
                USEBAGSENDING = True    
        else:
            return
        
    def run(self):
        if sg is None:
            return         
        self._running = True  
        sg.ChangeLookAndFeel('GreenTan')

		# ------ Menu Definition ------ #
        #menu_def = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']], ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],	['&Help', '&About...'], ]    
        

		# ------ Column Definition ------ #
        column1 = [[sg.Text('Column 1', background_color='lightblue', justification='center', size=(10, 1))],
				   [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],
				   [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],
				   [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]

        layout = [
            #[sg.Menu(menu_def, tearoff=True)],
			[sg.Text('Sampirebot for Champ', size=(30, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],  
            [sg.Text('by Astraroth cya Mark and Quark', size=(32, 1), justification='right', font=("Helvetica", 10))],
			[sg.Frame(layout=[
			    [sg.Text('On Rails', size=(36, 1)), sg.Button('ON' if ONRAILS else 'OFF', button_color=('black', 'green' if ONRAILS else 'red'), size=(4, 1), font=("Helvetica", 10) , key='1', tooltip='Enable to lure and kill the DF at the corner position') ], 
                [sg.Text('Select Rails to Run', size=(36, 1)), sg.Combo(['PAPUA','OAK','MARBLE', 'HUMILTY','BEDLAM','VALOR','TERRA_SANCTUM','T2A_PAPUA_DESERT', 'T2A_DAMWIM', 'DESTARD', 'XMAS_CHAMP', 'T2A_HOPPERS', 'DESPISE', 'FIRE', 'DECEIT', 'NEIRA_OLD', 'ICE', 'EVENTO' ],key='dest' )],
                [sg.Text('Select Type Player', size=(36, 1)), sg.Combo(['WHAMMY','SAMPIRE'],key='typeplayer')],
                [sg.Text('Use RessHelper', size=(36, 1)), sg.Button('ON' if USERESSHELPER else 'OFF', button_color=('black', 'green' if USERESSHELPER else 'red'), size=(4, 1), font=("Helvetica", 10) , key='1', tooltip='Enable to lure and kill the DF at the corner position') ], 
                [sg.Text('Enter id from RessHelper'), sg.InputText()]
                [sg.Text('X Position RessHelper'), sg.InputText()]
                [sg.Text('Y Position RessHelper'), sg.InputText()]
                [sg.Text('Send Money with Bag of sending', size=(36, 1)), sg.Button('ON' if USEBAGSENDING else 'OFF', button_color=('black', 'green' if USEBAGSENDING else 'red'), size=(4, 1), font=("Helvetica", 10) , key='1', tooltip='Enable to lure and kill the DF at the corner position') ], 

            ], title=' Flag Options ',title_color='black', relief=sg.RELIEF_SUNKEN)],
            [sg.Text('_' * 50)],
        ]                         
        icone = str(StealthPath())+'Scripts\Dark_Father.ico'                                                                                                         
        self._window = sg.Window('Sampirebot | Char: '+str(CharName()), layout, default_element_size=(40, 1), grab_anywhere=False, icon=icone)  
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = self._window.read()      
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            if event is not None:
                self.modify_flags(event)
            Wait(300)
        self.terminate()

    def terminate(self):     
        print("Closing window")
        self._running = False
        if self._window is not None:
            self._window.close()
        self.__del__()      
    
    def __del__(self):
        print('Thread finished..')  
    

def samp_aux():
    #print("Inicio SAMPIREBOT AUX")
    global last_tithingpoints_check
    global timer_deaths_in_a_row_check 
    honored = False
    room = GetGlobal('char','Room')
    timer_start = datetime.now()      
    SetGlobal('char','Room','Next')
    honored_list = []
    while True:
        if not Dead() and Connected(): 
            while( not Connected()):
                SetARStatus(True)
                SetPauseScriptOnDisconnectStatus(False)
                Wait(1000)
            
            if GetGlobal('char','Room') == "Ress":
                Wait(2000)
                continue
            ########### TITHINGPOINTS CHECK #############
            checktithingPoints()
                
            ########### CHIVALRY SPELLS ############
            if GetSkillValue('Chivalry') >= 60: 
                # ENEMY OF ONE
                 if not IsActivatedBufficon('Enemy of One',timer_start) and GetMana(Self()) >= 14:
                    Cast('Enemy of One')   
                    Wait(300)
            
            if GetStam(Self()) < 20:
                Cast('Divine Fury')
                Wait(600)
            CastConfidence(0.7)    
            #### HONOR ##### 
            if USEHONOR and not honored: 
                if honorMob(honored_list) == 0:
                    honored = True
            ##checkGMGump('Doom')
            ##checkIfInJail('Doom')                
            ##is_gm_present()

            Wait(200)
            ########### LOW DURABILITY CHECK #############
            if datetime.now() >= last_durability_check + timedelta(minutes=DURABILITY_COOLDOWN_IN_MINUTES):
                if checkIfEqpOnLowDurability() is not False:
                    SetGlobal('char','lowDurability',True)
                else:
                    SetGlobal('char','lowDurability',False)

def SampireBot(Rails):    
    if Dead():
        return GetX(Self()), GetY(Self())
    # reset corpse ids
    IgnoreReset()   
    # timer for enemy_of_one
    global timer_start_boss
    # timer for evasion
    global timer_evasion
    global FOLLOWAUT   
    # timer for special move
    timer_sm = datetime.now()

    rail = Rails
    
    #tries = 0  
    n = 0
    enemy = 0 
    mobdistance = 999           
    enemy = get_nearby_mobs(10, [], 6)
    while len(enemy) > 0:        
        Wait(200)
        if Dead():
            return GetX(Self()), GetY(Self())
        if (len(enemy) == 0 and FOLLOWAUT):
            if(not IsActivatedBufficon('Enemy of One',timer_boss4+timedelta(seconds=10))) and GetMana(Self()) > 14:
                #n = tries // len(rail)
                pos = rail[n]                
                print("going to rail pos: " + str(pos[0]) + " " + str(pos[1]) + " n: " + str(n))
                NewMoveXY(pos[0],pos[1], False,1,True)
                timer_boss4 = datetime.now()
                mana_before = GetMana(Self())   
                Cast('Enemy of One')   
                Wait(1000)   
                print(" mana before: "+ str(mana_before) + " mana atual: " + str(GetMana(Self())))                
                if mana_before <= GetMana(Self()):
                    pass
                else:
                    n = n + 1
                if n >= len(rail):
                    n = 0
        
        if (len(enemy) != 0):   
            n = 0
            if datetime.now() >= timer_sm+timedelta(seconds=3) or GetMana(Self()) >= 20 and IsActivatedBufficon('Consecrate Weapon',datetime.now()):   
                UsePrimaryAbility()
                timer_sm = datetime.now()   
            else:
                if not IsActivatedBufficon('Lightning Strike') and GetMana(Self()) >= 10:
                    Cast("Lightning Strike")
            
            Attack(enemy)
            
            if (FOLLOW and not danger):
                NewMoveXY(GetX(enemy),GetY(enemy), False,1,True) 
            
            if (GetHP(Self()) < GetMaxHP(Self())*0.4 and not Dead()):
                if not IsActivatedBufficon('Curse Weapon'):
                    print("DANGER!! MOVING AWAY!")
                    keepDistance(enemy,10)
                danger = True
                priority = False
                if not IsPoisoned(Self()):
                    CastConfidence(0.7)
                    CastConfidence(0.5,True)
            else:
                danger = False 
            ########### CHIVALRY SPELLS ############
            if GetSkillValue('Chivalry') >= 60: 
                # ENEMY OF ONE
                if ENEMYOFONE:  
                    if (not IsActivatedBufficon('Enemy of One',timer_start_boss) or GetNotoriety(enemy) != 5) and GetMana(Self()) >= 14 and not IsHidden(enemy) and GetDistance(enemy) < 2:
                        Cast('Enemy of One')   
                        Wait(200)                                                                  
                   
                # CONSECRATE WEAPON
                if (not IsActivatedBufficon('Consecrate Weapon',datetime.now())) and (GetMana(Self()) >= 8) and (mobdistance < 4) and not (IsHidden(enemy)):
                    Cast('Consecrate Weapon')                                               
                    Wait(200)                                                               
                                           
                if IsActivatedBufficon('Consecrate Weapon',datetime.now()):
                    priority = False
                else:
                    priority = True      
                                         
                # DIVINE FURY
                if not IsActivatedBufficon('Divine Fury') and GetMana(Self()) >= 12 and not priority:
                    Cast('Divine Fury')
                    Wait(600)  
                if GetStam(Self()) < 90 and GetMana(Self()) >= 12 and not priority:
                    Cast('Divine Fury')
                    Wait(600)  
                if GetStam(Self()) < GetMaxStam(Self())*0.4 and GetMana(Self()) >= 12:
                    Cast('Divine Fury')
                    Wait(600)            
             
            ########### CURSE WEAPON ############    
            if CURSEWEAPON and GetDistance(enemy) < 2:    
                CastCurseWeapon()       
            
            ########### BUSHIDO SPELLS #############
            CastConfidence(0.6)
            CastCounterAttack()                   
            CastConfidence(0.4,True)
            

    return GetX(Self()), GetY(Self())
    

if __name__ == '__main__':
    print("-----------------------------------------------")
    print("-----------------------------------------------")
    print("---- Running SAMPIREBOT by Astraroth cya Mark and Quaker ----")
    print("-----------------------------------------------")
    print("-----------------------------------------------")
    samp_aux_thread = threading.Thread(target=samp_aux, daemon=True)
    samp_aux_thread.start()

    menu_thread = SampireWindow()
    menu_thread.start() 

    save_set()
    initial_check()
    SampireBot(champ_rails.PAPUA, 5)
    if Dead():
        PlayWav(WAV_AFK)
        while Dead():
            Wait(1000)
    Wait(1000)
