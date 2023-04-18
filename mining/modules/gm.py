# ===================================================================
# GM check Utils
# ===================================================================
gm_names = "John: | Styx: | EOS: | GM controlling: | Larson: | Lyane: | Selene: | Marshall: | CNS Dysis: | CNS Astraeus"
gm_names_array = [
    "EOS:",
    "Larson:",
    "Selene:",
    "GM controlling:",
    "GM Tetra:",
    "Anjo Tetra:",
    "Tycho:",
    "Navrey:",
    "Ancient Wyrm Verde",
    "ORC BRUTE VERMELHO",
    "Samael:",
    "John:",
    "Styx:",
    "Lyane:",
    "CNS Marshall:",
    "CNS Forseti:",
    "CNS Dysis,:",
    "CNS Astraeus",
]

gm_msgs = [
    "here?",
    "attending",
    "hey",
    "hi",
    "ATTENDANCE CHECK!! IF YOU ARE ATTENDED",
]


def is_gm_present():
    if InJournal(gm_names) > -1:
        ClearJournal()
        return True
    else:
        return False


# def perform_routine_checks():
#     checkGMGump("lumber")
#     check_if_in_jail("lumber")
#     check_and_handle_world_save()
