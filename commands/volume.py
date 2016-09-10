from functions import logger, config, botfunc
import asyncio
import global_vars

DESC="Sets volume of currect song"
USAGE="volume [0-100]"



async def init(bot):
    chat=bot.message.channel
    user=str(bot.message.author.name)
    try:
        server_id = bot.message.server.id
        if server_id in global_vars.music_bots and await global_vars.music_bots.get(server_id).is_connected():
            if len(bot.args) > 0:
                if bot.args[0].isdigit() == False:
                    await botfunc.autoDelete(10,await bot.sendMessage( "Please use a number between 0 and 110!"), bot.message)
                    return False
                if int(bot.args[0]) > 110:
                    await botfunc.autoDelete(10,await bot.sendMessage( "It can be set max to 110%!"), bot.message)
                else:
                    await botfunc.autoDelete(10,bot.message)
                    await global_vars.music_bots[server_id].volume(int(bot.args[0]))
                    return True
            else:
                volume = await config.getConf(bot.message.server.id, "music_bot_volume")
                await botfunc.autoDelete(10,await bot.sendMessage( "Volume is set to {}%!".format(volume * 100)), bot.message)
        else:
            await bot.sendMessage( "There's no active player.")
    except Exception:
        logger.PrintException(bot.message)
