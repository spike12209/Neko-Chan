import discord
import asyncio
from pprint import pprint
from functions import logger, groups, startup
import time
import global_vars
import psutil

client = global_vars.client
@client.event
async def on_ready():
    try:
        await logger.print_to_file('[BOT] Logged in')
        await startup.createDatabases()
        await logger.print_to_file('[BOT] Setting default access levels')
        await startup.defaultLevels()
        await logger.print_to_file('[BOT] Setting bot administrators')
        await startup.setAdmins()
        await logger.print_to_file('[BOT] Setting default config values')
        await startup.defaultConfig()
        await logger.print_to_file('[BOT] Ready to rumble')
        global_vars.started = time.time()
        psutil.cpu_percent()
        await client.change_status(game=discord.Game(name=global_vars.game))
    except:
        logger.PrintException()