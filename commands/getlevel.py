from functions import groups,search,logger
import pprint
DESC="See your bots access level"
USAGE="getlevel [member*optional]"

async def init(bot):
    chat=bot.message.channel
    user=str(bot.message.author.name)
    try:
        user = bot.message.author
        if len(bot.args)>0:
            if len(bot.message.raw_mentions)>0:
                user = await search.user(chat, bot.message.raw_mentions[0])
            else:
                user = await search.user(chat, " ".join(bot.args))
            if user is not None:
                if user == bot.message.author:
                    await bot.sendMessage( "Your access level is `{}`".format(bot.access_level))
                else:
                    access_level = await groups.getLevel(bot.message.server.id, user)
                    await bot.sendMessage("`{}'s` access level is `{}`".format(user.display_name, access_level))
            else:
                await bot.sendMessage( "Could not find any user like \"`{}`\"".format(" ".join(bot.args)))
        else:
            level = await groups.getLevel(bot.message.server.id, user)
            if user == bot.message.author:
                await bot.sendMessage( "Your access level is `{}`".format(bot.access_level))
    except Exception:
        logger.PrintException(bot.message)
        return False
