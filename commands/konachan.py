from functions import konachan, logger
import json
import random
from random import randint

DESC = "Get a random konachan picture with specified tag"
USAGE = "konachan"


async def init(bot):
    try:
        chat=bot.message.channel
        tags = "+".join(bot.args)
        site = False
        img = False
        try:
            img = await konachan.select(tags)
            if img is not None:
                if tags.startswith("loli"):
                    await bot.sendMessage( img)
                else:
                    await bot.sendMessage( img)
            else:
                await bot.sendMessage( 'Couldn\'t find any pictures.')
        except:
            await bot.sendMessage( 'Something went wrong!')
    except:
        logger.PrintException(bot.message)
        return
