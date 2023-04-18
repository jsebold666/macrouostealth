import modules.common_utils as utils

BODTYPES = [0x2258]

def rename_item(id_runebook):
    print('Vai mudar o nome')

    SetContextMenuHook(id_runebook,0)
    RequestContextMenu(id_runebook)
    Wait(1500)
    ConsoleEntryUnicodeReply(("BS"+"\r"))
    Wait(1500)

while True:
    rename_item(0x4374132a)