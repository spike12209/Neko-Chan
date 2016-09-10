import os
import asyncio
#import aioodbc
import aiomysql
from functions import logger
import global_vars

loop = asyncio.get_event_loop()

async def getAliases(server_id):
    '''Gets all aliases for a server'''
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, charset='utf8') as con:
            async with await con.cursor(aiomysql.cursors.DictCursor) as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS aliases (alias VARCHAR(100) NOT NULL, command VARCHAR(255) NOT NULL, PRIMARY KEY (alias));")
                await con.commit()
                await cur.execute("SELECT * FROM aliases;")
                data = await cur.fetchall()
        if data != None and len(data)>0:
            return data
    except:
        logger.PrintException()
    return None

async def getReverse(server_id, command):
    '''Resolves a tag in reverse'''
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, charset='utf8') as con:
            async with await con.cursor() as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS aliases (alias VARCHAR(100) NOT NULL, command VARCHAR(255) NOT NULL, PRIMARY KEY (alias));")
                await con.commit()
                await cur.execute("SELECT alias FROM aliases WHERE LOWER(command)=LOWER(%s);", (str(command),))
                data = await cur.fetchone()
        if data != None:
            return str(data[0])
    except:
        logger.PrintException()
    return None

async def getAlias(server_id, alias):
    '''Gets a specific alias for a server'''
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, charset='utf8') as con:
            async with await con.cursor() as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS aliases (alias VARCHAR(100) NOT NULL, command VARCHAR(255) NOT NULL, PRIMARY KEY (alias));")
                await con.commit()
                await cur.execute("SELECT command FROM aliases WHERE LOWER(alias)=LOWER(%s);", (str(alias),))
                data = await cur.fetchone()
        if data != None:
            return str(data[0])
    except:
        logger.PrintException()
    return None

async def setAlias(server_id, alias, command):
    '''Sets an alias for a server'''
    try:
        '''file = os.path.join(global_vars.cwd, global_vars.database_dir, file)
        dsn = 'Driver=SQLite3;Database={}.db'.format(file)
        con = None
        async with aioodbc.connect(dsn=dsn, loop=loop) as con:
            async with con.cursor() as cur:'''
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, autocommit=True, charset='utf8') as con:
            async with await con.cursor() as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS aliases (alias VARCHAR(100) NOT NULL, command VARCHAR(255) NOT NULL, PRIMARY KEY (alias));")
                await cur.execute("INSERT INTO aliases VALUES(%s,%s);", (str(alias), str(command)))
                return cur.rowcount
    except:
        logger.PrintException()
        return False

async def deleteAlias(server_id, alias):
    '''Deletes an spefic alias from a server'''
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, autocommit=True, charset='utf8') as con:
            async with await con.cursor() as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS aliases (alias VARCHAR(100) NOT NULL, command VARCHAR(255) NOT NULL, PRIMARY KEY (alias));")
                await con.commit()
                await cur.execute("DELETE FROM aliases WHERE LOWER(alias)=LOWER(%s);", (str(alias),))
                return cur.rowcount
    except:
        logger.PrintException()
        return False
