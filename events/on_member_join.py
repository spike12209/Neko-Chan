import discord
import asyncio
import re
from pprint import pprint
from functions import logger, groups, search, config
import global_vars

client = global_vars.client
@client.event
async def on_member_join(member):
    try:
        if await config.getConf(member.server.id, "joined_notification") == True:
            def replace(*key_values):
                replace_dict = dict(key_values)
                replacement_function = lambda match: replace_dict[match.group(0)]
                pattern = re.compile("|".join([re.escape(k) for k, v in key_values]), re.M)
                return lambda string: pattern.sub(replacement_function, string)
            replacements = (u"{mention}", member.mention), (u"{name}", member.display_name), (u"{server}", member.server.name)
            channel = await config.getConf(member.server.id, "announcement_channel")
            channel = await search.channel(member.server, channel)
            if channel != None:
                await client.send_message(channel, replace(*replacements)(await config.getConf(member.server.id, "join_message")))
    except:
        logger.PrintException()