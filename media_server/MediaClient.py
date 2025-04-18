"""
@title

@description

"""
from collections import defaultdict

import discord

from media_server import data_dir
from media_server.storage import save_data, load_data


class MediaClient(discord.Client):

    def __init__(self, intents):
        """
        https://discord.com/developers/applications/1362593571340812379/information
        https://discordpy.readthedocs.io/en/stable/intro.html

        :param intents:
        """
        super().__init__(intents=intents)

        self.response_channels = [
            'bot',
            'app',
            'application'
        ]
        self.history = defaultdict(dict)
        self.channel_map = defaultdict(dict)
        self.channel_map_path = data_dir / 'channel_map.json'

        self.history_path = data_dir / 'history'
        for each_messages_path in self.history_path.glob('**/*.jsonl'):
            channel_id = each_messages_path.parent.stem
            messages = load_data(each_messages_path)

        return

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        return

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        author_id = message.author.id
        author_name = message.author.name
        author_display_name = message.author.display_name
        channel_id = message.channel.id
        channel_name = message.channel.name

        if not channel_name in self.channel_map:
            self.channel_map[channel_id] = channel_name
            save_data(self.channel_map, self.channel_map_path, human_readable=True)

        channel_history = self.history[channel_id]
        channel_history['name'] = author_name
        channel_history['id'] = channel_id
        if not 'messages' in channel_history:
            channel_history['messages'] = []

        channel_entry = {
            'author_id': author_id,
            'author_name': author_name,
            'author_display_name': author_display_name,
            'message': message.content,
            'message_id': message.id,
            'message_thread': message.thread,
            'tts': message.tts,
            'message_type': message.type.name,
            'timestamp': message.created_at.isoformat(),
        }
        channel_history['messages'].append(channel_entry)

        messages_path = self.history_path / f'{channel_id}' / 'messages.jsonl'
        save_data(channel_entry, messages_path, append=True)

        if message.author == self.user:
            return

        if not message.channel.name in self.response_channels:
            return

        await message.channel.send(f'The fuck you want, {author_display_name}?')
        return


