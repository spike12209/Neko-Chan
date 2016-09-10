from functions import logger,search, messagestorage, search
import pprint
import datetime

DESC="Tells you something about yourself or a user"
USAGE="userinfo"

async def init(bot):
    chat=bot.message.channel
    try:
        user = bot.message.author
        if len(bot.args) > 0:
            if len(bot.message.raw_mentions)>0:
                user = await search.user(chat, bot.message.raw_mentions[0])
            else:
                user = await search.user(chat, " ".join(bot.args))
        data = "Could not find any user matching {}".format(" ".join(bot.args))
        if user is not None:
            data = []
            if user.bot:
                data.append(["<!-- Bot information -->"])
            else:
                data.append(["<!-- User information -->"])
            data.append(["ID", user.id])
            data.append(["Nickname", user.display_name])
            data.append(["Name", user.name])
            data.append(["Discriminator", user.discriminator])
            data.append(["Created on", user.created_at])
            if user.is_afk:
                data.append(["Status", str(user.status)+" [AFK]"])
            else:
                data.append(["Status", user.status])
            if user.game is not None:
                data.append(["Playing", user.game])
            if not bot.message.channel.is_private and user.server is not None:
                #======== MESSAGE STATS ========
                stats = await messagestorage.stats(user.server.id, user.id)
                if stats is not None:
                    data.append(["<!-- 30 day stats -->"])
                    data.append(["Sent messages", stats['count']])
                    if stats['seen'] is not None:
                        data.append(["Last message", datetime.datetime.fromtimestamp(stats['seen']).strftime('%Y-%m-%d %H:%M:%S')])
                    if stats['channel'] is not None and len(stats['channel'])>0:
                        data.append(["Last seen", (await search.channel(user.server, stats['channel'])).name])
                #======== Server STATS =========
                data.append(["<!-- Server stats -->"])
                data.append(["Joined on", user.joined_at])
                if user.self_mute:
                    data.append(["Voice status", "Muted"])
                if user.voice_channel:
                        data.append(["Voice channel", user.voice_channel.name])
                msg = ""
                for row in data:
                    if len(row)==1:
                        msg += '\r\n{0!s:^40}'.format(row[0])
                    else:
                        msg += '\r\n{0!s:>15} :{1!s:<10}'.format(row[0], row[1])
                if len(user.roles) > 1:
                    msg += "\r\n{0!s:>15}  {1!s:<10}".format("Roles", "")
                    for role in user.roles:
                        if not role.is_everyone:
                            msg += "\r\n{0!s:>15}  {1!s:<10}".format(" ",role)
                #==============================================
            await bot.sendMessage( "```xl\r\n{}```".format(msg));
        else:
            await bot.sendMessage( "S-Sorry senpai. I can't find the user you asked for :sob:");
    except Exception:
        logger.PrintException(bot.message);
