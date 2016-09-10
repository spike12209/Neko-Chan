from functions import logger, groups, botfunc
import asyncio
import global_vars

DESC="Skips the current playing song"
USAGE="skip"

async def init(bot):
    user=str(bot.message.author.name)
    level = await groups.getLevel(bot.message.server.id, bot.message.author)
    try:
        server_id = bot.message.server.id
        if server_id in global_vars.music_bots and await global_vars.music_bots.get(server_id).is_connected():
            if await global_vars.music_bots[server_id].is_playing():
                await botfunc.autoDelete(10,bot.message)
                if global_vars.music_bots[server_id].sender.id == bot.message.author.id:
                    # if await global_vars.music_bots[server_id].remaining()<=0:
                        # await botfunc.autoDelete(10,await bot.sendMessage( "Nothing left in queue. Stopping playback."),bot.message)
                    await global_vars.music_bots[server_id].playNext()
                    return True
                elif bot.access_level >= await groups.needed_level(server_id, "skip_admin"):
                    message = await bot.sendMessage( "You have rights to skip it instantly. Do you want to bypass voting? Answer: `yes` or `no`")
                    reply = await bot.client.wait_for_message(timeout=10.0, author=bot.message.author)
                    if reply is not None:
                        if reply.content.casefold() == "yes":
                            await global_vars.music_bots[server_id].playNext()
                            return True
                        else:
                            return await global_vars.music_bots[server_id].voteSkip(bot.message.author)
                        await botfunc.autoDelete(10, message, reply)
                else:
                    return await global_vars.music_bots[server_id].voteSkip(bot.message.author)
            else:
                await botfunc.autoDelete(10,await bot.sendMessage( "There is no song playing."),bot.message)
                #del global_vars.music_bots[server_id]
        await botfunc.autoDelete(10,await bot.sendMessage( "There's no active player."),bot.message)
    except:
        logger.PrintException(bot.message)
