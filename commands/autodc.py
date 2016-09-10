from functions import logger,botfunc
import global_vars

DESC="Toggles if the music bot will automatically disconnect"
USAGE="autodc"



async def init(bot):
    chat=bot.message.channel
    user=str(bot.message.author.name)
    try:
        server_id = bot.message.server.id
        if server_id in global_vars.music_bots and await global_vars.music_bots.get(server_id).is_connected():
            if global_vars.music_bots[server_id].auto_dc:
                global_vars.music_bots[server_id].auto_dc = False
                await botfunc.autoDelete(10, bot.message, await bot.sendMessage(":notes: Automatic Disconnect turned **off**."))
            else:
                global_vars.music_bots[server_id].auto_dc = True
                await botfunc.autoDelete(10, bot.message, await bot.sendMessage(":musical_note: Automatic Disconnect turned **on**."))
    except:
        logger.PrintException(bot.message)
