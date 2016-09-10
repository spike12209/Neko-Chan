import os
import asyncio
#import aioodbc
import aiomysql
from functions import logger
import global_vars

loop = asyncio.get_event_loop()

async def getAll(server_id):
    '''Gets all tags of the server'''
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, charset='utf8') as con:
            async with await con.cursor(aiomysql.cursors.DictCursor) as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS tags (user_id VARCHAR(100) NOT NULL, tag VARCHAR(100) NOT NULL, text VARCHAR(1000) NOT NULL, creation_date VARCHAR(100) NOT NULL, PRIMARY KEY (tag));")
                await con.commit()
                await cur.execute("SELECT `tag` FROM tags;")
                data = await cur.fetchall()
        if data != None and len(data)>0:
            return data
    except:
        logger.PrintException()
    return None


async def get(server_id, tag):
    '''Gets the text of a specific tag'''
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, charset='utf8') as con:
            async with await con.cursor() as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS tags (user_id VARCHAR(100) NOT NULL, tag VARCHAR(100) NOT NULL, text VARCHAR(1000) NOT NULL, creation_date VARCHAR(100) NOT NULL, PRIMARY KEY (tag));")
                await con.commit()
                await cur.execute("SELECT * FROM tags WHERE LOWER(tag)=LOWER(%s);", (str(tag),))
                data = await cur.fetchone()
        if data != None:
            return data
    except:
        logger.PrintException()
    return None

async def set(server_id, user_id, tag, text, creation_date):
    '''Sets a new text for a tag'''
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, autocommit=True, charset='utf8') as con:
            async with await con.cursor() as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS tags (user_id VARCHAR(100) NOT NULL, tag VARCHAR(100) NOT NULL, text VARCHAR(1000) NOT NULL, creation_date VARCHAR(100) NOT NULL, PRIMARY KEY (tag));")
                await con.commit()
                await cur.execute("INSERT IGNORE INTO tags VALUES(%s,%s,%s,%s);", (str(user_id), str(tag), str(text), str(creation_date)))
                return cur.rowcount
    except:
        logger.PrintException()
        return False

async def delete(server_id, tag):
    '''Deletes an spefic alias from a server'''
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, autocommit=True, charset='utf8') as con:
            async with await con.cursor() as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS tags (user_id VARCHAR(100) NOT NULL, tag VARCHAR(100) NOT NULL, text VARCHAR(1000) NOT NULL, creation_date VARCHAR(100) NOT NULL, PRIMARY KEY (tag));")
                await con.commit()
                await cur.execute("DELETE FROM tags WHERE LOWER(tag)=LOWER(%s);", (str(tag),))
                return cur.rowcount
    except:
        logger.PrintException()
        return False
