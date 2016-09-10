import discord
import asyncio
import string
from pprint import pprint
from functions import logger, groups, config, search
import global_vars

client = global_vars.client
#@client.event
#async def on_member_ban(member):
#    channel = await config.getConf(member.server.id, "ban_log_channel")
#    channel = await search.channel(member.server, channel)
#    if channel != None:
#        await client.send_message(channel, ":hammer: **{0.name}#{0.discriminator}** has been banned. (**ID:** {0.id})".format(member))

@client.event
async def on_member_unban(server, user):
    try:
        channel = await config.getConf(server.id, "ban_log_channel")
        channel = await search.channel(server, channel)
        if channel != None:
            await client.send_message(channel, ":rainbow: **{0.name}#{0.discriminator}** is unbanned. (**ID:** {0.id})".format(user))
    except:
        logger.PrintException()