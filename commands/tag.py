from functions import config,logger,tools,tags,aliases,groups

DESC="Gets the text for a specific tag"
USAGE="tag [tag_name/info/add/delete]"

async def init(bot):
    try:
        if bot.message.channel.is_private:
            await bot.sendMessage( "This command is disabled in private chats!")
            return False
        if len(bot.args)==0:
            # No arguments giving. Assuming user wants a list.
            list = await tags.getAll(bot.message.server.id)
            if list is not None and len(list)>0:
                msg = ""
                for tag in list:
                    msg += tag['tag']+", "
                await bot.sendMessage("These are all tags on this server:\r\n```{}````{} Tags`".format(msg[:-2], len(list)))
            else:
                await bot.sendMessage("This server does not have any tags yet.")
        elif len(bot.args)>0:
            # args were given
            # First arg is "set" or "add"
            prefix = await config.getConf(bot.message.server.id, "prefix")
            if bot.args[0].casefold() == "set" or bot.args[0].casefold() == "add":
                # Has the user the right to set tags?
                if bot.access_level >= await groups.needed_level(bot.message.server.id, "tag_set"):
                    # Drop the first argument
                    bot.args.pop(0)
                    # No more arguments. We need at least a tag.
                    if len(bot.args)==0:
                        await bot.sendMessage(":question: To add a tag type `{}tag add [tag] [text]`".format(prefix))
                        return
                    # accept the tag and drop the next argument.
                    tag = bot.args[0]
                    bot.args.pop(0)
                    # We don't have a text.
                    if len(bot.args)==0:
                        await bot.sendMessage(":question: To add a tag type `{}tag add [tag] [text]`".format(prefix))
                        return False
                    text = " ".join(bot.args)
                    if await tags.set(bot.message.server.id, bot.message.author.id, tag, text, bot.message.timestamp):
                        await bot.sendMessage(":white_check_mark: Tag \"{}\" has been successfully created.".format(tag))
                    else:
                        await bot.sendMessage(":x: Tag \"{}\" could not be created. It most likely already exists.".format(tag))
            # First arg is "delete"
            elif bot.args[0].casefold() == "delete":
                # Delete only own tags
                if bot.access_level >= await groups.needed_level(bot.message.server.id, "tag_delete"):
                    # Delete the tag
                    bot.args.pop(0)
                    if len(bot.args)==0:
                        await bot.sendMessage(":question: To delete a tag type `{}tag delete [tag]`".format(prefix))
                        return False
                    tag = " ".join(bot.args)
                    if await tags.delete(bot.message.server.id, tag):
                        await bot.sendMessage(":white_check_mark: Tag \"{}\" has been successfully deleted.".format(tag))
                        return False
                    else:
                        await bot.sendMessage(":x: Tag \"{}\" does not exist.".format(tag))
                        return False
                # Has the user the right to delete tags?
                elif bot.access_level >= await groups.needed_level(bot.message.server.id, "tag_delete_own"):
                    # Delete the tag
                    bot.args.pop(0)
                    if len(bot.args)==0:
                        await bot.sendMessage(":question: To delete a tag type `{}tag delete [tag]`".format(prefix))
                        return False
                    tag = " ".join(bot.args)
                    s_tag = await tags.get(bot.message.server.id, tag)
                    if s_tag[0] == bot.message.author.id:
                        if await tags.delete(bot.message.server.id, tag):
                            await bot.sendMessage(":white_check_mark: Tag \"{}\" has been successfully deleted.".format(tag))
                    else:
                        await bot.sendMessage("You can only delete own tags!")
            elif bot.args[0].casefold() == "info":
                if bot.access_level >= await groups.needed_level(bot.message.server.id, "tag_info"):
                    # Get info about the tag
                    bot.args.pop(0)
                    if len(bot.args)==0:
                        await bot.sendMessage(":question: To get info about a tag type `{}tag info [tag]`".format(prefix))
                        return False
                    tag = " ".join(bot.args)
                    s_tag = await tags.get(bot.message.server.id, tag)
                    if s_tag is not None:
                        try:
                            owner = bot.message.server.get_member(s_tag[0]).display_name
                        except:
                            owner = s_tag[0]
                        await bot.sendMessage(":page_facing_up: Info:\n```Tag: {}\nOwner: {}\nDate: {}\nText: {}```".format(s_tag[1], owner, s_tag[3], s_tag[2]))
                    else:
                        await bot.sendMessage("Such tag doesn't exist!")

            else:
                tag = " ".join(bot.args)
                s_tag = await tags.get(bot.message.server.id, tag)
                if s_tag is not None and len(s_tag)>0:
                    await bot.sendMessage(s_tag[2])
    except Exception:
        logger.PrintException(bot.message)
        return False
