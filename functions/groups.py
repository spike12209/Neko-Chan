import os
import asyncio
#import aioodbc
import aiomysql
from functions import logger
import global_vars

loop = asyncio.get_event_loop()

async def needed_level(server_id, command):
    level = 6
    command = command.casefold()
    async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, charset='utf8') as con:
        async with await con.cursor(aiomysql.cursors.DictCursor) as cur:
            await cur.execute("SELECT level FROM command_levels WHERE command=%s;", (command,))
            data = await cur.fetchone()
            if data != None:
                level = int(data['level'])
    return level

async def getLevel(server_id, user):
    access_level = 0
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, charset='utf8') as con:
            async with await con.cursor() as cur:
                await cur.execute("SELECT rank FROM ranks WHERE user=%s;", (user.id,))
                data = await cur.fetchone()
                if data is not None:
                    access_level = int(data[0])
                else:
                    await cur.execute("CREATE TABLE IF NOT EXISTS `rank_link` (`role` VARCHAR(100) NOT NULL,`rank` SMALLINT NULL,PRIMARY KEY (`role`));")
                    await cur.execute("SELECT role,rank FROM rank_link;")
                    data = await cur.fetchall()
                    if data is not None and len(data)>0:
                        roles = []
                        for r in user.roles:
                            roles.append(r.id)
                        if len(roles)>0:
                            # Iterate through the linkings
                            for link in data:
                                # User has that role
                                if not link[0] in roles:
                                    continue;
                                # The rank is a digit
                                level = link[1]
                                if not isinstance(level,int):
                                    if level.isdigit():
                                        level = int(level)
                                if not isinstance(level,int):
                                    continue;
                                # The level is higher than the users level.
                                if level>access_level:
                                    access_level = level
    except:
        logger.PrintException()
    return access_level

async def setLevel(server_id, user, level):
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, autocommit=True, charset='utf8') as con:
            async with await con.cursor(aiomysql.cursors.DictCursor) as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS ranks (user VARCHAR(100) NOT NULL, rank SMALLINT, PRIMARY KEY (user));")
                await cur.execute("INSERT INTO ranks (`user`, `rank`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `rank`=VALUES(`rank`);", (user, level))
        return True
    except:
        logger.PrintException()
    return False

async def unsetLevel(server_id, user):
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, autocommit=True, charset='utf8') as con:
            async with await con.cursor(aiomysql.cursors.DictCursor) as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS ranks (user VARCHAR(100) NOT NULL, rank SMALLINT, PRIMARY KEY (user));")
                await cur.execute("DELETE FROM ranks WHERE `user`=%s", (user,))
        return True
    except:
        logger.PrintException()
    return False

async def getLinks(server_id):
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, charset='utf8') as con:
            async with await con.cursor() as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS `rank_link` (`role` VARCHAR(100) NOT NULL,`rank` SMALLINT NULL,PRIMARY KEY (`role`));")
                await cur.execute("SELECT role,rank FROM rank_link;")
                data = await cur.fetchall()
        if data != None and len(data)>0:
            return data
    except:
        logger.PrintException()
    return None

async def getLink(server_id, role):
    level = 0
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, charset='utf8') as con:
            async with await con.cursor() as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS `rank_link` (`role` VARCHAR(100) NOT NULL,`rank` SMALLINT NULL,PRIMARY KEY (`role`));")
                await cur.execute("SELECT rank FROM rank_link WHERE role=%s;", (role,))
                data = await cur.fetchone()
                if data != None:
                    level = int(data[0])
    except:
        logger.PrintException()
    return level

async def setLink(server_id, role, level):
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, autocommit=True, charset='utf8') as con:
            async with await con.cursor(aiomysql.cursors.DictCursor) as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS `rank_link` (`role` VARCHAR(100) NOT NULL,`rank` SMALLINT NULL,PRIMARY KEY (`role`));")
                await cur.execute("INSERT INTO rank_link (`role`, `rank`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `rank`=VALUES(`rank`);", (role, level))
        return True
    except:
        logger.PrintException()
        return False

async def deleteLink(server_id, role):
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, autocommit=True, charset='utf8') as con:
            async with await con.cursor(aiomysql.cursors.DictCursor) as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS `rank_link` (`role` VARCHAR(100) NOT NULL,`rank` SMALLINT NULL,PRIMARY KEY (`role`));")
                await cur.execute("DELETE FROM rank_link WHERE `role`=%s;", (role,))
        return True
    except:
        logger.PrintException()
        return False
