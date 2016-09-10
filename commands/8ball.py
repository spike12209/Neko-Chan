import random
from functions import logger

DESC="Ask 8ball anything!"
USAGE="8ball [either question here or raw command then type question in next 10s.]"

async def init(bot):
    chat=bot.message.channel
    user=str(bot.message.author.name)
    try:
        answer = [ "Signs point to yes.",
        "Yes.",
        "Reply hazy, try again.",
        "Without a doubt.",
        "My sources say no.",
        "As I see it, yes.",
        "You may rely on it.",
        "Concentrate and ask again.",
        "Outlook not so good.",
        "It is decidedly so.",
        "Better not tell you now.",
        "Very doubtful.",
        "Yes - definitely.",
        "It is certain.",
        "Cannot predict now.",
        "Most likely.",
        "Ask again later.",
        "My reply is no.",
        "Outlook good.",
        "Don\'t count on it."]
        if len(bot.args) > 0:
            await bot.sendMessage( "{}".format(random.choice(answer)))
        else:
            await bot.sendMessage( 'What do you want to ask? (Waiting 10 Seconds)')
            reply = await bot.client.wait_for_message(timeout=10.0, author=bot.message.author)
            if reply is not None:
                await bot.sendMessage( "{}".format(random.choice(answer)))
            else:
                return False
    except Exception:
        logger.PrintException(bot.message)
