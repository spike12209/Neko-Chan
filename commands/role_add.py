import pprint
import importlib
import re
from discord.utils import find
from functions import groups,search,logger
import discord

DESC="Add role to someone!"
USAGE="role_add [role] [member]"

async def init(bot):
    chat=bot.message.channel
    response = ""
    try:
        crole = str(bot.args[0])
        role = find(lambda r: r.name == str(bot.args[0]), bot.message.server.roles)
        bot.args.pop(0)
        if role is None:
            await bot.sendMessage( "`{}` is not a valid role. (Usage: role_add [`role`] [`member`])".format(crole))
            return False
        if len(bot.args)>0:
            if len(bot.message.raw_mentions)>0:
                user = await search.user(chat, bot.message.raw_mentions[0])
            else:
                user = await search.user(chat, " ".join(bot.args))
        else:
            await bot.sendMessage( "You have to specify a user.")
            return False
        if user is not None:
            try:
                await bot.client.add_roles(user, role)
                await bot.sendMessage( "Role `{}` has been added to `{}`.".format(role, user))
            except discord.Forbidden:
                await bot.sendMessage( "This role is above bot role, i can't do that!")
        else:
            await bot.sendMessage( "`{}` is not a valid user! (Usage: role_add [`role`] [`member`])".format(bot.args[0]))
            return False
    except Exception:
        logger.PrintException(bot.message)
        return False
