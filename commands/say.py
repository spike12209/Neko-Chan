from functions import logger, config, search
import asyncio
import global_vars

DESC="Just... you know.. for fun?!"
USAGE="say [channel] [message]"

async def init(bot):
    chat=bot.message.channel
    user=str(bot.message.author.name)
    try:
        try:
            channel = await search.channel(bot.message.server, str(bot.args[0]))
        except:
            return False
        user = await search.user(chat, bot.message.author.id)
        print(bot.args[0])
        def is_me(m):
            check = (m.author == user)
            if check:
                return "1"
        msg = " ".join(bot.args[1:])
        await bot.client.purge_from(chat, limit=1, check=is_me)
        await bot.sendMessage(msg, channel)
    except Exception:
        logger.PrintException(bot.message)
