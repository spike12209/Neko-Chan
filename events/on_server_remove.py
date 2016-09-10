import discord
import asyncio
from functions import logger,startup
import global_vars
import os
import aiomysql

client = global_vars.client
@client.event
async def on_server_remove(server):
    try:
        if server.id in global_vars.music_bots:
            global_vars.music_bots[server.id].disconnect()
            del global_vars.music_bots[server.id]
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], autocommit=True) as con:
            async with await con.cursor() as cur:
                if len(server.id)>0 and not "*" in server.id:
                    server.id = str(server.id).replace("'", "\'")
                    server.id = str(server.id).replace('"', '\"')
                    await cur.execute("DROP DATABASE IF EXISTS srv_"+server.id+";")
        await logger.print_to_file("[BOT] Removed Server \"{}\" from database.".format(server.name))
    except:
        logger.PrintException()