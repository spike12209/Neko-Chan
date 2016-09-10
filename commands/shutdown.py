import sys
import os
from functions import logger

DESC="Shuts down the bot"
USAGE="shutdown"

async def init(bot):
    try:
        await bot.sendMessage( "Shutting down. Good night. :wave:")
        await bot.client.logout()
    except Exception:
        logger.PrintException(bot.message)
        return False
    finally:
        sys.exit(0)
