from functions import logger,search
from pprint import pprint

DESC="Shows a list of disabled modules"
USAGE="modules"

async def init(bot):
    chat=bot.message.channel
