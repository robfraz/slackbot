import re
import logging
from random import choice
from time import sleep, time

from slackbot.bot import listen_to, default_reply

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

_FRISKA_CHANNEL = 'bristol_chitchat'

_IGNORE_LIST = set([
    'U0KNV5TS8',  # BS
    'U5P6TB21E',  # BE
    'U19TY8ZEZ',  # CGS
    'U6NS6858R',  # CS
    'U5YUTHUP2',  # CT
    'U6JJ4NQ57',  # DB
    'U04QQ9ZLC',  # EA
    'U388KDEET',  # HM
    'U04UPM7ET',  # JF
    'U7LF36R2T',  # LT
    'U0470B1LG',  # MZ
    'U3YCWA2Q3',  # RF Test account
    'U0KNYSN9L',  # SH
    'U04AW38AL',  # TO
    'U6HEJL3LK'   # WH
])


@default_reply
def do_nothing(message):
    pass


# Listen for shortish messages that mention Friska and end with a question mark.
@listen_to('^(.){0,20}friska(.){0,15}\?$', re.IGNORECASE)
def friska(message, *args):
    """Get some free Friska!"""
    try:
        channel_name = message._client.channels[message.body['channel']]['name']
        if channel_name == _FRISKA_CHANNEL:
            if message.body['user'] in _IGNORE_LIST:
                user_id = _get_user_id(message)
                logger.info(f"Ignoring feeble attempt by {user_id} to make me look a fool")
            else:
                logger.info("Someone is getting Friska'd!")
                # Only compete in 'friska-ings' every 12 hours, to avoid bot-like behaviour.
                if (time() - friska.time_of_last_friska) > 43200:
                    logger.info("Commencing Friska response...")
                    sleep(choice([1, 2, 3]))
                    message.send(choice(_FRISKA_REPLIES))
                    friska.time_of_last_friska = time()
                    logger.info("Friska was ordered successfully!")
                else:
                    logger.info("Last Friska-ing was too recent - ignoring this Friska opportunity :-(")
    except Exception as e:
        # We never want to invoke the normal error response mechanisms, lest they
        # find out that this is actually a bot.
        logger.exception("Ooopsy, something went wrong")


# A kludge to get a static variable within the friska function
friska.time_of_last_friska = 0


###################
#  PRIVATE STUFF  #
###################


def _get_user_id(message):
    return message._client.users[message.body['user']][u'name']
