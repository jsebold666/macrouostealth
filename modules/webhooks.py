from discord_webhook import DiscordWebhook

# ======================================================================
# Discord Utils
# ======================================================================


def send_discord_message(webhook_url, message):
    webhook = DiscordWebhook(url=webhook_url, content=str(message))
    webhook.execute()

    return


def send_discord_message_multi_lines(
    webhook_url,
    arrayOfMessages,
    username="Freddy Krueger",
    messageColor="16411130",
    avatarURL="https://vignette.wikia.nocookie.net/dcheroesrpg/images/b/b2/Freddy_Krueger.jpg",
):
    jsonPayload = {}
    jsonPayload["username"] = username
    jsonPayload["avatar_url"] = avatarURL

    jsonPayload["embeds"] = []
    for message in arrayOfMessages:
        embeds = {}
        embeds["description"] = message
        embeds["color"] = messageColor
        jsonPayload["embeds"].append(embeds)

    payload = json.dumps(jsonPayload)

    headers = {
        "Content-Type": "application/json",
    }
    response = requests.request("POST", webhook_url, headers=headers, data=payload)
    print(response.text.encode("utf8"))


# ======================================================================
# Telegram Utils
# ======================================================================
def send_afk_gump_warning(webhook_url, message):
    telegram_bot_url = "https://api.telegram.org/bot%s/warn_afk_gump" % (
        telegram_bot_token
    )
    response = requests.request("POST", webhook_url, headers=headers, data=payload)

    print(response.text.encode("utf8"))
    return response
