from functions import logger, search
import discord
import asyncio
import os
import aiohttp
import global_vars
import datetime

DESC="Changes the Nickname of a user"
USAGE="nick [user] [Nickname/None]"

async def init(bot):
    try:
        if len(bot.args)>0:
            user = None
            if len(bot.message.raw_mentions)>0:
                user = await search.user(bot.message.channel, bot.message.raw_mentions[0])
            else:
                user = await search.user(bot.message.channel, bot.args[0])
            bot.args.pop(0)
            if user is not None:
                try:
                    oldname = user.display_name
                    name = " ".join(bot.args)
                    print(name)
                    if name.casefold() == "none":
                        name = None
                    # Bot needs permissions for this!
                    await bot.client.change_nickname(user, name)
                    await bot.sendMessage( ":white_check_mark: {} has been renamed to {}".format(oldname, name))
                except discord.Forbidden:
                    await bot.sendMessage(":x: Sorry but I can't change {}'s name.".format(oldname))
            else:
                await bot.sendMessage( ":x: Can't find the specified user.")
    except:
        logger.PrintException(bot.message)
