from functions import logger, config
import asyncio
import global_vars

DESC="Sets volume of currect song"
USAGE="volume [0-100]"



async def init(bot):
    chat=bot.message.channel
    user=str(bot.message.author.name)
    try:
        server_id = bot.message.server.id
        if server_id in global_vars.music_bots:
            if not global_vars.music_bots[server_id].paused:
                await global_vars.music_bots[server_id].pause()
                await bot.sendMessage( "Music is now paused")
            else:
                await global_vars.music_bots[server_id].resume()
                await bot.sendMessage( "Music is now resumed")
            return True
        else:
            await bot.sendMessage( "There's no active player.")
    except Exception:
        logger.PrintException(bot.message)
