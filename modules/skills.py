# ###################################################################
# AUTODETECT CHAR TEMPLATES
# ###################################################################


def check_skill(skill_name, skill_value):
    if GetSkillValue(skill_name) >= skill_value:
        return True
    else:
        return False


def is_ninja():
    return check_skill("Ninjitsu", 50)


def is_samurai():
    return check_skill("Bushido", 50)


def is_healer():
    return check_skill("Healing", 50)


def is_shade():
    return check_skill("Hiding", 40)


#
def is_mage():
    return check_skill("Magery", 50)


def is_archer():
    return check_skill("Archery", 50)


def is_paladin():
    return check_skill("Chivalry", 50)


def is_necro_mage():
    if GetSkillValue("Magery") >= 90 and GetSkillValue("Necromancy") >= 60:
        return True
    else:
        return False
