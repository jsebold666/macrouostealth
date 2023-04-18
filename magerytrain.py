from py_stealth import *
from datetime import datetime
magery_cap = GetSkillCap('Magery')

def buff_exists_(name, timer_start=datetime.now()):
    if not name:
        return
    buffs = GetBuffBarInfo()
    for buff in buffs:
        buffname = GetClilocByID(buff['ClilocID1']) 
        if name.upper() in buffname.upper():
            return True
    return False
    
    
class SpellInfo:
    def __init__(self, name, mana_cost, min_skill, target = Self()):
        self.name = name
        self.mana_cost = mana_cost
        self.min_skill = min_skill
        self.target = target

while True:
    if not Dead():
        if GetSkillValue('Magery') < magery_cap:
        # Set mana and spell cast according to your stats
            spells = [
                SpellInfo('cure', 10, 20),
                SpellInfo('bless', 15, 35),
                SpellInfo('arch cure', 12, 45),
                SpellInfo('magic reflection', 18, 52),
                SpellInfo('invisibility', 30, 61),
                SpellInfo('mana vampire', 40, 85),
                SpellInfo('earthquake', 30, 115)
            ]

        current_spell = None
        for spell in spells:
            if spell.min_skill <= GetSkillValue('Magery'):
                current_spell = spell

        if Mana() >= current_spell.mana_cost:
            Cast(current_spell.name)
            WaitForTarget(5000)
            TargetToObject(current_spell.target)
            print("Your current Skill Magery is: " + str(GetSkillValue('Magery')) + "/" + str(GetSkillCap('Magery')))
            print("Your current Mana is: " + str(GetMana(Self())) + "/" + str(GetMaxMana(Self())))
        else:
            if not buff_exists_('Meditation'):
                UseSkill('Meditation')
                Wait(4000)
            else:
                print('Meditating... rising mana...')
                Wait(7000)
    else:
        StopScript()