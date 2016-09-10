from functions import logger
import time
import global_vars
import math
import psutil
import os

DESC="Print informations about this bot"
USAGE="stats"

async def init(bot):
    try:
        channels = 0
        members = 0
        for srv in bot.client.servers:
            channels = channels + len(srv.channels)
            members = members + srv.member_count
        stats = "Name: {}\r\nUID: {}\r\n".format(bot.client.user.name, bot.client.user.id)
        stats += "Running music bots: {}\r\n".format(len(global_vars.music_bots))
        stats += "Servers: {} **|** Channels: {} **|** Users: {}\r\n".format(len(bot.client.servers), channels, members)
        if global_vars.started is not None:
            secs = time.time()-global_vars.started
            hours = math.floor(secs/3600)
            mins = math.floor((secs-(hours*3600))/60)
            secs = math.floor(secs-(hours*3600)-(mins*60))
            stats += "Uptime: {} hours {} minutes {} seconds\r\n".format(hours, mins, secs)
        process = psutil.Process(os.getpid())
        mem = process.memory_info()[0]
        memp = process.memory_percent()
        for child in process.children(recursive=True):
            mem += child.memory_info()[0]
            memp += child.memory_percent()
        mem = mem / float(2 ** 20)
        stats += "Memory usage: {:.2f} MiB, {:.2f} %\r\nCPU usage: {:.2f} %".format(mem, memp, psutil.cpu_percent())
        await bot.sendMessage( stats)
    except Exception:
        logger.PrintException(bot.message)
