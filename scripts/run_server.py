"""
@title

@description

"""
import argparse
import os

import discord

from media_server import env_dir
from media_server.MediaClient import MediaClient
from media_server.gemini_server import GeminiServer
from media_server.ollama_server import OllamaServer


def main(main_args):
    """
    If you want to generate this URL dynamically at run-time inside your bot and using the
    discord.Permissions interface, you can use discord.utils.oauth_url().

    https://discordpy.readthedocs.io/en/stable/api.html#discord.Permissions
    https://discordpy.readthedocs.io/en/stable/api.html#discord.utils.oauth_url
    https://discord.com/developers/docs/topics/oauth2#bots

    :param main_args:
    :return:
    """
    model_name = 'hf.co/soob3123/amoral-gemma3-4B-v1-gguf:F16'
    model_server_type = OllamaServer
    print(f'Loading model server {model_server_type} with model: {model_name}')
    model_server = model_server_type(model_name=model_name)

    print(f'Loading token from {env_dir}')
    media_server_token = os.getenv('MEDIA_SERVER_TOKEN')

    intents = discord.Intents.all()
    client = MediaClient(intents=intents, model_server=model_server)

    client.run(media_server_token)
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')

    args = parser.parse_args()
    main(vars(args))
