import random
from functions import logger

DESC="Useless shit"
USAGE="idk"

async def init(bot):
    chat=bot.message.channel
    user=str(bot.message.author.name)
    try:
        idk = random.choice(list(open('idk.txt')))
        await bot.sendMessage( '{}'.format(idk))
    except Exception:
        logger.PrintException(bot.message)
