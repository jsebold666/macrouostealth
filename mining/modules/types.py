#!/usr/bin/env python3

# =======================================================================
# ITEM TYPES
# =======================================================================

ANY_TYPE = 0xFFFF
ANY_COLOR = 0xFFFF

CORPSE = 0x2006
GATE = 0xF6C
BANDAGE_TYPE = 0xE21

PLAYER_TYPES = [
    0x190,  # human males
    0x191,  # human females
    0x2E8,  # elven males
]

HUMANOIDS = [
    0x190,  # human males
    0x191,  # human females
    0x2E8,  # elven males
]

# tools
TINKER_TOOLS = 0x1EB8
SHOVEL = 0x0F39
SMALL_FORGE_TYPE = 0xFB1

# weapons
DOUBLE_AXE = 0xF4B


# monsters / mobs / pets

PETS = [0xB3, 0x317]  # nightmares  # swamp dragons


COMMODITY_DEED_BOX_SOUTH = 0x9AA
COMMODITY_DEED_BOX_EAST = 0xE7D
COMMODITY_DEED_BOX_COLOR = 71


# resources and materials
BOARD = 0x1BD7
INGOT = 0x1BF2

GOLD = 0xEED
CHECK = 0x14F0
CHECK_COLOR = 52

ROBE = 0x1F03
DEATH_ROBE_COLOR = 2301

ORE = 0x19B9
ORES = [
    0x19BA,
    0x19B7,
    0x19B8,
    0x19B9,
]


# reagents
PIG_IRON = 0x0F8A
VAMPIRIC_EMBRACE_SCROLL = 0x226C
CURSE_WEAPON_SCROLL = 0x2263

POISON_POTION = 0x0F0A
REFRESH_POTION = 0x0F0B
HEAL_POTION = 0x0F0C
EXPLOSION_POTION = 0x0F0D
CONFLAGRATION_POTION = 0x0F06
CURE_POTION = 0x0F07
AGILITY_POTION = 0x0F08
STRENGTH_POTION = 0x0F09
GRAPES_OF_WRATH = 0x2FD7
SMOKE_BOMB = 0x2808
ENCHANTED_APPLE = 0x2FD8
ORANGE_PETAL = 0x1021
BOLA = 0x26AC

ARROW = 0xF3F
COMPOSITE_BOW = 0x26C2

# general items
ALCHEMICAL_SYMBOL_TYPE = 0x1822
POF = 0x1006
BAG = 0xE76
CHAMPION_SKULL = 0x1F18

# ANKH_TYPE_LEFT = 0x2
# ANKH_TYPE_RIGHT = 0x3
#
ANKH_TYPES = [
    0x2,  #
    0x3,  #
    0x5,  #
    0x1E5C,  # ankh of sacrifice south 1-2
    0x1E5D,  # ankh of sacrifice south 2-2
]


# =======================================================================
# ITEM TYPES
# =======================================================================
#
#

SCORPION_TYPE = 0x30  # for miasmas
AGRESSIVE_MOBS = [
    0x5C,  # silver serpents
    0x6C,  # bronze elementals
    0x6B,  # agapite elemental
    0x11,  # orc
    0x21,  # lizardman
    0x4,  # gargoyle
    0x1,  # ogre
    0x36,  # troll
    0x2,  # ettin
    0x9,  # demon
    0x4A,  # imp
    0x16,  # gazer
    0x28,  # balron
    0x2A,  # ratman
    0xB,  # dread spider
    0x1E,  # harpy
    0x1C,  # giant spider
    0xD7,  # giant rat
    0x15,  # giant serpent
    0xD,  # air elemental
    0xA2,  # poison elemental
    0x9F,  # blood elemental
    0x27,  # mongbat
    0x308,  # horde minion
    0x27,  # snake
    0x2F,  # reaper
    0x2E,  # ancient wyrm
    0x18,  # lich
    0x4F,  # lich lord
]

PLAYER_SUMMONS = [
    0xA5,  # wisps
    0x0018,  # common liches
    0x004F,  # lich lords
    0x130,  # flesh golem
    0xE2,  # horse
    0x009A,  # mummy
    0x013F,  # a mound of maggots
    0x0136,  # a wailing banshee but with titan graphic (hz mod client for wraith form)
]

DOUBLE_AXE = 0xF4B

ANY = 0xFFFF
ANY_TYPE = 0xFFFF

# COLOR CONSTANTS
ANY_COLOR = 0xFFFF
DEFAULT = 52
BLACK = 1
DARK_ORANGE = 43
ORANGE = 44
PURPLE = 15
LIGHT_RED = 31
DARK_RED = 33
RED = 40
DARK_PINK = 36
GREEN = 73
LIGHT_GREEN = 75
DARK_GREEN = 77
CYAN = 80
GHOST_BLUE = 1159
TRUE_WHITE = 1153
YELLOW = 52  # 53 is also cool
LIGHT_YELLOW = 54

PLAYER_TYPES = [
    0x190,  # human males
    0x191,  # human females
    0x2E8,  # elven males
]


PET_TYPES = [0xB3, 0x317]  # nightmares  # swamp dragons
BANDAGE_TYPE = 0xE21
NPC_TYPES = [0x190, 0x191]  # female and male npcs
COMMODITY_DEED_BOX_SOUTH = 0x9AA
COMMODITY_DEED_BOX_EAST = 0xE7D
COMMODITY_DEED_BOX_COLOR = 71


CORPSE = 0x2006


BOARD = 0x1BD7
LOG_TYPE = 0x1BDD
GOLD = 0xEED

ROBE_TYPE = 0x1F03
DEATH_ROBE_COLOR = 2301


INGOT = 0x1BF2
SMALL_FORGE = 0xFB1
ORE = 0x19B9
ORE_TYPES = [
    0x19BA,
    0x19B7,
    0x19B8,
    0x19B9,
]

PIG_IRON = 0x0F8A
VAMPIRIC_EMBRACE_SCROLL = 0x226C
CURSE_WEAPON_SCROLL = 0x2263
ALCHEMICAL_SYMBOL_TYPE = 0x1822


HEAL_POTION = 0x0F0C
CURE_POTION = 0x0F07
REFRESH_POTION = 0x0F0B
STRENGTH_POTION = 0x0F09
AGILITY_POTION = 0x0F08
POISON_POTION = 0x0F0A
EXPLOSION_POTION = 0x0F0D
CONFLAGRATION_POTION = 0x0F06
CONFUSION_BLAST_POTION = 0x048D

ENCHANTED_APPLE = 0x2FD8
ORANGE_PETAL = 0x1021
GRAPES_OF_WRATH = 0x2FD7
SMOKE_BOMB = 0x2808
BOLA = 0x26AC

ARROW = 0xF3F
COMPOSITE_BOW = 0x26C2
YUMI = 0x27A5


ORDER_SHIELD = 0x1BC4
CHAOS_SHIELD = 0x1BC3


## LUMBER SCRIPT TYPES (REMOVED FROM SCRIPT FILE CLEANING)

LOG = 0x1BDD
BOARD = 0x1BD7

PARASITIC_PLANT = 0x3190
LUMINESCENT_FUNGI = 0x3191
BRILLIANT_AMBER = 0x3199
BARK_FRAGMENT = 0x318F
SWITCH_TYPE = 0x2F5F

LUMBER_RESOURCES = {
    "boards": {"graphic": 0x1BD7, "color": 0000},
    "oak_boards": {"graphic": 0x1BD7, "color": 2010},
    "ash_boards": {"graphic": 0x1BD7, "color": 1191},
    "heartwood_boards": {"graphic": 0x1BD7, "color": 1193},
    "parasitic_plant": {"graphic": 0x3190, "color": 0},
    "luminescent_fungi": {"graphic": 0x3191, "color": 0},
    "brilliant_amber": {"graphic": 0x3199, "color": 0},
}

SPECIAL_LUMBER_RESOURCES = {
    # colored logs
    "oak_logs": {"graphic": 0x1BDD, "color": 2010},
    "ash_logs": {"graphic": 0x1BDD, "color": 1191},
    "yew_logs": {"graphic": 0x1BDD, "color": 1192},
    "heartwood_logs": {"graphic": 0x1BDD, "color": 1193},
    "bloodwood_logs": {"graphic": 0x1BDD, "color": 1194},
    "frostwood_logs": {"graphic": 0x1BDD, "color": 1151},
    # colored boards
    "oak_boards": {"graphic": 0x1BD7, "color": 2010},
    "ash_boards": {"graphic": 0x1BD7, "color": 1191},
    "yew_boards": {"graphic": 0x1BD7, "color": 1192},
    "heartwood_boards": {"graphic": 0x1BD7, "color": 1193},
    "bloodwood_boards": {"graphic": 0x1BD7, "color": 1194},
    "frostwood_boards": {"graphic": 0x1BD7, "color": 1151},
    # special resources
    "bark_fragment": {"graphic": 0x318F, "color": 0},
    "parasitic_plant": {"graphic": 0x3190, "color": 0},
    "luminescent_fungi": {"graphic": 0x3191, "color": 0},
    "brilliant_amber": {"graphic": 0x3199, "color": 0},
    "switch": {"graphic": 0x2F5F, "color": 0},
}

LUMBER_RESOURCES_TYPES = [
    0x1BD7,  # utils.boards
    0x1BDD,  # utils.logs
    0x318F,  # bark fragment
    0x3190,  # parasitic plant
    0x3199,  # brilliant amber
    0x3191,  # luminescent fungi
    0x2F5F,  # switch
    0xEED,  # ?
]

# Types of axes to lumber
HATCHET = 0xF43
BATTLE_AXE = 0xF43
AXES = {"battle_axe": 0x0F47, "hatchet": 0xF43}

TREES = [
    3274,
    3275,
    3277,
    3280,
    3281,
    3282,
    3283,
    3286,
    3288,  # ceddar tree
    3289,  # ceddar tree
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
    3396,  # a walnut tree
    3415,
    3416,
    3417,
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


SCORPION_TYPE = 0x30  # for miasmas
AGRESSIVE_MOBS = [
    0x5C,  # silver serpents
    0x6C,  # bronze elementals
    0x6B,  # agapite elemental
    0x11,  # orc
    0x21,  # lizardman
    0x4,  # gargoyle
    0x1,  # ogre
    0x36,  # troll
    0x2,  # ettin
    0x9,  # demon
    0x4A,  # imp
    0x16,  # gazer
    0x28,  # balron
    0x2A,  # ratman
    0xB,  # dread spider
    0x1E,  # harpy
    0x1C,  # giant spider
    0xD7,  # giant rat
    0x15,  # giant serpent
    0xD,  # air elemental
    0xA2,  # poison elemental
    0x9F,  # blood elemental
    0x27,  # mongbat
    0x308,  # horde minion
    0x27,  # snake
    0x2F,  # reaper
    0x2E,  # ancient wyrm
    0x18,  # lich
    0x4F,  # lich lord
]
