import discord
import asyncio
import string
from pprint import pprint
from functions import logger, groups, config, search
import global_vars
import json

client = global_vars.client
@client.event
async def on_socket_raw_receive(msg):
    try:
        if type(msg) == str:
            raw = json.loads(msg)
            if raw['t'] == "GUILD_BAN_ADD":
                #if raw['d']['guild_id'] == "170511099567800320":
                channel = await config.getConf(raw['d']['guild_id'], "ban_log_channel")
                channel = await search.channel(client.get_server(raw['d']['guild_id']), channel)
                if channel != None:
                    await client.send_message(channel, ":hammer: **{username}#{discriminator}** has been banned. (**ID:** {id})".format(**raw['d']['user']))
    except:
        logger.PrintException()