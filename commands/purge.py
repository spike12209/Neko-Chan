from functions import search, logger

DESC = "Delete x messages"
USAGE="purge [*amount*] [*user* `optional`]"



async def init(bot):
    chat=bot.message.channel
    try:
        if len(bot.args) == 0:
            await bot.sendMessage( "Didn't receive any arguments! Usage: {}".format(USAGE))
            return False
        try:
            bot.args[0] = int(bot.args[0])
        except:
            await bot.sendMessage( "`{}` is not a valid number.".format(bot.args[0]))
            return False
        if len(bot.args) > 1:
            if len(bot.message.raw_mentions)>0:
                user = await search.user(chat, bot.message.raw_mentions[0])
            else:
                user = list(bot.args)
                user.pop(0)
                user = await search.user(chat, " ".join(user))
            if user is not None:
                def is_me(m):
                    check = (m.author == user)
                    if check:
                        bot.args[0] = bot.args[0]-1
                        return (bot.args[0]>=0)
                await bot.client.purge_from(chat, limit=500, check=is_me)
                #await bot.sendMessage( user.display_name))
            else:
                await bot.sendMessage( "Could not find any user with \"`{}`\"".format(user))
                return False

        else:
            await bot.client.purge_from(chat, limit=bot.args[0]+1, check=None)
            return False

    except Exception:
        logger.PrintException(bot.message)
        return False
