import discord
import asyncio
import string
from pprint import pprint
from functions import logger, groups, config, search
import global_vars

client = global_vars.client
@client.event
async def on_member_update(before, after):
    try:
        if after.id != client.user.id:
            channel = await config.getConf(before.server.id, "log_channel")
            channel = await search.channel(before.server, channel)
            if channel != None:
                if before.display_name != after.display_name:
                    await client.send_message(channel, "`{}` is now known as `{}`".format(before.display_name, after.display_name))
                elif before.roles != after.roles:
                    if len(after.roles)-len(before.roles) > 0:
                        roles = list(set(after.roles) - set(before.roles))
                        for role in roles:
                            await client.send_message(channel, "`{}` received `{}` role!".format(after.display_name, role))
                    else:
                        roles = list(set(before.roles) - set(after.roles))
                        for role in roles:
                            await client.send_message(channel, "`{}` lost `{}` role!".format(after.display_name, role))
    except:
        logger.PrintException()