import sys
import os
from functions import logger

DESC="Restarts the bot"
USAGE="restart"

async def init(bot):
    try:
        await bot.sendMessage( "Brb. Killing myself.")
        await bot.client.logout()
    except Exception:
        logger.PrintException(bot.message)
    finally:
        sys.exit(1337)
