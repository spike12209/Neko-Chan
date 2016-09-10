from functions import logger, tools
import asyncio
import os
from xml.etree import ElementTree
import re
import aiohttp
import html

DESC="Shows informations about an anime"
USAGE="anime [name]"

async def init(bot):
    try:
        data = await tools.mal_anime("+".join(bot.args))
        print(data)
        if data is None or len(data)==0:
            bot.sendMessage("Sorry, no Anime named \"{}\" found :sob:".format(" ".join(bot.args)))
            return
        root = ElementTree.fromstring(data)
        if len(root)==0:
            bot.sendMessage("Sorry, no Anime named \"{}\" found :sob:".format(" ".join(bot.args)))
            return
        elif len(root) == 1:
            # Only one entry found. Using it.
            entry = root[0]
        else:
            # Found multiple anime. Informing user
            choose = "**Multiple anime found**\r\nChoose one of the following anime by sending its number:\r\n"
            choose += "\r\n".join([ '`{}` - `{}`'.format(n+1, entry[1].text) for n, entry in enumerate(root) if n < 10 ])
            await bot.sendMessage(choose)

            # Wait for an (valid) answer
            check = lambda m: m.content in map(str, range(1, len(root)+1))
            choice = await bot.client.wait_for_message(timeout=20.0, check=check, author=bot.message.author)
            if choice is None:
                return
            entry = root[int(choice.content)-1]
        #=========================================
        # Enough talking. Let's give them facts
        #=========================================
        switcher = [
            'type',
            'episodes',
            'score',
            'status',
            'start_date',
            'end_date'
        ]
        
        # Title first
        msg = '**{}**\r\n\r\n'.format(entry.find('title').text)
        
        # Alternative names
        spec = entry.find("synonyms")
        if spec is not None and spec.text is not None:
            msg += '**Synonyms:**\r\n'
            spec = html.unescape(spec.text.replace('<br />', ''))
            spec = spec.split("; ")
            for synonym in spec:
                msg += " - {}\r\n".format(synonym)
        
        # The URL to the anime
        msg += '**Link: ** http://myanimelist.net/anime/{}\r\n'.format(entry.find('id').text)
        
        # Fetch all data defined above
        for k in switcher:
            spec = entry.find(k)
            if spec is not None and spec.text is not None:
                msg += '**{}** {}\r\n'.format(k.capitalize()+':', html.unescape(spec.text.replace('<br />', '')))
                
        # Tell them about the story
        spec = entry.find("synopsis")
        if spec is not None and spec.text is not None:
            msg += '**Story:**\r\n```{}```'.format(html.unescape(spec.text.replace('<br />', '')))
        
        # Send it
        await bot.sendMessage(msg)
    except:
        logger.PrintException(bot.message)