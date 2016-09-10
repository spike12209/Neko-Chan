import global_vars

DESC = "Gives you the link to add this bot to your server."
USAGE="link"


async def init(bot):
    await bot.sendMessage( 'Use the following link to add this bot to your own Server:\r\nhttps://discordapp.com/oauth2/authorize?&client_id={}&scope=bot&permissions=66321471'.format(global_vars.application_id))
