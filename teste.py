from py_stealth import *

def Discord(message):
    webhook = 'https://discord.com/api/webhooks/998684122623000697/yIF5-Z-4lDANyHs4_TBDJmbeMKdOCoH2xP0YcmUeV6ZU1mUNLsQr7RzTKjJQiMhiMF7_'
    dict = {"content": message}
    response = HttpClient().PostAsync( webhook, FormUrlEncodedContent(Dictionary[str,str](dict)))
    return response.Result.IsSuccessStatusCode
    
def toDiscord(found):
    item = Engine.Items.GetItem(found)
    props= []
    for x in item.Properties:
        props.append(x.Text)
    Discord('[{}] \n{}\n{}\n{}\n{}'.format(props[0], props[3], props[4], props[5]))
    Discord("".join(["{} \n"]*len(props)))

FindType(0x1086, Backpack())
founds = GetFindedList()
toDiscord(founds)