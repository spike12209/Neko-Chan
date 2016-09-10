from discord.ext import commands
import asyncio
import traceback
import discord
import inspect
import sys
from io import StringIO  # Python3


class REPL:
    def __init__(self, client):
        self.client = client
        self.sessions = set()

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    def get_syntax_error(self, e):
        return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

    async def repl(self, ctx):
        msg = ctx.message
        variables = {
            'bot': self.client,
            'message': msg,
            'server': msg.server,
            'channel': msg.channel,
            'author': msg.channel,
            'last': None,
        }

        if msg.channel.id in self.sessions:
            await ctx.sendMessage('Already running a REPL session in this channel. Exit it with `quit`.')
            return

        self.sessions.add(msg.channel.id)
        await ctx.sendMessage('Enter code to execute or evaluate. `exit()` or `quit` to exit.')
        while True:
            response = await self.client.wait_for_message(author=msg.author, channel=msg.channel,
                                                       check=lambda m: m.content.startswith('`'))
            # Let the user know I'm processing
            self.client.send_typing(msg.channel)
            cleaned = self.cleanup_code(response.content)

            if cleaned in ('quit', 'exit', 'exit()'):
                await ctx.sendMessage('Exiting.')
                self.sessions.remove(msg.channel.id)
                return

            executor = exec
            if cleaned.count('\n') == 0 and not "print" in cleaned:
                # single statement, potentially 'eval'
                try:
                    code = compile(cleaned, '<repl session>', 'eval')
                except SyntaxError:
                    pass
                else:
                    executor = eval

            if executor is exec:
                try:
                    code = compile(cleaned, '<repl session>', 'exec')
                except SyntaxError as e:
                    await ctx.sendMessage(self.get_syntax_error(e))
                    continue

            variables['message'] = response

            fmt = None

            try:
                if executor is exec:
                    old_stdout = sys.stdout
                    result = StringIO()
                    sys.stdout = result
                    executor(code, variables)
                    sys.stdout = old_stdout
                    result = result.getvalue()
                else:
                    result = executor(code, variables)
            except Exception as e:
                fmt = '```py\n{}\n```'.format(traceback.format_exc())
            else:
                if result is not None:
                    fmt = '```py\n{}\n```'.format(result)
                    variables['last'] = result

            try:
                if fmt is not None:
                    if len(fmt) > 2000:
                        await ctx.sendMessage('Content too big to be printed.')
                    else:
                        await ctx.sendMessage(fmt)
            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                await ctx.sendMessage('Unexpected error: `{}`'.format(e))