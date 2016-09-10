from functions import tools

DESC="Check online status of domain"
USAGE="isup domain"


async def init(bot):
    chat=bot.message.channel
    user=str(bot.message.author.name)
    if len(bot.args) > 0:
        await bot.sendMessage( '{}'.format(await tools.isUP(bot.args[0])))
    else:
        await bot.sendMessage( "Please provide site you want to check!")
