from functions import tools,logger
import json

DESC="Current BTC exchange rate"
USAGE="btc"

async def init(bot):
    chat=bot.message.channel
    user=str(bot.message.author.name)
    try:
        if len(bot.args) > 0:
            rate = await tools.btcrate(bot.args[0].upper())
            if rate is False:
                await bot.sendMessage( 'Wrong currency!')
            else:
                await bot.sendMessage( 'Current BTC rate: {} {}'.format(rate, bot.args[0].upper()))
        else:
            rate = await tools.btcrate()
            await bot.sendMessage( 'Current BTC rate: {} USD'.format(rate))
    except:
        logger.PrintException(bot.message)
