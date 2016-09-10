from functions import groups,logger,config,disabledcmd
import pprint
import importlib
import re
DESC="Enable disabled for this server"
USAGE="enablecmd [cmd]"

async def init(bot):
    chat=bot.message.channel
    user=str(bot.message.author.name)
    try:
        user = bot.message.author
        if len(bot.args) > 0:
            msg = " ".join(bot.args)
            try:
                importlib.import_module('commands.' + msg)
                if msg == "disablecmd" or msg == "enablecmd":
                    await bot.sendMessage( "You can't do that!")
                else:
                    await disabledcmd.delete(bot.message.server.id, msg)
                    await bot.sendMessage( "Command has been enabled!")
            except ImportError:
                await bot.sendMessage( "Command doesn't exist!")
        else:
            await bot.sendMessage( "Not enough arguments!")
    except Exception:
        logger.PrintException(bot.message)
        return False
