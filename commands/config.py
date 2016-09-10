from functions import config,logger, tools

DESC="Set/Get a config"
USAGE="config [setting] [value]"

async def init(bot):
    chat=bot.message.channel
    response = ""
    try:
        if bot.message.channel.is_private:
            await bot.sendMessage( "This command is disabled in private chats!")
            return False
        if len(bot.args)==0:
            settings = await config.getAllConf(bot.message.server.id);
            if settings is not None:
                for conf in settings:
                    if str(conf['value']).startswith("@"):
                        conf['value'] = conf['value'][1:]
                    response += "({}){}: \"{}\" # {}\r\n".format(conf['type'], conf['setting'], tools.convertVal(conf['type'], conf['value']), conf['desc'])
            else:
                response += "No config values found.";
            await bot.sendMessage( "```{}```".format(response))
        elif len(bot.args)==1:
            s_string=bot.args[0]
            setting = await config.confData(bot.message.server.id, str(s_string));
            if setting is not None:
                if str(setting['value']).startswith("@"):
                    setting['value'] = setting['value'][1:]
                response += "({}){}: \"{}\" # {}\r\n".format(setting['type'], setting['setting'], tools.convertVal(setting['type'], setting['value']), setting['desc'])
            else:
                response += "No config value named \"{}\" found".format(s_string);
            await bot.sendMessage( "`{}`".format(response))
        else:
            s_string=bot.args[0]
            setting = await config.confData(bot.message.server.id, str(s_string));
            bot.args.pop(0)
            value = " ".join(bot.args)
            if setting is not None:
                value = tools.convertVal(setting['type'], value)
                if value is not None:
                    if str(tools.convertVal(setting['type'], (setting['value']))) == str(value):
                        await bot.sendMessage("Setting `{}` is already set to `{}`!".format(setting['setting'], str(value)));
                        return False
                    elif await config.setConf(bot.message.server.id, setting['setting'], value):
                        response = "Setting \"{}\" set to \"{}\"!".format(setting['setting'], str(value));
                    else:
                        response = "Setting \"{}\" could not be set!".format(setting['setting'],);
                else:
                    response = "Setting \"{}\" has to be of type {}".format(setting['setting'], setting['type']);
                pass
            else:
                response = "No config value named \"{}\" found".format(s_string);
            await bot.sendMessage( "`{}`".format(response))
    except Exception:
        logger.PrintException(bot.message)
        return False
