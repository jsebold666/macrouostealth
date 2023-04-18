config = {}
config["general_config"] = {
    # general options
    "ore_storage_container": 0,
    "pet_id": 0,
    "skip_bad_runes": True,
    "skip_runes_where_char_was_attacked": True,
    "skip_runes_where_char_died": True,
    "recall_to_escape_attacks": True,
    "wait_home_if_attacked": False,
    "place_to_escape_attacks": "home",
    "discord_webhook_url": "https://discord.com/api/webhooks/967780402922151958/jKDXJeKoeFfOxPCItC9bR0nQbfcDO4ZR505Hi3rLmU0M9oUd2su53K_okHI4Gz-138S7",
    "discord_webhook_afk_url": "https://discord.com/api/webhooks/967780402922151958/jKDXJeKoeFfOxPCItC9bR0nQbfcDO4ZR505Hi3rLmU0M9oUd2su53K_okHI4Gz-138S7",
    "auto_reequip_set": True,
    "auto_refill_tithing_points": True,
    "minimum_tithing_points": 3000,
    # runebook names
    "home_runebook": "Home",
    "ore_runebooks": ["Ore1", "Ore2", "Ore3"],
    # rune positions in Home runebook
    "rune_positions": {"home": 1, "shrine": 2},
    "fast_ecru_mode": False,
}
#########################################
# !!! CHARACTERS SPECIFIC CONFIGURATION !!!
# !!! PUT YOUR CHARS CONFIG HERE !!!
#########################################

config["aaaa"] = {
    "pet_id": 0xac754,
    "forge_id": 0x41a746d3,
    "rune_positions": {"home": 1, "shrine": 2},
    "wait_home_if_attacked": True
}

