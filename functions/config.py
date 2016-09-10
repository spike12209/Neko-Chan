import os
import asyncio
#import aioodbc
from functions import logger, tools
import global_vars
from pydoc import locate
import aiomysql

loop = asyncio.get_event_loop()
async def setConf(server_id, setting, value):
    ''' Sets a config value.
    Args: server_id, setting, value'''
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, autocommit=True, charset='utf8') as con:
            async with await con.cursor() as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS config (`setting` VARCHAR(100) PRIMARY KEY NOT NULL, `value` VARCHAR(255), `type` VARCHAR(20), `desc` VARCHAR(255));")
                await cur.execute("UPDATE config SET `value`=%s WHERE `setting`=%s;", (value,str(setting)))
                return cur.rowcount
    except:
        logger.PrintException()
    return False

async def addConf(server_id, setting, value, type, description):
    ''' Adds a config value.
    Args: server_id,setting,value,type'''
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, autocommit=True, charset='utf8') as con:
            async with await con.cursor() as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS config (`setting` VARCHAR(100) PRIMARY KEY NOT NULL, `value` VARCHAR(255), `type` VARCHAR(20), `desc` VARCHAR(255));")
                await cur.execute("INSERT INTO config(`setting`,`value`,`type`,`desc`) VALUES (%s,%s,%s,%s);", (str(setting),str(value),str(type),str(description)))
                return cur.rowcount
    except:
        logger.PrintException()
    return False

async def delConf(server_id, setting):
    ''' Deletes a config value.
    Args: server_id, setting'''
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, autocommit=True, charset='utf8') as con:
            async with await con.cursor() as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS config (`setting` VARCHAR(100) PRIMARY KEY NOT NULL, `value` VARCHAR(255), `type` VARCHAR(20), `desc` VARCHAR(255));")
                await cur.execute("DELETE FROM config WHERE `setting`=%s;", (str(setting), ))
                return cur.rowcount
    except:
        logger.PrintException()
    return False

async def confData(server_id, setting):
    ''' Gets a config value.
    Args: server_id, setting'''
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, charset='utf8') as con:
            async with await con.cursor(aiomysql.cursors.DictCursor) as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS config (`setting` VARCHAR(100) PRIMARY KEY NOT NULL, `value` VARCHAR(255), `type` VARCHAR(20), `desc` VARCHAR(255));")
                await con.commit()
                await cur.execute("SELECT * FROM config WHERE `setting`=%s", (str(setting),))
                data = await cur.fetchone()
        if data != None and len(data)>0:
            return data
    except:
        logger.PrintException()
        return None

async def getConf(server_id, setting):
    ''' Gets a config value.
    Args: server_id, setting'''
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, charset='utf8') as con:
            async with await con.cursor(aiomysql.cursors.DictCursor) as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS config (`setting` VARCHAR(100) PRIMARY KEY NOT NULL, `value` VARCHAR(255), `type` VARCHAR(20), `desc` VARCHAR(255));")
                await con.commit()
                await cur.execute("SELECT * FROM config WHERE `setting`=%s", (str(setting),))
                data = await cur.fetchone()
        if data != None and len(data)>0:
            return tools.convertVal(data['type'], data['value'])
    except:
        logger.PrintException()
        return None

async def getAllConf(server_id):
    ''' Gets all configuration values
    Args: server_id'''
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server_id, charset='utf8') as con:
            async with await con.cursor(aiomysql.cursors.DictCursor) as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS config (`setting` VARCHAR(100) PRIMARY KEY NOT NULL, `value` VARCHAR(255), `type` VARCHAR(20), `desc` VARCHAR(255));")
                await con.commit()
                await cur.execute("SELECT * FROM config ORDER BY `setting` ASC;")
                data = await cur.fetchall()
        if data != None and len(data)>0:
            return data
    except:
        logger.PrintException()
        return None
