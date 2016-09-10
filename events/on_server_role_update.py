import discord
import asyncio
import string
from pprint import pprint
from functions import logger, groups, config, search
import global_vars

client = global_vars.client
@client.event
async def on_server_role_update(before, after):
    try:
        channel = await config.getConf(before.server.id, "log_channel")
        channel = await search.channel(before.server, channel)
        if channel != None:
            if after.permissions != before.permissions:
                changed = dict()
                permb = dict(before.permissions)
                for perm, value in list(after.permissions):
                    if permb[perm] != value:
                        changed[perm] = value
                        await client.send_message(channel, "Permission `{}` for role `{}` has been changed to `{}`".format(perm, after ,changed[perm]))
            elif before.colour != after.colour:
                await client.send_message(channel, "Color `{}` of `{}` role has been changed to `{}`".format(before.colour, after, after.colour))
    except:
        logger.PrintException()