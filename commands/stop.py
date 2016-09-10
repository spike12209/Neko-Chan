from functions import logger, botfunc
import asyncio
import global_vars

DESC="Stops the music bot"
USAGE="stop"

async def init(bot):
    chat=bot.message.channel
    user=str(bot.message.author.name)
    try:
        server_id = bot.message.server.id
        if server_id in global_vars.music_bots:
            await global_vars.music_bots[server_id].disconnect()
            await botfunc.autoDelete(10, await bot.sendMessage( "Music bot stopped."), bot.message)
            return True
        await botfunc.autoDelete(10, await bot.sendMessage( "There's no active player."), bot.message)
    except:
        logger.PrintException(bot.message)
