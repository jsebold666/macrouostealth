print("Importing lumber_config.py")

config = {}
config["general_config"] = {
    # general options
    "sell_wood": True,
    "unload_boards_at_bank": True,
    "wood_storage_container": 0,
    "auto_reequip_set": True,
    "auto_refill_tithing_points": True,
    "store_checks_at_home": True,
    "minimum_tithing_points": 3000,
    "fast_cash": True,
    "sell_board_stock": True,
    # !!!!!!!  CHANGE DISCORD WEBHOOK HERE  !!!!!!!
    "discord_webhook_url": "https://discord.com/api/webhooks/844530195041615882/oqpkPJFBfFPVbghMpbEVUw615VHcqOxEXABZZ1PdIjuFqesRttsSu5yDxmztaW-Um9Vm",
    # relative X Y to target tress
    "relative_x": 0,
    "relative_y": -1,
    # if char should lock skill at 64.9 to get only boards that sells
    "lock_skill_at_64_9": True,
    "skip_bad_runes": True,
    "skip_runes_where_char_was_attacked": True,
    "skip_runes_where_char_died": True,
    "drop_money_to_main_char": True,
    # drop money config
    "main_char_name": "gugutz",
    "drop_money_secret_msg": "vendor bbuy sell",
    # runebook names
    "home_runebook": "Home",
    "wood_runebooks": ["Wood1", "Wood2"],
    "banks_runebook": "Banks",
    "carpenters_runebook": "Carps",
    # rune positions in Home runebook
    "rune_positions": {"vendor": 1, "bank": 2, "home": 3, "shrine": 4},
    "place_to_escape_attacks": "home",  # home or bank
}
config["Tobias"] = {
    "sell_wood": True,
    "wood_runebooks": ["Wood1"],
    "store_checks_at_home": True,
}
