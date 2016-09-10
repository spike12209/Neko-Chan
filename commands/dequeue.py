import json
from functions import logger,search,tools,botfunc,groups
from classes.music import Music
import asyncio
import global_vars
import re
import importlib
from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError

def parseInt(str):
    try:
        return int(str)
    except:
        return False
DESC="Removes a song from the queue"
USAGE="dequeue [id]"
async def init(bot):
    try:
        server_id = bot.message.server.id
        if server_id in global_vars.music_bots:
            if global_vars.music_bots[server_id].shutting_down == False:
                if global_vars.music_bots[server_id].sender.id != bot.message.author.id and not (bot.access_level >= await groups.needed_level(server_id, "dequeue_admin"):
                    return
                queue = await global_vars.music_bots[server_id].queuelist()
                size = len(queue)
                if len(bot.args)>0:
                    entry = bot.args[0]
                else:
                    choose = "**Which song would you like to remove from queue?**\r\n"
                    for id, music in enumerate(queue):
                        if id < 10:
                            choose+="`{}` - `{}` by `{}`\r\n".format((id+1), music.title, music.user)
                        else:
                            break
                    await botfunc.autoDelete(25,await bot.sendMessage(choose))

                    # Wait for an (valid) answer
                    check = lambda m: parseInt(m.content)<=size
                    choice = await bot.client.wait_for_message(timeout=20.0, check=check, author=bot.message.author)
                    if choice is None:
                        return
                    await botfunc.autoDelete(10,choice)
                    entry = choice.content
                entry = int(entry)
                if (entry-1) < size:
                    title = await global_vars.music_bots[server_id].getqueue((entry-1))
                    title = title.title
                    if await global_vars.music_bots[server_id].dequeue(entry):
                        await botfunc.autoDelete(10,await bot.sendMessage( ":white_check_mark: `{}` removed from queue.".format(title)),bot.message)
                else:
                    await botfunc.autoDelete(10,await bot.sendMessage( ":x: Invalid entry."),bot.message)
                    return False
            else:
                await botfunc.autoDelete(10,await bot.sendMessage( ":x: The current player is done and about to shut down."),bot.message)
                return False
    except:
        logger.PrintException(bot.message)
