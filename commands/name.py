from functions import logger, search
import discord
import asyncio
import os
import aiohttp
import global_vars
import datetime

DESC="Changes the bots name on this Server"
USAGE="name [new name]"

async def init(bot):
    try:
        if len(bot.args)>0:
            name = " ".join(bot.args)
            myself = bot.message.server.me
            if myself is not None:
                if name.casefold() == "none":
                    name = None
                # Bot needs permissions for this!
                await bot.client.change_nickname(myself, name)
                await bot.sendMessage( "New name set.")
        else:
            await bot.sendMessage( "Current name: {}\r\nYou can give a new name as second argument.".format(bot.client.user.name))
    except discord.Forbidden:
        await bot.sendMessage(":x: Sorry but I can't change my name.")
    except:
        logger.PrintException(bot.message)
