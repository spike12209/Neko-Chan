import discord
from functions import logger
import re
import global_vars

async def banned_user(server, needle):
    ''' Returns a user object if found on the server's ban list '''
    try:
        user = None
        needle = str(needle)
        try:
            bans = await global_vars.client.get_bans(server)
        except discord.Forbidden:
            return None
        if re.match("<@\d+>",needle):
            user = discord.utils.find(lambda m: m.mention == needle, bans)
        elif re.match("\d+",needle):
            user = discord.utils.find(lambda m: m.id == needle, bans)
        elif re.match(".*#\d+",needle):
            split = needle.split("#")
            user = discord.utils.find(lambda m: (m.name.casefold() == split[0].casefold() and m.discriminator == split[1]), bans)
        if user is None:
            user = discord.utils.find(lambda m: m.name.casefold() == needle.casefold(), bans)
        return user
    except Exception:
        logger.PrintException()
        return None

async def user(chat, needle):
    ''' Returns a member object if found on the server '''
    try:
        user = None
        needle = str(needle)
        if re.match("<@\d+>",needle):
            user = discord.utils.find(lambda m: m.mention == needle.replace("!",""), chat.server.members)
        elif re.match("\d+",needle):
            user = discord.utils.find(lambda m: m.id == needle, chat.server.members)
        elif re.match(".*#\d+",needle):
            split = needle.split("#")
            user = discord.utils.find(lambda m: (m.name.casefold() == split[0].casefold() and m.discriminator == split[1]), chat.server.members)
        if user is None:
            user = discord.utils.find(lambda m: m.name.casefold() == needle.casefold(), chat.server.members)
            if user is None:
                user = discord.utils.find(lambda m: m.display_name.casefold() == needle.casefold(), chat.server.members)
        return user
    except Exception:
        logger.PrintException()
        return None

async def channel(server, needle):
    ''' Returns a channel object if found on the server '''
    try:
        channel = None
        needle = str(needle)
        if re.match("<#\d+>",needle):
            channel = discord.utils.find(lambda c: c.mention == needle, server.channels)
        elif re.match("\d+",needle):
            channel = discord.utils.find(lambda c: c.id == needle, server.channels)
        else:
            channel = discord.utils.find(lambda c: c.name.casefold() == needle.casefold(), server.channels)
        return channel
    except Exception:
        logger.PrintException()
    return None

async def role(server, needle):
    ''' Returns a role object if found on the server '''
    try:
        role = None
        needle = str(needle)
        if re.match("<#\d+>",needle):
            role = discord.utils.find(lambda c: c.mention == needle, server.roles)
        elif re.match("\d+",needle):
            role = discord.utils.find(lambda c: c.id == needle, server.roles)
        else:
            role = discord.utils.find(lambda c: c.name.casefold() == needle.casefold(), server.roles)
        return role
    except Exception:
        logger.PrintException()
    return None
