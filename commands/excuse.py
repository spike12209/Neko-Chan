from functions import tools

DESC="Coding excuse."
USAGE="excuse"


async def init(bot):
    chat=bot.message.channel
    user=str(bot.message.author.name)
    await bot.sendMessage( '{}'.format(await tools.excuse()))
