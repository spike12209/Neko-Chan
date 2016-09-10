from functions import logger, config
import asyncio

class MessageHandler:
    def __init__(self, client, message, command, args):
        ''' Create a new messagehandler which handles the required parts for the commands.
        disabling this module will fuck up the whole bot.'''
        self.client = client
        self.message = message
        self.command = command
        self.channel = message.channel
        self.access_level = 0
        self.needed_level = 6
        self.args = args
    async def sendMessage(self, text, channel=None):
        '''
        Sends a text message to a channel.
        Arguments:
            (str) text: The message you want to send
            (Optional) channel: The channel you want the message to be sent in
        Returns:
            An messageobject if the message has been sent, None otherwise.'''
        message = None
        text = str(text)
        if len(text)==0:
            raise ValueError("The message needs at least one character.")
        if len(text)>2000:
            raise ValueError("The message can\'t be more than 2000 chars")
        if channel is None:
            message = await self.client.send_message(self.channel, "\u200B{}".format(text))
        else:
            message = await self.client.send_message(channel, "\u200B{}".format(text))
        return message