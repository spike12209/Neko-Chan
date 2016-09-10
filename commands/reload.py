from functions import logger
import asyncio
import importlib

DESC="Reloads the given module"
USAGE="reload *module*"



async def init(bot):
    try:
        if len(bot.args)<1:
            await bot.sendMessage( 'Which module should be reloaded? (Waiting 10 Seconds)')
            reply = await bot.client.wait_for_message(timeout=10.0, author=bot.message.author)
            if reply is not None:
                module = reply.content
            else:
                return False
        else:
            module = " ".join(bot.args)
        try:
            func = importlib.import_module(module)
            importlib.reload(func)
            await bot.sendMessage( "Reloaded \"{}\"".format(module))
        except Exception as e:
            if "No module named '{}'".format(module) in str(e):
                await bot.sendMessage( "Can't find a module named \"{}\"".format(module))
            else:
                logger.PrintException(bot.message)
                await bot.sendMessage( "Can't reload \"{}\" due to a error.".format(module))
                    
    except:
        logger.PrintException(bot.message)