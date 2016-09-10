from functions import logger, config, botfunc
import asyncio
import discord
from classes.musicplayer import MusicPlayer
from classes.music import Music
from pprint import pprint
import os.path
import global_vars
import importlib

DESC="Will play a link in your current voice channel"
USAGE="play url"



async def init(bot):
    chat=bot.message.channel
    user=str(bot.message.author.name)
    try:
        #await logger.print_to_file(str(type(bot.message.author)))
        if bot.message.channel.is_private:
            await botfunc.autoDelete(10, await bot.sendMessage( "This is a private chat."),bot.message)
            return False
        if await config.getConf(bot.message.server.id, "music_bot") == False:
            await botfunc.autoDelete(10, await bot.sendMessage( "Music bots are disabled on this server."),bot.message)
            return False
        if bot.message.author.voice_channel is None:
            await botfunc.autoDelete(10, await bot.sendMessage( "You have to be in a voice channel."),bot.message)
            return False
        if bot.message.attachments is not None and len(bot.message.attachments)==1:
            if bot.message.attachments[0] is not None:
                bot.args = []
                bot.args.append(bot.message.attachments[0]['url'])
                if not bot.args[0].endswith(".mp3") and not bot.args[0].endswith(".wav"):
                    await botfunc.autoDelete(10, await bot.sendMessage( "The attachment has to be an MP3 file!"),bot.message)
                    return False
        if len(bot.args)==0:
            await botfunc.autoDelete(10, await bot.sendMessage( "You have to enter a link or attach a file."),bot.message)
            return False
        server_id = bot.message.server.id
        if not server_id in global_vars.music_bots or not await global_vars.music_bots[server_id].is_playing():
            await botfunc.autoDelete(10,bot.message) # Auto-Delete
            if not server_id in global_vars.music_bots or not await global_vars.music_bots.get(server_id).is_connected():
                global_vars.music_bots[server_id] = MusicPlayer(bot)
                try:
                    await global_vars.music_bots[server_id].connect()
                except:
                    await global_vars.music_bots[server_id].disconnect()
                    return False
                    logger.PrintException(bot.message)

            if "http://" in bot.args or "https://" in bot.args:
                url = "%20".join(bot.args)
            else:
                url = " ".join(bot.args)
            await global_vars.music_bots[server_id].play(Music(bot.message.author, "ytdl", url))
        else:
            try:
                func = importlib.import_module('commands.queue')
                importlib.reload(func)
                await func.init(bot)
            except Exception as e:
                if "No module named" in str(e):
                    return False
                logger.PrintException(bot.message)
                return
    except:
        logger.PrintException(bot.message)
