import re
import logging
from random import choice
from time import sleep

from slackbot.bot import listen_to

logger = logging.getLogger(__name__)

_FRISKA_REPLIES = [
        "Flat white pls",
        "Flat white pls.",
        "I'd like a flat white",
        "I'd like a flat white.",
        "Cortado please",
        "Cortado please.",
        "Cortado please!",
        "I'll have a flat white please",
        "Flat white please!",
        "Cortado pls!",
        "Cortado pls",
        "House bacon please!",
        "Bacon pls",
        "BACON"
]


# Listen for shortish messages that mention Friska and end with a question mark.
@listen_to('(.){0,20}friska(.){0,15}\?$', re.IGNORECASE)
def get_some_free_friska(message):
    try:
        channel_name = message._client.channels[message.body['channel']]['name']
        if channel_name == 'bristol_chitchat':
            sleep(choice([1, 2, 3]))
            message.send(choice(_FRISKA_REPLIES))
    except Exception as e:
        # We never want to invoke the normal error response mechanisms, lest they
        # find out that this is actually a bot.
        logger.exception("Ooopsy, something went wrong")
