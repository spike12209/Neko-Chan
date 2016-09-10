import discord
import asyncio
from functions import logger,startup
import global_vars
import os

client = global_vars.client
@client.event
async def on_channel_delete(channel):
    try:
        server = channel.server
        if server.id in global_vars.music_bots:
            # Music bots voice channel got deleted. Stopping playback.
            if global_vars.music_bots[server.id].channel.id == channel.id:
                await global_vars.music_bots[server.id].disconnect()
                del global_vars.music_bots[server.id]
            # The music bots text channel got deleted. Switching to servers main channel
            elif global_vars.music_bots[server.id].chat.id == channel.id:
                global_vars.music_bots[server.id].chat = server.get_default_channel()
    except:
        logger.PrintException()