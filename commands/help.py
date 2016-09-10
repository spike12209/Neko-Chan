from os import listdir
from os.path import isfile, join
import global_vars
import discord
import importlib
from functions import logger, groups, config, aliases, disabledcmd
from pprint import pprint
import datetime
import asyncio
import aiohttp

dt = datetime.datetime
DESC="Shows the help"
USAGE="help"

async def generateHelp(bot):
    try:
        if not bot.channel.is_private:
            prefix = await config.getConf(bot.message.server.id, "prefix")
        else:
            prefix = "!"
        modules = [ f for f in listdir("commands/") if isfile(join("commands/",f)) and not ".pyc" in f and not "__" in f]
        response = "-- Command list --\r\n"
        modules.sort()
        modules = iter(modules)
        for command in modules:
            command = command.replace(".py","")
            if not bot.channel.is_private:
                if await disabledcmd.get(bot.message.server.id, command) == True:
                    continue
            # Has the user sufficient permissions?
                needed_level = await groups.needed_level(bot.message.server.id, command)
            else:
                for cmd in global_vars.default_access:
                    if command in cmd:
                        needed_level = cmd[1]
            if needed_level > 0:
                if not bot.channel.is_private:
                    if bot.access_level < needed_level:
                        continue
                else:
                    continue
            response += "{}{}\r\n".format(prefix, command)
        return response
    except:
        logger.PrintException(bot.message)
        return None

async def generateRest(bot):
    if not bot.channel.is_private:
        prefix = await config.getConf(bot.message.server.id, "prefix")
    else:
        prefix = "!"
    response = ""
    response += """!Use "how [command]" to check information about choosen command!

    Users can be specified by:
     - Mentioning them
     - User ID
     - Username#Discriminator
     - Username
     - Display Name"""
    if not bot.channel.is_private:
        modules = await aliases.getAliases(bot.message.server.id);
        if modules is not None:
            response += "\r\n\r\n--- Available aliases ---\r\n"
            for command in modules:
                response += "{0}{1} -> {0}{2}\r\n".format(prefix, command['alias'], command['command'])
    return response


async def init(bot):
    # Generate Help document
    help = await generateHelp(bot)
    # Only try if help has been generated
    if help is not None:
        try:
            try:
                await bot.sendMessage( "```{}```".format(help), bot.message.author)
                await bot.sendMessage( "```diff\n{}```".format(await generateRest(bot)), bot.message.author)
                await bot.sendMessage( "I've PM'd you the available commands to reduce spam. :upside_down:")
            except discord.Forbidden:
                # Let's check if we have cached a previous generated pastebin url.
                if len(global_vars.pastebin_url)==0 or global_vars.pastebin_date is None or global_vars.pastebin_date+datetime.timedelta(days=1) <= dt.now():
                    # No pastebin url found or too old (older than 1 Day)
                    # Generate a new Pastebin URL
                    data={"api_dev_key": global_vars.pastebin_api_key,"api_user_key": '', "api_paste_name": 'LLSG-Bot Help',"api_paste_format": 'text',"api_paste_private": '1',"api_paste_expire_date": '1D',"api_option": 'paste',"api_paste_code": help}
                    with aiohttp.ClientSession() as session:
                        async with session.post("http://pastebin.com/api/api_post.php", data=data) as r:
                            url = await r.text()
                    if url is not None:
                        global_vars.pastebin_url = url
                        global_vars.pastebin_date = dt.now()
                        # Send the newly generated link to the chat
                        await bot.sendMessage( 'Here\'s the lastest help:\r\n{}'.format(url))
                    else:
                        # Could not generate pastebin url. Sorry.
                        await bot.sendMessage( 'Sorry. I failed pushing the help to pastebin.:sob:\r\nPlease report us this occurence using !bug \"message\".')
                else:
                    # We have a cached URL which is not older than one day. Take this one.
                    await bot.sendMessage('Here\'s the help as of {}-{}-{}.\r\n{}'.format(global_vars.pastebin_date.year, global_vars.pastebin_date.month, global_vars.pastebin_date.day, global_vars.pastebin_url))
        except:
            logger.PrintException(bot.message)
