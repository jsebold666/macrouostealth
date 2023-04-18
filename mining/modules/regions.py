################################################################################
# REGION UTILS
################################################################################

char = Self()
# FORMAT:
# [X_TOP_LEFT, Y_TOP_LEFT, X_BOTTOM_RIGHT, Y_BOTTOM_RIGHT]
DUNGEONS = {
    "destard": [
        5193,
        776,
        5364,
        987,
    ],
    "doom_safe_room": [
        479,
        364,
        501,
        379,
    ],
}
CHAMP_SPAWNS = {
    "t2a_ice_west": [
        5361,
        2326,
        5590,
        2417,
    ],  # safe corner for the cu shide boss in castle
    "t2a_ice_east": [
        5941,
        2353,
        6057,
        2409,
    ],  # safe corner for the cu shide boss in castle
    "t2a_damwin": [
        5217,
        3151,
        5301,
        3202,
    ],  # safe corner for the cu shide boss in castle
    "t2a_hoppers": [
        5890,
        3332,
        6068,
        3542,
    ],  # safe corner for the cu shide boss in castle
    "t2a_papua_desert": [
        5553,
        2819,
        5961,
        3008,
    ],  # safe corner for the cu shide boss in castle
    "marble": [
        1111,
        1111,
        1111,
        1111,
    ],  # safe corner for the cu shide boss in castle
}
CITIES = {
    "delucia": [
        4408,
        4412,
        4485,
        4443,
    ],
    "cove": [
        2208,
        1112,
        2285,
        1243,
    ],
}

MALAS = {
    "bedlam": [
        153,
        1610,
        185,
        1649,
    ],  # safe corner for the cu shide boss in castle
    # dungeons
    "luna_moongate": [
        1011,
        524,
        1021,
        534,
    ],
    "ilshenar_spirituality": [
        1157,
        1137,
        1700,
        1350,
    ],  # safe corner for the cu shide boss in castle
}


OUTLANDS_CITIES = {
    "britain_bank": [
        1414,
        1666,
        1447,
        1699,
    ],
    "outpost": [
        589,
        184,
        638,
        215,
    ],
}
OUTLANDS_SPECIFIC_REGIONS = {
    "outlands_arena": [
        589,
        184,
        638,
        215,
    ],
}

DEMISE_SPECIFIC_REGIONS = {
    "vendor_mall": [
        589,
        184,
        638,
        215,
    ],
    "easter_champ": [
        6396,
        1207,
        6491,
        1291,
    ],  # safe corner for the cu shide boss in castle
    # xmas bosses
    "jack_frost": [
        5906,
        1069,
        5949,
        1120,
    ],
    "christmas_angel": [
        6442,
        1215,
        6667,
        1047,
    ],
    "maugrim": [
        442,
        1466,
        462,
        1488,
    ],
    # sala da white witch fiz igual do maugrim pq eh aqui que o char espera
    "white_witch": [
        6193,
        1138,
        6214,
        1160,
    ],
    "xmas_safe_area": [
        6074,
        1194,
        6089,
        1209,
    ],  # safe corner for the cu shide boss in castle
    # halloween bosses
    "heap": [6087, 1207],
    "clauser": [7036, 531],
    "christmas_carol_entrance_house": [
        6030,
        1167,
        6025,
        1164,
    ],
    "mother_faule_home": [
        5962,
        1177,
        5968,
        1183,
    ],
    "gomez": [5267, 1227],
}

# group all regions into one
REGIONS = {}
for regions in [
    DUNGEONS,
    CITIES,
    DEMISE_SPECIFIC_REGIONS,
    OUTLANDS_SPECIFIC_REGIONS,
    OUTLANDS_CITIES,
]:
    REGIONS.update(regions)


def in_region(region_name):
    if region_name not in REGIONS:
        #debug("regions.in_region(): Region {region_name} is not yet catalogued.")
        return False

    region_coords = REGIONS.get(region_name)
    currentX = GetX(char)
    currentY = GetY(char)
    x_top_left = region_coords[0]
    y_top_left = region_coords[1]
    x_bottom_right = region_coords[2]
    y_bottom_right = region_coords[3]

    if (currentX >= x_top_left) and (currentX <= x_bottom_right):
        if (currentY >= y_top_left) and (currentY <= y_bottom_right):
            return True

    return False
