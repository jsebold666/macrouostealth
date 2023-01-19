# =================================================================================
# Journal Utils
# =================================================================================


def in_journal(msg):
    if InJournal(msg) > 0:
        return True
    return False


def is_char_being_attacked():
    under_attack_journal_msg = "is attacking you"

    if InJournal(under_attack_journal_msg) > -1:
        ClearJournal()
        return True
    else:
        return False
