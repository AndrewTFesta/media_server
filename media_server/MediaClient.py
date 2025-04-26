"""
@title

@description

"""
import uuid
from collections import defaultdict

import discord

from media_server import data_dir
from media_server.storage import save_data, load_data


def get_top_channel(message):
    parent = message.channel
    return parent.id

def is_thread(message):
    return isinstance(message.channel, discord.Thread)

class MediaClient(discord.Client):

    def __init__(self, intents, model_server):
        """
        https://discord.com/developers/applications/1362593571340812379/information
        https://discordpy.readthedocs.io/en/stable/intro.html

        :param intents:
        """
        super().__init__(intents=intents)

        self.response_channels = [
            'bot',
            'app',
            'application',
            'top-secret'
        ]
        self.history = defaultdict(dict)
        self.channel_map = defaultdict(dict)
        self.channel_map_path = data_dir / 'channel_map.json'

        self.history_path = data_dir / 'history'
        for each_messages_path in self.history_path.glob('**/*.jsonl'):
            channel_id = each_messages_path.parent.stem
            messages = load_data(each_messages_path)

        self.model_server = model_server
        return

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        return

    async def on_message(self, message):
        message_is_thread = is_thread(message)
        top_channel = get_top_channel(message) if message_is_thread else None

        author_id = message.author.id
        author_name = message.author.name
        author_display_name = message.author.display_name
        channel_id = message.channel.id
        channel_name = message.channel.name

        print(f'Message in channel {channel_name} ({channel_id}) from {message.author}: {message.content}')
        respond_criteria = [
            message.author != self.user,
            not message.channel.name in self.response_channels,
            not top_channel in self.response_channels,
        ]
        if not all(respond_criteria):
            print(f'\tMessage is not set to respond')
            return

        if not channel_name in self.channel_map:
            self.channel_map[channel_id] = {'name': channel_name}
            save_data(self.channel_map, self.channel_map_path, human_readable=True)

        channel_history = self.history[channel_id]
        if not 'messages' in channel_history:
            channel_history['messages'] = []

        channel_entry = {
            'author_id': author_id,
            'author_name': author_name,
            'author_display_name': author_display_name,
            'message': message.content,
            'message_id': message.id,
            'is_thread': message_is_thread,
            'tts': message.tts,
            'message_type': message.type.name,
            'timestamp': message.created_at.isoformat(),
        }
        channel_history['messages'].append(channel_entry)

        messages_path = self.history_path / f'{channel_id}' / 'messages.jsonl'
        save_data(channel_entry, messages_path, append=True)

        model_entry = {
            'author_id': self.user.id,
            'author_name': self.user.name,
            'author_display_name': self.user.display_name,
            'message': None,
            'message_id': None,
            'message_thread': message_is_thread,
            'tts': None,
            'message_type': 'text',
            'timestamp': message.created_at.isoformat(),
            'success': False
        }
        try:
            if message_is_thread:
                history_length = 10
                user_history = [
                    each_message
                    for each_message in channel_history['messages']
                    if each_message['thread'] == message_thread
                ]
                # todo  reverse?
                user_history = sorted(user_history, key=lambda each_message: each_message['timestamp'])
                history_length = min(len(user_history), history_length)
                user_history = user_history[-history_length:]
            else:
                user_history = [channel_entry]

            user_history = [
                {
                    'role': 'assistant' if each_entry['author_id'] == self.user.id else 'user', 'content': each_entry['message']
                }
                for each_entry in user_history
            ]

            model_response = self.model_server.gen_text(user_history)
            model_entry['success'] = True
        except Exception as e:
            print(f'Error occurred while generating response: {e}')
            model_response = f'Shit broke somehow. WTF did you do, {author_display_name}?'
            model_entry['success'] = False

        model_entry['message'] = model_response
        channel_history['messages'].append(model_entry)
        if message_is_thread:
            thread_shortid = f'{uuid.uuid4()}'[:8]
            thread_name = f'{self.user.name}->{author_display_name}: {thread_shortid}'
            thread = await message.create_thread(name=thread_name)
        else:
            thread = await message.channel.get_thread(channel_id)
        await thread.send(f'[{author_display_name}]: {model_response}')
        return


