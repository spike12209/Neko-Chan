from functions import logger, config, tools, botfunc
from classes.music import Music
from classes.queue import Queue
import re
import os
import discord
import aiohttp
import asyncio
import math
from time import time
from pprint import pprint
import global_vars
from youtube_dl.utils import (
    DownloadError,
)


class ClientException(Exception):
    def __init__(self, mismatch):
        Exception.__init__(self, mismatch)

class ArgumentException(Exception):
    def __init__(self, mismatch):
        Exception.__init__(self, mismatch)

class PlayerException(Exception):
    def __init__(self, mismatch):
        Exception.__init__(self, mismatch)

class MusicPlayer:
    def __init__(self, bot):
        ''' Initialize the MusicPlayer object '''
        self.id = bot.message.server.id
        self.__loop = asyncio.get_event_loop()
        self.chat = bot.message.channel
        self.sender = bot.message.author
        self.channel = bot.message.author.voice_channel
        self.bot = bot
        self.VC = None
        self.Player = None
        self.__queue = Queue()
        self.shutting_down = False
        self.allowed = ["file","ytdl"]
        self.skipvotes = []
        self.paused = False
        self.oldmsg = None
        self.auto_dc = True

    async def disconnect(self):
        ''' Stops the current music player and disconnects the client '''
        try:
            self.shutting_down = True
            self.__queue = None
            await self.stop()
            if self.VC is not None and self.VC.is_connected():
                await self.VC.disconnect()
            self.VC = None
            del global_vars.music_bots[self.id]
        except:
            logger.PrintException()

    async def connect(self):
        ''' Connects the Client to a Voice channel '''
        if not discord.opus.is_loaded():
            raise PlayerException("Opus is not loaded.")
            # discord.opus.load_opus("libopus-0_x86.dll")
            #if not discord.opus.is_loaded():
                #PlayerException("Could not load Opus dll")
                #return False
        if not self.VC:
            try:
                #logger.printtf("connecting")
                self.VC = await self.bot.client.join_voice_channel(self.channel)
                print("Connected to {}".format(self.channel.name))
                #logger.printtf("connected")
                return True
            except Exception:
                logger.PrintException()
                return False
        else:
            raise ClientException("The MusicPlayer is already connected")

    async def stop(self):
        ''' Stops the current music player '''
        if self.Player is not None:
            if not self.Player.is_done():
                self.Player.stop()
                return True
            self.Player = None
        return False

    async def volume(self, value):
        """Sets the volume of the currently playing song."""

        if self.Player is not None:
            player = self.Player
            player.volume = value / 100
            await config.setConf(self.id, "music_bot_volume", player.volume)
            await self.bot.sendMessage('Set the volume to {:.0%}'.format(player.volume))

    async def pause(self):
        ''' Pauses the player '''
        if self.shutting_down:
            raise PlayerException("The player already finished.")
        if self.paused:
            raise PlayerException("The player is already paused.")
        self.Player.pause()
        self.paused = True

    async def resume(self):
        ''' Resumes the player '''
        if self.shutting_down:
            raise PlayerException("The player already finished.")
        if not self.paused:
            raise PlayerException("The player is already playing.")
        self.Player.resume()
        self.paused = False

    async def getqueue(self, position):
        return self.__queue.list[position]

    async def dequeue(self, position):
        return await self.__queue.remove(position)

    async def queuelist(self):
        return await self.__queue.getQueue()

    async def remaining(self):
        ''' Remaining songs in queue '''
        if self.shutting_down:
            raise PlayerException("The player already finished")
        return self.__queue.size()

    async def empty(self):
        ''' Clear the queue '''
        if self.shutting_down:
            raise PlayerException("The player already finished.")
        self.__queue = Queue()

    async def downloadSoundCloud(self, url):
        ''' Tries to get the download URL for soundcloud songs.
        Returns None if it fails '''
        try:
            posturl = "http://soundflush.com/"
            with aiohttp.ClientSession() as session:
                async with session.post(posturl, data={"track_url_field": url}) as r:
                    r = re.search('download=\".*\" href=\"(.*)\" class', await r.text())
                    if r is not None:
                        return r.group(1)
        except:
            logger.PrintException()
        return None
    async def voteSkip(self, user):
        ''' Handles the skipping votes and skips the current songs
        when there were enough votes
        Returns: True/False depending onif the vote was successfull or not'''
        if not user.voice_channel or user.voice_channel.id != self.channel.id:
            await self.bot.sendMessage("You have to be in the bots voice channel to vote for a skip.")
            return False
        members = len(self.channel.voice_members)-1
        success = False
        if members == 1:
            await self.bot.sendMessage("Skip vote was successful. Skipping song.")
            await self.playNext()
        if members > 0:
            needed = 1
            if members % 2 == 0:
                needed = int((members/2)+1)
            else:
                needed = int(math.ceil(members/2))
        else:
            if self.auto_dc:
                await self.disconnect()
            return success
        # If the user has not voted yet, count the vote and return True
        if not user.id in self.skipvotes:
            self.skipvotes.append(user.id)
            if len(self.skipvotes)<needed:
                await botfunc.autoDelete(10,await self.bot.sendMessage("{} voted to skip the current song. ({}/{} votes)".format(user.display_name, len(self.skipvotes), needed)))
            success = True
        # We've got enough votes. Skipping.
        if len(self.skipvotes)>=needed:
            await botfunc.autoDelete(10,await self.bot.sendMessage("{} voted to skip the current song.\r\nThe vote was successful. Skipping song.".format(user.display_name)))
            await self.playNext()
            return True
        elif success == False:
            await botfunc.autoDelete(10,await self.bot.sendMessage("You can't vote twice. ({}/{} votes)".format(len(self.skipvotes), needed)))
        return success

    async def playNext(self):
        ''' Play the next song'''

        # Delete the old message
        if self.oldmsg is not None:
            await botfunc.autoDelete(1,self.oldmsg)

        mb_allowed = await config.getConf(self.id, "music_bot")
        if mb_allowed == False:
            self.shutting_down = True
            await self.bot.sendMessage("The music bot has been stopped as it has been disabled by an administrator.")
            await self.disconnect()
        if mb_allowed == True:
            if not await self.stop():
                if self.__queue is not None:
                    if not self.__queue.empty():
                        MusicObj = await self.__queue.next()
                        return await self.play(MusicObj)
                    else:
                        if self.auto_dc:
                            await self.disconnect()
                            self.shutting_down = True
        return False
    async def play(self, obj):
        ''' initial play function '''
        try:
            if not self.VC or not self.VC.is_connected:
                raise ClientException("Not connected to a channel")
            if self.Player is not None:
                raise PlayerException("Could not play. There's another player running.")
            self.skipvotes = []
            obj.type = obj.type.lower()
            if not obj.type in self.allowed:
                raise ArgumentException("Invalid link type.")
            #if obj.type == "ytdl":
            await self.__yt_play(obj)
            #elif obj.type == "file":
            #    await self.__file_play(obj)
            return True
        except:
            logger.PrintException()
    async def add(self, obj):
        ''' Add a song to queue '''
        obj.type = obj.type.lower()
        if obj.type not in self.allowed:
            raise ArgumentException("Invalid link type.")
        if self.shutting_down:
            raise PlayerException("The player already finished.")
        if not self.__queue.full():
            return await self.__queue.add(obj)
        else:
            return False

    async def is_connected(self):
        ''' Is the bot connected? '''
        return (self.VC is not None and self.VC.is_connected())
    async def is_playing(self):
        ''' Is the bot playing? '''
        return ( self.Player is not None and not self.Player.is_done())

    async def playing_now(self):
        try:
            if not self.VC or not self.VC.is_connected:
                raise ClientException("Not connected to a channel")
            self.Player.volume = await config.getConf(self.id, "music_bot_volume")
            title = self.Player.title
            try:
                if self.Player.duration is not None:
                    secs = self.Player.duration
                    mins = math.floor(secs/60)
                    secs-=(mins*60)
                    mins = str(mins).zfill(2)
                    secs = str(secs).zfill(2)
                    # Change this shit so it does only generate the message. ?playing should send it so I can improve the auto deletion
                if self.Player.duration is None:
                    await botfunc.autoDelete(10,await self.bot.sendMessage("Currently playing `{}` in {}.\r\nQueue: {} left.".format(title, self.channel.name, self.__queue.size())))
                elif self.Player.is_live:
                    await botfunc.autoDelete(10,await self.bot.sendMessage("Currently playing `{}` (a livestream) in {}.\r\nQueue: {} left.".format(title, self.channel.name, self.__queue.size())))
                else:
                    await botfunc.autoDelete(10,await self.bot.sendMessage("Currently playing `{}` in {}.\r\nDuration: {}:{}\r\nQueue: {} left.".format(title, self.channel.name, mins, secs, self.__queue.size())))
            except:
                await botfunc.autoDelete(10,await self.bot.sendMessage("Currently playing {} (a file).".format(title)))
        except:
            logger.PrintException();

    async def __yt_play(self, MusicObj):
        ''' Plays a youtube url '''
        try:
            if not self.VC or not self.VC.is_connected:
                raise ClientException("Not connected to a channel")
            if self.Player is not None:
                raise PlayerException("Could not play. There's another player running.")
            try:
                opts = {
                    'default_search': 'auto',
                    'quiet': True,
                    'noplaylist': True,
                }
                self.Player = await self.VC.create_ytdl_player(MusicObj.url, after=lambda: self.__loop.create_task(self.playNext()), ytdl_options=opts)
            except DownloadError:
                await botfunc.autoDelete(10,await self.bot.sendMessage("Could not play `{}`. This video is banned in my country. :sob:".format(MusicObj.url)))
                await self.stop()
                await self.playNext()
                return False
            except:
                await botfunc.autoDelete(10,await self.bot.sendMessage("Could not play `{}`. There's something wrong with the link.".format(MusicObj.url)))
                await self.stop()
                await self.playNext()
                return False
            self.Player.start()
            self.Player.volume = await config.getConf(self.id, "music_bot_volume")
            if self.Player.title is not None:
                title = self.Player.title
            if self.Player.duration is not None:
                secs = self.Player.duration
                mins = math.floor(secs/60)
                secs-=(mins*60)
                mins = str(mins).zfill(2)
                secs = str(secs).zfill(2)
            if self.Player.duration is None:
                #await botfunc.autoDelete(10,await self.bot.sendMessage("Now playing `{}` in {}.\r\n**Requested by:** {}\r\n**Queue:** {} left.".format(title, self.channel.name, MusicObj.user, self.__queue.size())))
                self.oldmsg = await self.bot.sendMessage("Now playing `{}` in {}.\r\n**Requested by:** {} || **Queue:** {} left.".format(title, self.channel.name, MusicObj.user, self.__queue.size()))
            elif self.Player.is_live:
                #await botfunc.autoDelete(10,await self.bot.sendMessage("Now playing `{}` (a livestream) in {}.\r\n**Requested by:** {}\r\n**Queue:** {} left.".format(title, self.channel.name, MusicObj.user, self.__queue.size())))
                self.oldmsg = await self.bot.sendMessage("Now playing `{}` (a livestream) in {}.\r\n**Requested by:** {} || **Queue:** {} left.".format(title, self.channel.name, MusicObj.user, self.__queue.size()))
            else:
                #await botfunc.autoDelete(10,await self.bot.sendMessage("Now playing `{}` in {}.\r\n**Requested by:** {}\r\n**Duration:** {}:{}\r\n**Queue:** {} left.".format(title, self.channel.name, MusicObj.user, mins, secs, self.__queue.size())))
                self.oldmsg = await self.bot.sendMessage("Now playing `{}` in {}.\r\n**Requested by:** {} || **Duration:** {}:{} || **Queue:** {} left.".format(title, self.channel.name, MusicObj.user, mins, secs, self.__queue.size()))
        except:
            logger.PrintException();
