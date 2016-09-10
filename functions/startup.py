import os
import global_vars
from os import listdir
from os.path import isfile, join
from functions import groups, config, logger
import asyncio
import aiomysql


async def createDatabases(server_id=None):
    '''Creates the databases for all servers (if not already existent)'''
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], autocommit=True, charset='utf8') as conn:
            async with await conn.cursor() as cur:
                if server_id != None:
                    try:
                        if len(server_id)>0 and not "*" in server_id:
                            server_id = str(server_id).replace("'", "\'")
                            server_id = str(server_id).replace('"', '\"')
                            await cur.execute("CREATE DATABASE IF NOT EXISTS srv_"+server_id+";")
                    except:
                        logger.PrintException();
                else:
                    for server in global_vars.client.servers:
                        try:
                            if len(server.id)>0 and not "*" in server.id:
                                server.id = str(server.id).replace("'", "\'")
                                server.id = str(server.id).replace('"', '\"')
                                await cur.execute("CREATE DATABASE IF NOT EXISTS srv_"+server.id+";")
                        except:
                            logger.PrintException();
    except:
        logger.PrintException();

async def defaultLevels(server_id=None):
    ''' Sets all the default access levels in all servers'''
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], autocommit=True, charset='utf8') as con:
            async with await con.cursor(aiomysql.cursors.DictCursor) as cur:
                if server_id != None:
                    server_id = "srv_"+server_id
                    await cur.execute("USE "+server_id+";")
                    await cur.execute("CREATE TABLE IF NOT EXISTS command_levels (command VARCHAR(100) NOT NULL, level SMALLINT, PRIMARY KEY (command));")
                    for val in global_vars.default_access:
                        await cur.execute("INSERT IGNORE INTO command_levels (`command`, `level`) VALUES (%s, %s);", (val[0], val[1]))
                else:
                    for server in global_vars.client.servers:
                        server_id = "srv_"+server.id
                        await cur.execute("USE "+server_id+";")
                        await cur.execute("CREATE TABLE IF NOT EXISTS command_levels (command VARCHAR(100) NOT NULL, level SMALLINT, PRIMARY KEY (command));")
                        for val in global_vars.default_access:
                            await cur.execute("INSERT IGNORE INTO command_levels (`command`, `level`) VALUES (%s, %s);", (val[0], val[1]))
    except:
        logger.PrintException();
        
async def setAdmins(server_id=None):
    ''' Sets the bot administrators to highest level in all databases '''
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], autocommit=True, charset='utf8') as con:
            async with await con.cursor(aiomysql.cursors.DictCursor) as cur:
                if server_id != None:
                    server_id = "srv_"+server_id
                    await cur.execute("USE "+server_id+";")
                    await cur.execute("CREATE TABLE IF NOT EXISTS ranks (user VARCHAR(100) NOT NULL, rank SMALLINT, PRIMARY KEY (user));")
                    for d_val in global_vars.botadmins:
                        #print("[ACCESS] Setting {}'s Access Level to 6".format(d_val[1].rstrip()))
                        if d_val[2] == 0:
                            await cur.execute("DELETE FROM ranks WHERE `user`=%s", (d_val[0]))
                        else:
                            await cur.execute("INSERT INTO ranks (`user`, `rank`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `rank`=VALUES(`rank`);", (d_val[0],d_val[2]))
                else:
                    for server in global_vars.client.servers:
                        server_id = "srv_"+server.id
                        await cur.execute("USE "+server_id+";")
                        await cur.execute("CREATE TABLE IF NOT EXISTS ranks (user VARCHAR(100) NOT NULL, rank SMALLINT, PRIMARY KEY (user));")
                        #print("[ACCESS] Bot Admins on "+server_id)
                        for d_val in global_vars.botadmins:
                            #print("[ACCESS] Setting {}'s Access Level to 6".format(d_val[1].rstrip()))
                            if d_val[2] == 0:
                                await cur.execute("DELETE FROM ranks WHERE `user`=%s", (d_val[0]))
                            else:
                                await cur.execute("INSERT INTO ranks (`user`, `rank`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `rank`=VALUES(`rank`);", (d_val[0],d_val[2]))
    except:
        logger.PrintException();

async def defaultConfig(server_id=None):
    ''' Sets the default configuration to all databases, if not existent '''
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], autocommit=True, charset='utf8') as con:
            async with await con.cursor(aiomysql.cursors.DictCursor) as cur:
                if server_id != None:
                    server_id = "srv_"+server_id
                    await cur.execute("USE "+server_id+";")
                    await cur.execute("CREATE TABLE IF NOT EXISTS config (`setting` VARCHAR(100) PRIMARY KEY NOT NULL, `value` VARCHAR(255), `type` VARCHAR(20), `desc` VARCHAR(255));")
                    for d_val in global_vars.defaultvalues:
                        #print("[CONFIG] ({}){}: {}".format(d_val[2],d_val[0],d_val[1]))
                        await cur.execute("SELECT * FROM config WHERE `setting`=%s", (d_val[0],))
                        data = await cur.fetchone()
                        if data is None or len(data)==0:
                            await cur.execute("INSERT INTO config(`setting`,`value`,`type`,`desc`) VALUES (%s,%s,%s,%s);", (d_val[0],d_val[1],d_val[2],d_val[3]))
                else:
                    for server in global_vars.client.servers:
                        server_id = "srv_"+server.id
                        await cur.execute("USE "+server_id+";")
                        await cur.execute("CREATE TABLE IF NOT EXISTS config (`setting` VARCHAR(100) PRIMARY KEY NOT NULL, `value` VARCHAR(255), `type` VARCHAR(20), `desc` VARCHAR(255));")
                        #print("[CONFIG] Default config for "+server_id)
                        for d_val in global_vars.defaultvalues:
                            #print("[CONFIG] ({}){}: {}".format(d_val[2],d_val[0],d_val[1]))
                            await cur.execute("SELECT * FROM config WHERE `setting`=%s", (d_val[0],))
                            data = await cur.fetchone()
                            if data is None or len(data)==0:
                                await cur.execute("INSERT INTO config(`setting`,`value`,`type`,`desc`) VALUES (%s,%s,%s,%s);", (d_val[0],d_val[1],d_val[2],d_val[3]))
    except:
        logger.PrintException()