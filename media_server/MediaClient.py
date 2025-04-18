"""
@title

@description

"""

import discord

class MediaClient(discord.Client):

    def __init__(self, intents):
        """
        https://discord.com/developers/applications/1362593571340812379/information
        https://discordpy.readthedocs.io/en/stable/intro.html

        :param intents:
        """
        super().__init__(intents=intents)
        return

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        return

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        return
