from functions import groups,search,logger,config
import pprint
DESC="Set channel for log bot.messages"
USAGE="set_log #channel"

async def init(bot):
    chat=bot.message.channel
    user=str(bot.message.author.name)
    try:
        user = bot.message.author
        if bot.args[0] == "off":
            await config.setConf(bot.message.server.id, "log_channel", None)
            await bot.sendMessage( "Logs has been turned OFF!")
        elif len(bot.args) > 0:
            channel = " ".join(bot.args)
            channel = await search.channel(bot.message.server, channel)
            if channel is not None:
                await config.setConf(bot.message.server.id, "log_channel", channel.name)
                await bot.sendMessage( "Channel set!")
            else:
                await bot.sendMessage( "Such channel doesn't exist!")

        else:
            await bot.sendMessage("Not enough arguments! Current channel: {}").format(config.getConf(message.server.id, "log_channel"))
    except Exception:
        logger.PrintException(bot.message)
        return False
