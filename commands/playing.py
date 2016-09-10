from functions import logger, config, botfunc
import asyncio
import global_vars

DESC="Information about current song!"
USAGE="playing"

async def init(bot):
    chat=bot.message.channel
    user=str(bot.message.author.name)
    try:
        server_id = bot.message.server.id
        if server_id in global_vars.music_bots:
            await global_vars.music_bots[server_id].playing_now()
            await botfunc.autoDelete(10,bot.message)
            return True
        else:
            await bot.sendMessage( "There's no active player.")
    except Exception:
        logger.PrintException(bot.message)
