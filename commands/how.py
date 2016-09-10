import global_vars
import discord
import importlib
from functions import logger, groups, config, aliases, disabledcmd
from pprint import pprint
import datetime
import asyncio

DESC="Shows how to use selected command"
USAGE="how [`command`]"

async def init(bot):
    if not bot.message.channel.is_private:
        prefix = await config.getConf(bot.message.server.id, "prefix")
    else:
        prefix = "!"
    try:
        if len(bot.args) > 0:
            command = " ".join(bot.args)
            wl = False
            if not bot.channel.is_private:
                needed_level = await groups.needed_level(bot.message.server.id, command)
                if needed_level > 0:
                    if bot.access_level < needed_level:
                        await bot.sendMessage( "You can't use this command!")
                        return
            else:
                await bot.sendMessage( "You can't use this command!")
                return
            cmd_class = 'commands.'+command
            try:
                func = importlib.import_module(cmd_class)
            except ImportError:
                return False
            if func.USAGE is not None:
                msg = "**Access Level:** `{}`\n**Usage:** `{}{}`\n**Description:** `{}`".format(needed_level, prefix, func.USAGE, func.DESC)
                await bot.sendMessage(msg)
        else:
            await bot.sendMessage( "`Usage:` {}how [command]".format(prefix))
    except:
        logger.PrintException(bot.message)
        return None
