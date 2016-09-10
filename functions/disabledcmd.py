import os
import asyncio
#import aioodbc
import aiomysql
from functions import logger
import global_vars

loop = asyncio.get_event_loop()


async def getall(server_id):
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, charset='utf8') as con:
            async with await con.cursor(aiomysql.cursors.DictCursor) as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS disabledCmds (cmd VARCHAR(100) NOT NULL, PRIMARY KEY (cmd));")
                await con.commit()
                await cur.execute("SELECT * FROM disabledCmds;")
                data = await cur.fetchall()
        if data != None and len(data)>0:
            return data
    except:
        logger.PrintException()
    return None

async def get(server_id, cmd):
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, charset='utf8') as con:
            async with await con.cursor() as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS disabledCmds (cmd VARCHAR(100) NOT NULL, PRIMARY KEY (cmd));")
                await con.commit()
                await cur.execute("SELECT cmd FROM disabledCmds WHERE LOWER(cmd)=LOWER(%s);", (str(cmd),))
                data = await cur.fetchone()
                if data != None:
                    return True
                else:
                    return False
    except:
        logger.PrintException()
    return None

async def add(server_id, cmd):
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, autocommit=True, charset='utf8') as con:
            async with await con.cursor() as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS disabledCmds (cmd VARCHAR(100) NOT NULL, PRIMARY KEY (cmd));")
                await cur.execute("INSERT INTO disabledCmds VALUES(%s);", (str(cmd),))
        return True
    except:
        logger.PrintException()
        return False

async def delete(server_id, cmd):
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, autocommit=True, charset='utf8') as con:
            async with await con.cursor() as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS disabledCmds (cmd VARCHAR(100) NOT NULL, PRIMARY KEY (cmd));")
                await cur.execute("DELETE FROM disabledCmds WHERE LOWER(cmd)=LOWER(%s);", (str(cmd),))
        return True
    except:
        logger.PrintException()
        return False
