from functions import logger,search
import discord
import aiohttp
import re
from bs4 import BeautifulSoup as soup

DESC="xxx"
USAGE="xx"

async def status():
    url = "https://status.discordapp.com/"
    with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            r = await r.text()
            return r

async def init(bot):
    try:
        stat = soup(await status())
        if not bot.message.channel.is_private:
            api = []
            response = "```xl\n"
            response += "{}\n\n".format(stat.find("div", {"class":"page-status status-none"}).text.strip())
            for word in stat.find("div", {"class":"components-container one-column"}).text.replace("?", "").splitlines():
                if len(word.strip())>1:
                    api.append(word.strip())
            api2 = list(filter(lambda s: not s.startswith(('Operational','Degraded', 'Partial', 'Major')), api))
            api3 = list(filter(lambda s: s.startswith(('Operational','Degraded', 'Partial', 'Major')), api))
            response += "\r\n".join([ "'{}' - {}".format(entry, api2[n]) for n, entry in enumerate(api3) if n < 4] + ["\r\n- Voice Servers:\r\n"])
            response += "\r\n".join([ "'{}' - {}".format(entry, api2[n]) for n, entry in enumerate(api3) if n >= 4])
            response += "```"
            await bot.sendMessage(response)
        else:
            await bot.sendMessage("rip.")
    except:
        logger.PrintException(bot.message)
