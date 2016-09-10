import discord
import global_vars
import os
# For the event loop
import asyncio
# For iterating through the events
from os import listdir
from os.path import isfile, join
# For importing events
import importlib
# For logging
from functions import logger
# For logging
import datetime
# For repl
from classes import repl
# For signal handling
import signal
import sys

loop = asyncio.get_event_loop()
try:
    logger.printtf("[BOT] Booting up")

    client = discord.Client()
    global_vars.client = client
    global_vars.repl_sess = repl.REPL(client)

    logger.printtf("[BOT] Loading events")
    try:
        events = [ f for f in listdir("events/") if isfile(join("events/",f)) and not ".pyc" in f and not "__" in f]
        if len(events) == 0:
            logger.printtf("[EVENTS] No events found. This sure isn't normal!")
        events = iter(events)
        for event in events:
            event = event.replace(".py","")
            event_class = 'events.'+event
            try:
                if hasattr(event, 'NO_AUTOLOAD'):
                    continue;
                func = importlib.import_module(event_class)
            except Exception as e:
                print(str(e))
                logger.PrintException()
                continue
            print("[EVENTS] {} loaded.".format(event))
    except Exception as e:
        print(str(e))
        logger.PrintException()
except (KeyboardInterrupt, SystemExit):
    for server_id in global_vars.music_bots:
        global_vars.music_bots[server_id].disconnect()
    client.logout()
    sys.exit(0)
except Exception as e:
    print(str(e))
    logger.PrintException()

# Log in the client
client.run(global_vars.discord_token)