import os
import asyncio
import time
import aiomysql
from functions import logger, config
import global_vars

loop = asyncio.get_event_loop()

async def store(message, access_level: int):
    '''Stores the message into the database'''
    try:
        as_enabled = await config.getConf(message.server.id, "antispam_enabled")
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+message.server.id, autocommit=True, charset='utf8') as con:
            async with await con.cursor(aiomysql.cursors.DictCursor) as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS `messages` (`id` INT NOT NULL AUTO_INCREMENT,`channel` VARCHAR(100) NULL,`author` VARCHAR(100) NULL,`time` INT NULL,`message` TEXT(2000) NULL,PRIMARY KEY (`id`)) COLLATE 'utf8_bin';")
                await cur.execute("DELETE FROM `messages` WHERE `time`<%s;", (time.time()-(60*60*24*30)))
                await cur.execute("INSERT INTO `messages` (`channel`,`author`,`time`,`message`) VALUES (%s,%s,%s,%s);", (message.channel.id, message.author.id, time.time(), message.content))
                if as_enabled and not message.author.id == global_vars.client.user.id:
                    as_count = await config.getConf(message.server.id, "antispam_messages")
                    as_time = await config.getConf(message.server.id, "antispam_seconds")
                    as_ignore = await config.getConf(message.server.id, "antispam_ignore_level")
                    if as_ignore > access_level:
                        await cur.execute("SELECT COUNT(`id`) as count FROM `messages` WHERE `time`>%s AND `author`=%s;", (time.time()-as_time, message.author.id))
                        data = await cur.fetchone()
                        if data is not None:
                            if int(data['count']) >= as_count:
                                return True
    except:
        logger.PrintException(message)
    return False

async def delete(message, seconds: int=None, amount :int=None):
    '''Deletes x messages from from specified message author'''
    try:
        as_enabled = await config.getConf(message.server.id, "antispam_enabled")
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+message.server.id, autocommit=True, charset='utf8') as con:
            async with await con.cursor(aiomysql.cursors.DictCursor) as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS `messages` (`id` INT NOT NULL AUTO_INCREMENT,`channel` VARCHAR(100) NULL,`author` VARCHAR(100) NULL,`time` INT NULL,`message` TEXT(2000) NULL,PRIMARY KEY (`id`)) COLLATE 'utf8_bin';")
                if seconds is None and amount is not None:
                    await cur.execute("DELETE FROM `messages` WHERE `author`=%s LIMIT %d;", (message.author.id, int(amount)))
                elif amount is None and seconds is not None:
                    await cur.execute("DELETE FROM `messages` WHERE `time`>=%s AND `author`=%s;", (time.time()-(seconds), message.author.id))
                return True
    except:
        logger.PrintException(message)
    return False
    

async def stats(server:int, user: int):
    '''Returns the message stats of a user'''
    try:
        async with await aiomysql.connect(host=global_vars.mysql_data['host'], port=global_vars.mysql_data['port'], user=global_vars.mysql_data['user'], password=global_vars.mysql_data['password'], db="srv_"+server, autocommit=True, charset='utf8') as con:
            async with await con.cursor(aiomysql.cursors.DictCursor) as cur:
                await cur.execute("CREATE TABLE IF NOT EXISTS `messages` (`id` INT NOT NULL AUTO_INCREMENT,`channel` VARCHAR(100) NULL,`author` VARCHAR(100) NULL,`time` INT NULL,`message` TEXT(2000) NULL,PRIMARY KEY (`id`)) COLLATE 'utf8_bin';")
                await cur.execute("SELECT COUNT(`id`) as `count`, MAX(`time`) AS `seen`, s.`channel` FROM `messages`INNER JOIN (SELECT `channel` FROM `messages` WHERE author=%s ORDER BY `id` DESC LIMIT 1) s WHERE author=%s ;", (user, user))
                data = await cur.fetchone()
                if data is not None:
                    return data
    except:
        logger.PrintException(message)
    return None