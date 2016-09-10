import discord
import asyncio
from functions import logger,startup
import global_vars
import os

client = global_vars.client
@client.event
async def on_voice_state_update(before, after):
    try:
        server = before.server.id
        old_channel = before.voice_channel
        new_channel = after.voice_channel
        if after.id == after.server.me.id:
            if server in global_vars.music_bots:
                global_vars.music_bots[server].channel = new_channel
                return
        if server in global_vars.music_bots:
            if old_channel:
                # Was the user in the same channel as the music bot before?
                if global_vars.music_bots[server].channel.id == old_channel.id:
                    # Is the user not connected to voice or not in the same channel as the bot anymore?
                    if new_channel is None or global_vars.music_bots[server].channel.id != new_channel.id:
                        if len(global_vars.music_bots[server].channel.voice_members)<=1:
                            if global_vars.music_bots[server].auto_dc:
                                await global_vars.music_bots[server].disconnect()
                                return False
                        else:
                            if before.id == global_vars.music_bots[server].sender.id:
                                new_owner = global_vars.music_bots[server].channel.voice_members[0]
                                if new_owner.id == before.server.me.id:
                                    new_owner = global_vars.music_bots[server].channel.voice_members[1]
                                global_vars.music_bots[server].sender = new_owner
                                await global_vars.client.send_message(global_vars.music_bots[server].chat, ":notes: Music-Bot ownership transfered to `{0.display_name}`".format(new_owner))
                        # The user has voted for a skip!
                        if before.id in global_vars.music_bots[server].skipvotes:
                            # Your vote is now invalid
                            global_vars.music_bots[server].skipvotes.remove(before.id)
            elif new_channel is not None and (global_vars.music_bots[server].sender is None or (global_vars.music_bots[server].channel.id == new_channel.id and after.id != global_vars.music_bots[server].sender.id)):
                print(len(global_vars.music_bots[server].channel.voice_members))
                if len(global_vars.music_bots[server].channel.voice_members)!=2:
                    return
                new_owner = global_vars.music_bots[server].channel.voice_members[0]
                if new_owner.id == after.server.me.id:
                    new_owner = global_vars.music_bots[server].channel.voice_members[1]
                global_vars.music_bots[server].sender = new_owner
                await global_vars.client.send_message(global_vars.music_bots[server].chat, ":notes: Music-Bot ownership transfered to `{0.display_name}`".format(new_owner))
    except:
        logger.PrintException()