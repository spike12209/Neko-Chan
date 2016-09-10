from functions import groups,search,logger

DESC="Set a users accesslevel"
USAGE="setlevel level userid"

async def init(bot):
    chat=bot.message.channel
    response = ""
    try:
        try:
            level = int(bot.args[0])
            if level > 5:
                await bot.sendMessage( "The highest level is 5")
                return False
            if level < -1:
                await bot.sendMessage( "The lowest level is -1")
                return False
            bot.args.pop(0)

        except:
            await bot.sendMessage( "`{}` is not a valid number.".format(bot.args[0]))
            return False

        if len(bot.args)>0:
            if len(bot.message.raw_mentions)>0:
                user = await search.user(chat, bot.message.raw_mentions[0])
            else:
                user = await search.user(chat, " ".join(bot.args))
        else:
            await bot.sendMessage( "You have to specify a user.")
            return False

        if user is not None:
            if await groups.getLevel(bot.message.server.id, user) <= 5:
                if user.id == bot.message.author.id:
                    await bot.sendMessage( "You can't change your level.")
                    return False
                if level == 0:
                    await bot.sendMessage("**Do you want to __enforce__ access level 0?** (Yes/__No__)\r\nThis means that this users access level will be 0, independent of his roles.")
                    choice = await bot.client.wait_for_message(timeout=20.0, author=bot.message.author)
                    if choice is None or choice.content.casefold() == "no":
                        if await groups.unsetLevel(bot.message.server.id, user.id):
                            await bot.sendMessage("`{}` will now inherit it's roles access level.".format(user.display_name))
                            return True
                if await groups.setLevel(bot.message.server.id, user.id, level):
                    if level == 0:
                        await bot.sendMessage("`{}'s` access level has been **enforced** to `{}`".format(user.display_name, level))
                    else:
                        await bot.sendMessage("`{}'s` access level has been set to `{}`".format(user.display_name, level))
            else:
                await bot.sendMessage( "You can't change `{}'s` access level as (s)he's a bot administrator!".format(user.display_name))
        else:
            await bot.sendMessage( "Could not find any user like \"`{}`\"".format(" ".join(bot.args)))
            return False

    except Exception:
        logger.PrintException(bot.message)
        return False
