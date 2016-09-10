from functions import groups,logger,config,disabledcmd
import pprint
import importlib
import re
DESC="Disable cmd for this server"
USAGE="disablecmds"

async def init(bot):
    chat=bot.message.channel
    user=str(bot.message.author.name)
    try:
        user = bot.message.author
        commands = await disabledcmd.getall(bot.message.server.id)
        if commands is not None:
            response = "`--- Disabled Commands ---`\r\n"
            for command in commands:
                response += "{}\r\n".format(command['cmd'])
            await bot.sendMessage( response)
        else:
            await bot.sendMessage( "All commands are enabled!")
    except Exception:
        logger.PrintException(bot.message)
        return False
