from functions import groups,logger,config
import pprint
import re
DESC="Set custom quit bot.message"
USAGE="set_quit [msg {mention}, {name}, {server}]"

async def init(bot):
    chat=bot.message.channel
    user=str(bot.message.author.name)
    try:
        user = bot.message.author
        if len(bot.args) > 0:
            msg = " ".join(bot.args)
            if msg is not None:
                await config.setConf(bot.message.server.id, "quit_message", msg)
                await bot.sendMessage( "Quit message set!")
            else:
                await bot.sendMessage( "Something isn't ok!")
        else:
            await bot.sendMessage( "Not enough arguments!")
    except Exception:
        logger.PrintException(bot.message)
        return False
