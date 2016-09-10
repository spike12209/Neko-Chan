from functions import groups,search,logger,config
import pprint
DESC="Set channel for join/leave msgs"
USAGE="set_announce #channel/[on/off]"

async def init(bot):
    chat=bot.message.channel
    user=str(bot.message.author.name)
    try:
        user = bot.message.author
        #if len(bot.args[0]) == 0:
        #    await bot.sendMessage("Not enough arguments! Current channel: {}").format(config.getConf(message.server.id, "announcement_channel"))
        if len(bot.args) > 0:
            if bot.args[0] == "off":
                await config.setConf(bot.message.server.id, "joined_notification", 0)
                await config.setConf(bot.message.server.id, "left_notification", 0)
                await bot.sendMessage( "Announcements have been turned OFF!")
            elif bot.args[0] == "on":
                await config.setConf(bot.message.server.id, "joined_notification", 1)
                await config.setConf(bot.message.server.id, "left_notification", 1)
                await bot.sendMessage( "Announcements have been turned ON!")
            else:
                channel = " ".join(bot.args)
                channel = await search.channel(bot.message.server, channel)
                if channel is not None:
                    await config.setConf(bot.message.server.id, "announcement_channel", channel.name)
                    await bot.sendMessage( "Channel set!")
                else:
                    await bot.sendMessage( "Such channel doesn't exist!")
        else:
            await bot.sendMessage("Not enough arguments! Current channel: {}".format(await config.getConf(bot.message.server.id, "announcement_channel")))
    except Exception:
        logger.PrintException(bot.message)
        return False
