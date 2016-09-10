from functions import groups,search,logger,config
import re
import discord
import pprint

DESC="Ban many members at once with id's"
USAGE="massban [list of id's (separated with space or new line)]"

async def init(bot):
    chat=bot.message.channel
    try:
        if len(bot.args)>0:
            uid = ' '.join(bot.args)
            banned = []
            notfound = 0
            forbidden = []
            user = None
            for line in uid.split():
                if re.match("\d+",line):
                    user = discord.Object(id=line)
                    user.server = bot.message.server
                else:
                    await bot.sendMessage( ":x: {} is not a valid User or ID".format(line))
                try:
                    if user is not None:
                        await bot.client.ban(user, delete_message_days=1)
                        if not hasattr(user, 'display_name'):
                            banned.append("<@{}>".format(user.id))
                except discord.Forbidden:
                    #await bot.sendMessage( ':x: The bot does not have permissions to ban members or this user got highter rank than the bot.')
                    forbidden.append("<@{}>".format(user.id))
                except discord.NotFound:
                    notfound =+ 1
                except:
                    logger.PrintException(bot.message)
            if banned:
                if forbidden:
                    await bot.sendMessage( ":x: I couldn't ban: {}.".format(" ".join(forbidden)))
                if notfound:
                    await bot.sendMessage( ":rainbow: Banned users: {}\r\n Not found: {} user(s).\r\nForbidden: {}".format(" ".join(banned), notfound, forbidden))
                else:
                    await bot.sendMessage( ":rainbow: Banned users: {}.".format(" ".join(banned)))
        else:
            await bot.sendMessage( "I can't ban nothing.")
    except Exception:
        logger.PrintException(bot.message)
        return False
