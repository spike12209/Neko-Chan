from functions import groups,logger,config
import pprint
import re
DESC="Set custom welcome bot.message!"
USAGE="set_welcome [msg {mention}, {name}, {server}]"

async def init(bot):
    chat=bot.message.channel
    user=str(bot.message.author.name)
    try:
        user = bot.message.author
        if len(bot.args) > 0:
            msg = " ".join(bot.args)
            if msg is not None:
                await config.setConf(bot.message.server.id, "join_message", msg)
                await bot.sendMessage( "Join message set!")
            else:
                await bot.sendMessage( "Something isn't ok!")
        else:
            await bot.sendMessage( "Not enough arguments!")
    except Exception:
        logger.PrintException(bot.message)
        return False
