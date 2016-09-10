from functions import logger,search
import pprint
import discord

DESC="Tells you something about the server"
USAGE="serverinfo"

async def init(bot):
    try:
        if not bot.message.channel.is_private:
            server = bot.message.server
            response = "```"
            response += "Name: {}\r\n".format(server.name)
            response += "ID: {}\r\n".format(server.id)
            response += "Owner: {}#{}\r\n".format(server.owner.name, server.owner.discriminator)
            response += "Default channel: {}\r\n".format(server.default_channel.name)
            response += "Created at: {} UTC\r\n".format(server.created_at)
            response += "Region: {}\r\n".format(server.region)
            response += "AFK Timeout: {} seconds\r\n".format(server.afk_timeout)
            if server.afk_channel is not None:
                response += "AFK Channel: {}\r\n".format(server.afk_channel.name)
            response += "Members: {}+{} idle/{}\r\n".format(sum(1 for m in server.members if m.status == discord.Status.online),sum(1 for m in server.members if m.status == discord.Status.idle) , len(server.members))
            response += "Text channels: {}\r\n".format(sum(1 for channel in server.channels if channel.type==discord.ChannelType.text))
            response += "Voice channels: {}".format(sum(1 for channel in server.channels if channel.type==discord.ChannelType.voice))
            if server.mfa_level>0:
                response += "\r\nThis server requires multi factor authorisation"
            response += "```"
            response += "{}".format(server.icon_url)
            await bot.sendMessage(response)
        else:
            await bot.sendMessage("We are talking on direct message! Try `userinfo` command instead.")
    except:
        logger.PrintException(bot.message)
