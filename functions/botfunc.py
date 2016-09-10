import discord
import asyncio
import global_vars
from functions import logger

loop = asyncio.get_event_loop()

async def delete(time,messages):
    try:
        await asyncio.sleep(time)
        for message in messages:
            try:
                await global_vars.client.delete_message(message)
            except discord.NotFound:
                pass
            except discord.Forbidden:
                print("I'm not allowed to delete message.")
            except:
                logger.PrintException(message)
    except:
        logger.PrintException()
    
async def autoDelete(time, *args):
    try:
        loop.create_task(delete(time,args))
    except:
        logger.PrintException()