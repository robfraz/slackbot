import re
from random import choice
from time import sleep

from slackbot.bot import listen_to

_FRISKA_REPLIES = [
        "Flat white pls",
        "I'd like a flat white",
        "Cup of tea please",
        "Tea please!",
        "I'll have a flat white please",
        "Flat white please!",
        "Tea pls!",
        "Tea pls",
        "House bacon please!",
        "BACON"
]


@listen_to('friska.*\?$', re.IGNORECASE)
# @respond_to('friska ', re.IGNORECASE)
def get_some_free_friska(message):
    channel_name = message._client.channels[message.body['channel']]['name']
    if channel_name == 'general':
        sleep(choice([1, 2, 3]))
        message.send(choice(_FRISKA_REPLIES))
