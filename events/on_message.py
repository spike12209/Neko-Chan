import discord
import asyncio
import string
import re
import time
import importlib
import shlex
import re
from classes.messagehandler import MessageHandler
from pprint import pprint
from functions import logger, groups, config, aliases, disabledcmd, search, tools, messagestorage
import global_vars

client = global_vars.client


@client.event
async def on_message(message):
    try:
        user = str(message.author.name)
        msg = str(message.content).strip()
        printable = set(string.printable)
        logmsg = "".join(filter(lambda x: x in printable, msg))
        user = "".join(filter(lambda x: x in printable, user))
        msgt = time.strftime("%H:%M:%S", time.localtime())
        if message.channel.is_private and message.server is None:
            message.server = message.channel
            if not message.server.name:
                message.server.name = "Private"
        prefix = None
        force_exec = False
        access_level = 0
        if not message.channel.is_private:
            # Mass-mention autoban - maybe in future? Leaving it for now
            #if str(message.server.id) == "170511099567800320":
            #    if len(list(set(message.raw_mentions))) >= 5:
            #        mentions = await config.getConf(message.server.id, "massmentions_autoban")
            #        if len(list(set(message.raw_mentions))) >= mentions:
            #            print("k")
            # AntiSpam
            access_level = await groups.getLevel(message.server.id, message.author)
            # Check for a possible higher access level through the user roles
            if await messagestorage.store(message, access_level):
                action = await config.getConf(message.server.id, "antispam_action")
                action = action.casefold()
                try:
                    performed = False
                    if action == "move":
                        role = await config.getConf(message.server.id, "antispam_move_role")
                        role = await search.role(message.server, role)
                        if role is not None:
                            await global_vars.client.replace_roles(message.author, role)
                            if role.name.startswith("@"):
                                role = role.name[1:]
                            else:
                                role = role.name
                            await client.send_message(message.channel, ":loudspeaker: **{0.name}#{0.discriminator}** has been moved to role **{1}** for spamming.".format(message.author, role))
                            performed = True
                    elif action == "kick":
                        await global_vars.client.kick(message.author) # Kick the member
                        await client.send_message(message.channel, ":loudspeaker: **{0.name}#{0.discriminator}** has been **kicked** for spamming.".format(message.author))
                        performed = True
                    elif action == "ban":
                        await global_vars.client.ban(message.author) # Ban the member
                        await client.send_message(message.channel, ":loudspeaker: **{0.name}#{0.discriminator}** has been **banned** for spamming.".format(message.author))
                        performed = True
                    if performed:
                        # Purge last messages from DB
                        as_time = await config.getConf(message.server.id, "antispam_seconds")
                        await messagestorage.delete(message, as_time)
                except discord.Forbidden:
                    await config.setConf(message.server.id, "antispam_enabled", False)
                    await client.send_message(message.channel, ":x: I can't perform the selected anti-spam action. **Antispam disabled**".format(message.author.display_name))
                except:
                    logger.PrintException()
                return False
            # Bad way to unshort urls
            if message.author.id != client.user.id:
                #(https?:\/\/[a-z0-9\-\.]{1,128}\/[^\/\?\$]+)
                regex = r"(?P<url>https?://[^\s]+)"
                urls = re.findall(regex, message.content, re.I)
                if len(urls)>0:
                    amount_r = 0
                    unshorted_r = "URL's:\r\n"
                    for url in urls:
                        unshorted = await tools.unshort(re.sub('[!@\"\'#$]', '', url))
                        if unshorted is not None:
                            if await config.getConf(message.server.id, "unshort_urls") == True:
                                if unshorted != url:
                                    unshorted_r += "{}\r\n".format(unshorted)
                                    amount_r = amount_r+1
                    if amount_r > 0:
                        await client.send_message(message.channel, "`{}`".format(unshorted_r))
            # Auto invite ban
            if len(client.get_server(message.server.id).get_member(message.author.id).roles) == 1:
                if re.search("discord\.gg\/[a-z0-9]+", message.content, re.I):
                    if await config.getConf(message.server.id, "invite_autoban") == True:
                        if message.server.id == message.author.server.id:
                            try:
                                await client.ban(client.get_server(message.server.id).get_member(message.author.id), delete_message_days=1)
                                await client.send_message(message.channel, ":rainbow: Banned **{0.name}#{0.discriminator}** for advertising!".format(message.author))
                                channel = await config.getConf(message.server.id, "ban_log_channel")
                                channel = await search.channel(message.server, channel)
                                if channel != None:
                                    await client.send_message(channel, ":hammer: Auto-banned **{0.name}#{0.discriminator}** for advertising.\r\nMessage: {1}".format(message.author, message.content))
                            except discord.Forbidden:
                                return
            # Prefix
            if msg.startswith("<@") and len(message.raw_mentions)>0:
                if client.user.id == message.raw_mentions[0]:
                    force_exec = True
            if not force_exec:
                prefix = await config.getConf(message.server.id, "prefix")
                if prefix is None:
                    return False
        else:
            prefix = "!"
        if force_exec or (prefix is not None and msg.startswith(prefix)):
            # Log the message
            await logger.print_to_file("[MESSAGE] [{}][{}] {}: {}".format(msgt, message.server.name, user, logmsg))
            # Continue
            if force_exec:
                msg = re.sub("<@!?\d+>", "", msg, 1)
                message.raw_mentions.pop(0)
            else:
                msg = msg[len(prefix):]

            del prefix

            # Split using shlex if not sending a code
            if not msg.startswith("`") and not msg.endswith("`"):
                try:
                    msg = shlex.split(msg)
                except:
                    msg = msg.split(" ")
            else:
                # A code has been sent, just split using spaces
                msg = msg.split(" ")

            # Is a command supplied?
            if len(msg)==0 or not re.search("[A-Za-z0-9]", msg[0][:1]):
                return False

            if not message.channel.is_private:
                # Check for an alias if we're not in a private chat
                alias = await aliases.getAlias(message.server.id, msg[0])
                if alias is not None:
                    # Alias has been found.
                    # Remove the original command but leave the arguments
                    msg.pop(0)
                    #Interpret it just line an command.
                    new_command = shlex.split(alias)
                    index = 0
                    for arg in new_command:
                        # Prepend every single part of the alias to our original arguments
                        msg.insert(index, str(arg))
                        index = index+1
                    pass

            # First part of a message is always the command
            command = msg[0].lower()
            msg.pop(0)
            messagehandler = MessageHandler(client, message, command, msg)
            if not message.channel.is_private:
                if await disabledcmd.get(message.server.id, command) == True and await groups.getLevel(message.server.id, message.author) < 6:
                    return
                messagehandler.access_level = access_level
                messagehandler.needed_level = await groups.needed_level(message.server.id, command)
            else:
                messagehandler.needed_level = 0
                messagehandler.access_level = 0
            del msg
            # Has the user sufficient permissions?
            if not message.channel.is_private:
                if messagehandler.access_level < messagehandler.needed_level:
                    return False
            else:
                if messagehandler.needed_level > 0:
                    return False
            del command
            # Try to import the given command
            try:
                func = importlib.import_module('commands.' + messagehandler.command)
                importlib.reload(func)
            except Exception as e:
                # The command has not been found.
                if "No module named" in str(e) and messagehandler.command in str(e):
                    return False
                logger.PrintException(message)
                return
            try:
                # Let the users know I'm working.
                await client.send_typing(message.channel)
                # Pass the client, the message object and the args to the commands
                await func.init(messagehandler)
            except Exception as e:
                logger.PrintException(message)
        return None
    except Exception as e:
        logger.PrintException(message)
