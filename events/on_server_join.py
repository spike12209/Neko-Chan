import discord
import asyncio
from pprint import pprint
from functions import logger,startup, groups, config
import global_vars
import aiomysql

client = global_vars.client
@client.event
async def on_server_join(server):
    try:
        await startup.createDatabases(server.id)
        await logger.print_to_file('[BOT] Setting default access levels')
        await startup.defaultLevels(server.id)
        await logger.print_to_file('[BOT] Setting bot administrators')
        await startup.setAdmins(server.id)
        await logger.print_to_file('[BOT] Setting default config values')
        await startup.defaultConfig(server.id)
        await logger.print_to_file("[BOT] Setting \"\" to access level 5".format(server.owner.display_name))
        await groups.setLevel(server.id, server.owner.id, 5)
        
        await client.send_message(server.default_channel, """Hello there. :wave:
My name is `{}` and I'm a bot.
`{}` added me to this server so (s)he's my master on this server at the moment.
If you want to see the avaiable commands, just type `{}help`.
I will then PM you with all commands that you are able to use.
I'm looking forward being with you :slight_smile:

**Information for Server Owner:**
If this bot collides with another bot mention me and type
`config prefix "prefix"`
to change the command prefix.""".format(client.user.name, server.owner.display_name, await config.getConf(server.id, "prefix")))
    except:
        logger.PrintException()