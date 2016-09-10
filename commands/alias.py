from functions import config,aliases,logger,tools

DESC="Set/Get/Delete an alias"
USAGE="alias [command] [new command/delete]"

async def init(bot):
    chat=bot.message.channel
    try:
        if bot.message.channel.is_private:
            await bot.sendMessage( "This command is disabled in private chats!")
            return False
        if len(bot.args)==0:
            alias_list = await aliases.getAliases(bot.message.server.id);
            response = ""
            if alias_list is not None:
                for alias in alias_list:
                    response += "{0}{1} -> {0}{2}\r\n".format(await config.getConf(bot.message.server.id, "prefix"), alias['alias'], alias['command'])
            else:
                response  = "No aliases found.";
            await bot.sendMessage( "```{}```".format(response))
        elif len(bot.args)==1:
            alias = await aliases.getAlias(bot.message.server.id, str(bot.args[0]));
            if alias is not None:
                response = "{0}{1} -> {0}{2}".format(await config.getConf(bot.message.server.id, "prefix"), bot.args[0], alias)
            else:
                response = "Alias \"{}\" couldn't be found".format(bot.args[0]);
            await bot.sendMessage( "`{}`".format(response))
        else:
            prefix = await config.getConf(bot.message.server.id, "prefix")
            alias = bot.args[0]
            bot.args.pop(0)
            value = " ".join(bot.args)
            if value is not None:
                if value.casefold()=="delete" or value.casefold()=="remove" or value.casefold()=="null" or value.casefold()=="none":
                    if await aliases.deleteAlias(bot.message.server.id, alias):
                        response = "Alias \"{0}{1}\" has been deleted!".format(prefix, alias);
                    else:
                        response = "Alias \"{0}{1}\" could not be deleted!".format(prefix, alias);
                else:
                    if await aliases.setAlias(bot.message.server.id, alias, value):
                        response = "Alias \"{0}{1}\" set to \"{0}{2}\"!".format(prefix, alias, value);
                    else:
                        response = "Alias \"{0}{1}\" could not be set!".format(prefix, alias);
                await bot.sendMessage( "`{}`".format(response))
    except Exception:
        logger.PrintException(bot.message)
        return False