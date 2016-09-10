from functions import groups,search,logger,config
import discord

DESC="Unban member"
USAGE="unban [member]"

async def init(bot):
    chat=bot.message.channel
    #user=str(bot.message.author.name)
    try:
        if len(bot.args)>0:
            try:
                if len(bot.message.raw_mentions)>0:
                    user = await search.banned_user(bot.message.server, bot.message.raw_mentions[0])
                else:
                    user = await search.banned_user(bot.message.server, " ".join(bot.args))
                if user is not None:
                    await bot.client.unban(bot.message.server,user)
                else:
                    await bot.sendMessage( ':x: This user was not found on this server\'s ban list or bot doesn\'t have access to it.')
            except discord.Forbidden:
                await bot.sendMessage( ':x: The bot does not have permissions to unban members.')
    except Exception:
        logger.PrintException(bot.message)
        return False
