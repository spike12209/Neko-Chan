from functions import logger
from time import localtime, strftime

DESC="Report a bug to devs"
USAGE="bug \"message\""

async def init(bot):
    try:
        if len(bot.args)>0:
            msg = " ".join(bot.args)
            msg = msg[:1500]
            report = "**Bug report**:\r\n"
            report += "Reported by: {}#{}\r\n".format(bot.message.author.name,bot.message.author.discriminator)
            report += "Server: {} (ID: {})\r\n".format(bot.message.server.name, bot.message.server.id)
            report += "Time: {}\r\n".format(strftime("%H:%M:%S", localtime()))
            report += "Bug report: {}".format(msg)
            await logger.send_error_to_devs(report)
            await bot.sendMessage( ":white_check_mark: Your bug has been reported to my developers.\r\nThey will contact you if they have further questions.")
        else:
            await bot.sendMessage( "You have to describe the bug.")
    except Exception:
        logger.PrintException(bot.message)
        return False
