import json
from functions import logger,search,tools,botfunc
from classes.music import Music
import asyncio
import global_vars
import math
import re
import importlib
from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError


DESC="Will add a youtube url to the music players queue"
USAGE="queue youtube-link"

@asyncio.coroutine
def ytsearch(string):
    try:
        with YoutubeDL({'default_search': 'auto', 'format': 'webm[abr>0]/bestaudio/best', 'simulate': True, 'quiet': True, 'noplaylist': True}) as ydl:
            info = ydl.extract_info(string, download=False)
            if "entries" in info:
                info = info['entries'][0]
            return info.get('webpage_url', None)
    except DownloadError:
        #return "Could not play that. This video is banned in my country."
        return None
    except:
        logger.PrintException()
        return url

@asyncio.coroutine
def get_title(url):
    try:
        with YoutubeDL({'quiet': True, 'simulate': True, 'noplaylist': True}) as ydl:
            infos = ydl.extract_info(url, download=False)
            return infos.get('title', None)
    except DownloadError:
        return None
    except:
        logger.PrintException()
        return url

async def init(bot):
    chat=bot.message.channel
    user=str(bot.message.author.name)
    try:
        server_id = bot.message.server.id
        if server_id in global_vars.music_bots and await global_vars.music_bots.get(server_id).is_connected():
            if global_vars.music_bots[server_id].shutting_down == False:
                if bot.message.attachments is not None and len(bot.message.attachments)==1:
                    if bot.message.attachments[0] is not None:
                        bot.args = []
                        bot.args.append(bot.message.attachments[0]['url'])
                        if not bot.args[0].endswith(".mp3") and not not bot.args[0].endswith(".wav"):
                            await botfunc.autoDelete(10,await bot.sendMessage( "The attachment has to be an MP3 file!"),bot.message)
                            return False
                done = False
                if len(bot.args) == 0 or (len(bot.args[0])==1 and (isinstance(bot.args[0],int) or bot.args[0].isdigit())):
                    page = 1
                    queue = await global_vars.music_bots[server_id].queuelist()
                    pages = math.ceil(len(queue)/10)
                    if len(bot.args) == 1:
                        page = int(bot.args[0])
                        if page > pages:
                            page = pages
                    response = ""
                    start = ((page-1)*10)
                    end = start+9
                    if pages > 1:
                        response = "--> **Page {}** / {}\r\n".format(page,pages)
                    for id, entry in enumerate(queue):
                        if id >= start and id <= end:
                            val = re.search('<@!?(.*)>', entry.user)
                            if val:
                                user = await search.user(chat, val.group(1))
                                user = user.display_name
                            else:
                                user = entry.user
                            response+="{}. `{}` by `{}`\r\n".format(id+1, entry.title, user)
                    if len(response)==0:
                        response = "The queue is empty"
                    #await botfunc.autoDelete(20,await bot.sendMessage(response),bot.message)
                    await botfunc.autoDelete(20,await bot.sendMessage(response),bot.message)
                    return

                if "http://" in bot.args or "https://" in bot.args:
                    url = "%20".join(bot.args)
                else:
                    url = " ".join(bot.args)
                if not "http://" in url and not "https://" in url:
                    url = await ytsearch(" ".join(bot.args))
                if url is None :
                    await botfunc.autoDelete(10,await bot.sendMessage("Nothing found for `{}`.".format(" ".join(bot.args))),bot.message)
                    return False
                title = await get_title(url)
                if title is None:
                    await botfunc.autoDelete(10,await bot.sendMessage("Could not play {}. This video is banned in my country.".format(url)),bot.message)
                    return False
                done = await global_vars.music_bots[server_id].add(Music(bot.message.author, "ytdl", url, title))

                if done != False:
                    if await global_vars.music_bots[server_id].is_playing():
                        await botfunc.autoDelete(10,await bot.sendMessage( "`{}`\r\nAdded to queue. You are queued in place {} .".format(title, done)),bot.message)
                    else:
                        await botfunc.autoDelete(10,bot.message)
                        await global_vars.music_bots[server_id].playNext()
                    return True
                else:
                    await botfunc.autoDelete(10,await bot.sendMessage( "The queue is full. Please try again later."),bot.message)
                    return False
            else:
                await botfunc.autoDelete(10,await bot.sendMessage( "The current player is done and about to shut down. Please start a new one once it's disconnected."),bot.message)
                #del global_vars.music_bots[server_id]
                return False
        try:
            func = importlib.import_module('commands.play')
            importlib.reload(func)
            await func.init(bot)
        except Exception as e:
            if "No module named" in str(e):
                return False
            logger.PrintException(bot)
            return
    except:
        logger.PrintException(bot.message)
